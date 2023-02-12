from app import db
from flask import Blueprint, jsonify, request, make_response, abort

from app.models.org import Org
from app.models.types.org_sector import OrgSector
from app.models.types.work_focus import WF
from .utils import validate_UUID, append_dicts_to_list

bp = Blueprint("orgs_bp", __name__, url_prefix="/orgs")

def validate_sector_enum(sector_id):
    try:
        return OrgSector(int(sector_id))
    except ValueError:
        try:
            return OrgSector[sector_id]
        except KeyError:
            abort(make_response({"message": "Invalid sector value submitted"}, 400))

def validate_wf_enum(wf_id):
    try:
        return WF(int(wf_id))
    except ValueError:
        try:
            return WF[wf_id]
        except KeyError:
            abort(make_response({"message": "Invalid work focus value(s) submitted"}, 400))

def validate_request_body(request_body):
    if not request_body.get("name"):
        abort(make_response({"message": "Organization requires a name"}, 400))

    if (("sector" not in request_body) or ("foci" not in request_body)):
        abort(make_response(
            {"message": "Request body requires the following keys: 'name', 'sector', 'foci'"}, 400))

    sector_id = request_body["sector"]
    sector_enum = validate_sector_enum(sector_id)

    wf_data = request_body["foci"]
    wf_list = []

    if wf_data:
        if type(wf_data) == list or type(wf_data) == tuple:
            for wf_id in wf_data:
                wf_enum = validate_wf_enum(wf_id)
                wf_list.append(wf_enum)
        else:
            wf_enum = validate_wf_enum(wf_data)
            wf_list.append(wf_enum)

    validated_dict = dict(
        name=request_body["name"],
        org_sector=sector_enum,
        foci=wf_list
    )

    return validated_dict

@bp.route("", methods=["POST"], strict_slashes=False)
def create_org():
    request_body = request.get_json()

    org_dict = validate_request_body(request_body)

    new_org = Org.new_from_dict(org_dict)

    db.session.add(new_org)
    db.session.commit()

    return make_response(jsonify(new_org.to_dict()), 201)

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
def get_all_orgs():
    sort_query = request.args.get("sort")
    name_query = request.args.get("name")
    sector_query = request.args.get("sector")
    wf_query = request.args.get("wf")
    logical_or = request.args.get("OR")

    orgs_query = Org.query

    if logical_or:
        existing_query = False

        if name_query:
            orgs_query = orgs_query.filter(Org.name.ilike(f'%{name_query}%'))
            existing_query = True
        
        if sector_query:
            sector_enum = validate_sector_enum(sector_query)

            if existing_query:
                q_sector = Org.query.filter_by(org_sector=sector_enum)
                orgs_query = orgs_query.union(q_sector)
            else:
                orgs_query = orgs_query.filter_by(org_sector=sector_enum)
                existing_query = True

        if wf_query:
            wf_plus_split = find_and_operator(wf_query)

            if wf_plus_split:
                query_items = wf_query.split(wf_plus_split)
                for wf_id in query_items:
                    wf_enum = validate_wf_enum(wf_id)
                    item_query = Org.query.filter(Org.foci.any(wf_enum))
                
                if existing_query:
                    orgs_query = orgs_query.union(item_query)
                else:
                    orgs_query = item_query
            elif wf_query.find("_") > -1:
                query_items = wf_query.split["_"]
                for wf_id in query_items:
                    wf_enum = validate_wf_enum(wf_id)
                    item_query = Org.query.filter(Org.foci.any(wf_enum))
                    orgs_query = orgs_query.union(item_query)
            else:
                wf_enum = validate_wf_enum(wf_query)
                if existing_query:
                    q_wf = Org.query.filter(Org.foci.any(wf_enum))
                    orgs_query = orgs_query.union(q_wf)
                else:
                    orgs_query = orgs_query.filter(Org.foci.any(wf_enum))

    else:
        if name_query:
            orgs_query = orgs_query.filter(Org.name.ilike(f'%{name_query}%'))
        
        if sector_query:
            sector_enum = validate_sector_enum(sector_query)
            orgs_query = orgs_query.filter_by(org_sector=sector_enum)

        if wf_query:
            wf_plus_split = find_and_operator(wf_query)

            if wf_plus_split:
                query_items = wf_query.split(wf_plus_split)
                
                for wf_id in query_items:
                    wf_enum = validate_wf_enum(wf_id)
                    orgs_query = orgs_query.filter(Org.foci.any(wf_enum))
            elif wf_query.find("_") > -1:
                query_items = wf_query.split("_")
                for wf_id in query_items:
                    wf_enum = validate_wf_enum(wf_id)
                    item_query = Org.query.filter(Org.foci.any(wf_enum))
                    orgs_query = orgs_query.union(item_query)
            else:
                wf_enum = validate_wf_enum(wf_query)
                orgs_query = orgs_query.filter(Org.foci.any(wf_enum))

    if sort_query:
        if sort_query == "desc":
            orgs_query = orgs_query.order_by(Org.name.desc())
    else:
        orgs_query = orgs_query.order_by(Org.name)

    orgs = orgs_query.all()

    if not orgs:
        return jsonify([])

    orgs_response = append_dicts_to_list(orgs)

    return jsonify(orgs_response)


@bp.route("/<uuid:id>", methods=["GET"], strict_slashes=False)
def get_org(id):
    org = validate_UUID(Org, id)
    return org.to_dict()


@bp.route("/<uuid:id>", methods=["PUT"])
def update_org(id):
    org = validate_UUID(Org, id)
    request_body = request.get_json()
    
    org_dict = validate_request_body(request_body)

    org.name = org_dict["name"]
    org.org_sector = org_dict["org_sector"]
    org.foci = org_dict["foci"]

    db.session.add(org)
    db.session.commit()

    return jsonify(org.to_dict())


@bp.route("/<uuid:id>", methods=["DELETE"])
def delete_org(id):
    org = validate_UUID(Org, id)
    db.session.delete(org)
    db.session.commit()
    return make_response({"message": f"Organization '{org.name}' successfully deleted"}, 200)