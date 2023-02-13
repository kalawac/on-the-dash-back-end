from app import db
from flask import Blueprint, jsonify, request, make_response, abort
import uuid

from app.models.contact import Contact
from app.models.org import Org
from app.models.contact_org import xContactOrg
from app.models.types.gender import Gender
from .utils import validate_UUID, append_dicts_to_list

bp = Blueprint("contacts_bp", __name__, url_prefix="/contacts")

def validate_gender_enum(gender_id):
    try:
        return Gender(int(gender_id))
    except ValueError:
        try:
            return Gender[gender_id]
        except KeyError:
            abort(make_response({"message": "Invalid gender value submitted"}, 400))

def validate_request_body(request_body):
    if not request_body.get("lname"):
        abort(make_response({"message": "Contact requires last name"}, 400))

    if (("fname" not in request_body) or ("age" not in request_body) or
        ("gender" not in request_body)):
        abort(make_response(
            {"message": "Request body requires the following keys: 'fname', 'lname', 'age', 'gender'"}, 400))

    gender_id = request_body["gender"]
    gender_enum = validate_gender_enum(gender_id)

    org_data = request_body.get("orgs", [])
    org_list = []

    if org_data:
        if type(org_data) == list or type(org_data) == tuple:
            for org_id in org_data:
                org = validate_UUID(Org, org_id)
                org_list.append(org)

        else:
            org = validate_UUID(Org, org_list)
            org_list.append(org)

    validated_dict = dict(
        fname=request_body["fname"],
        lname=request_body["lname"],
        age=request_body["age"] if request_body["age"] else 0,
        gender=gender_enum,
        orgs=org_list
    )

    return validated_dict


@bp.route("", methods=["POST"], strict_slashes=False)
def create_contact():
    request_body = request.get_json()

    contact_dict = validate_request_body(request_body)

    new_contact = Contact.new_from_dict(contact_dict)

    db.session.add(new_contact)
    db.session.commit()

    return make_response(jsonify(new_contact.to_dict()), 201)


def find_and_operator(query_value):
    if str(query_value).find("+") > -1:
        plus_split = "+"
    elif str(query_value).find(" ") > -1:
        plus_split = " "
    elif str(query_value).find("%2B") > -1:
        plus_split = "%2B"
    else:
        plus_split = False
    
    return plus_split

@bp.route("", methods=["GET"], strict_slashes=False)
def get_all_contacts():
    sort_query = request.args.get("sort")
    name_query = request.args.get("name")
    fname_query = request.args.get("fname")
    lname_query = request.args.get("lname")
    gender_query = request.args.get("gender")
    org_query = request.args.get("org")
    logical_or = request.args.get("OR")

    contacts_query = Contact.query

    if logical_or:
        existing_query = False

        if fname_query:
            contacts_query = contacts_query.filter(Contact.fname.ilike(f'%{fname_query}%'))
            existing_query = True
        
        if lname_query:
            if existing_query:
                q_lname = Contact.query.filter(Contact.lname.ilike(f'%{lname_query}%'))
                contacts_query = contacts_query.union(q_lname)
            else:
                contacts_query = contacts_query.filter(Contact.lname.ilike(f'%{lname_query}%'))
                existing_query = True
        
        if name_query:
            qfn = Contact.query.filter(Contact.fname.ilike(f'%{name_query}%'))
            qln = Contact.query.filter(Contact.lname.ilike(f'%{name_query}%'))

            if existing_query:
                q_name = qfn.union(qln)
                contacts_query = contacts_query.union(q_name)
            else:
                contacts_query = qfn.union(qln)
                existing_query = True
        
        if gender_query:
            gender_enum = validate_gender_enum(gender_query)

            if existing_query:
                q_gender = Contact.query.filter_by(gender=gender_enum)
                contacts_query = contacts_query.union(q_gender)
            else:
                contacts_query = contacts_query.filter_by(gender=gender_enum)
                existing_query = True

        if org_query:
            org_plus_split = find_and_operator(org_query)

            if org_plus_split:
                query_items = org_query.split(org_plus_split)
                item_query = Contact.query

                i = 0
                for org_id in query_items:
                    org = validate_UUID(Org, org_id)
                    item_query = item_query.join(xContactOrg).join(Org).filter(xContactOrg.org_id == org.id)
                    if i == 0:
                        build_query = item_query
                    else:
                        build_query = build_query.union(item_query)
                    i += 1
                
                if existing_query:
                    contacts_query = contacts_query.union(build_query)
                else:
                    contacts_query = build_query
            elif org_query.find("_") > -1:
                query_items = org_query.split("_")
                for org_id in query_items:
                    org = validate_UUID(Org, org_id)
                    item_query = Contact.query.join(xContactOrg).join(Org).filter(xContactOrg.org_id == org.id)
                    contacts_query = contacts_query.union(item_query)
            else:
                org = validate_UUID(Org, org_query)
                if existing_query:
                    q_org = Contact.query.join(xContactOrg).join(Org).filter((xContactOrg.org_id == org.id))
                    contacts_query = contacts_query.union(q_org)
                else:
                    contacts_query = contacts_query.join(xContactOrg).join(Org).filter((xContactOrg.org_id == org.id))

    else:
        if fname_query:
            contacts_query = contacts_query.filter(Contact.fname.ilike(f'%{fname_query}%'))
        
        if lname_query:
            contacts_query = contacts_query.filter(Contact.lname.ilike(f'%{lname_query}%'))
        
        if name_query:
            qfn = Contact.query.filter(Contact.fname.ilike(f'%{name_query}%'))
            qln = Contact.query.filter(Contact.lname.ilike(f'%{name_query}%'))
            contacts_query = qfn.union(qln)
        
        if gender_query:
            gender_enum = validate_gender_enum(gender_query)
            contacts_query = contacts_query.filter_by(gender=gender_enum)

        if org_query:
            org_plus_split = find_and_operator(org_query)

            if org_plus_split:
                query_items = org_query.split(org_plus_split)
                for org_id in query_items:
                    org = validate_UUID(Org, org_id)
                    item_query = Contact.query.join(xContactOrg).join(Org).filter(xContactOrg.org_id == org.id)
                    contacts_query = contacts_query.intersect(item_query)

            elif org_query.find("_") > -1:
                query_items = org_query.split("_")
                i = 0
                for org_id in query_items:
                    org = validate_UUID(Org, org_id)
                    item_query = Contact.query.join(xContactOrg).join(Org).filter(xContactOrg.org_id == org.id)
                    if i == 0:
                        build_query = item_query
                    else:
                        build_query = build_query.union(item_query)
                    i += 1
                contacts_query = contacts_query.intersect(build_query)

            else:
                org = validate_UUID(Org, org_query)
                contacts_query = contacts_query.join(xContactOrg).join(Org).filter(xContactOrg.org_id == org.id)

    if sort_query:
        if sort_query == "desc":
            contacts_query = contacts_query.order_by(Contact.lname.desc())

        if sort_query == "fname":
            contacts_query = contacts_query.order_by(Contact.fname)
        elif sort_query == "fname-desc":
            contacts_query = contacts_query.order_by(Contact.fname.desc())
    else:
        contacts_query = contacts_query.order_by(Contact.lname)

    contacts = contacts_query.all()

    if not contacts:
        return jsonify([])

    contacts_response = append_dicts_to_list(contacts)

    return jsonify(contacts_response)


@bp.route("/<uuid:id>", methods=["GET"], strict_slashes=False)
def get_contact(id):
    contact = validate_UUID(Contact, id)
    return contact.to_dict()


@bp.route("/<uuid:id>", methods=["PUT"])
def update_contact(id):
    contact = validate_UUID(Contact, id)
    request_body = request.get_json()
    
    contact_dict = validate_request_body(request_body)

    contact.fname = contact_dict["fname"]
    contact.lname = contact_dict["lname"]
    contact.age = contact_dict["age"]
    contact.gender = contact_dict["gender"]
    contact.orgs = contact_dict["orgs"]

    db.session.add(contact)
    db.session.commit()

    return jsonify(contact.to_dict())


@bp.route("/<uuid:id>", methods=["DELETE"])
def delete_contact(id):
    contact = validate_UUID(Contact, id)
    db.session.delete(contact)
    db.session.commit()
    return make_response({"message": f"Contact {contact.fname} {contact.lname} successfully deleted"}, 200)