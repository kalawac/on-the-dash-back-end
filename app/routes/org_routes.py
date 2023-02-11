from app import db
from flask import Blueprint, jsonify, request, make_response, abort
from app.models.contact import Contact
from .utils import validate_UUID, validate_intID, append_dicts_to_list

bp = Blueprint("orgs_bp", __name__, url_prefix="/orgs")

@bp.route("", methods=["POST"], strict_slashes=False)
def create_org():
    request_body = request.get_json()

    if not request_body.get("name"):
        abort(make_response({"message": "Contact requires last name"}, 400))

    new_contact = Contact.new_from_dict(request_body)

    db.session.add(new_contact)
    db.session.commit()

    return make_response(jsonify(new_contact.to_dict()), 201)