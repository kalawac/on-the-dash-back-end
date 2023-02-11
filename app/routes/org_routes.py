from app import db
from flask import Blueprint, jsonify, request, make_response, abort
from app.models.org import Org
from app.models.types.org_sector import OrgSector
from .utils import validate_UUID, validate_intID, append_dicts_to_list

bp = Blueprint("orgs_bp", __name__, url_prefix="/orgs")

@bp.route("", methods=["POST"], strict_slashes=False)
def create_org():
    request_body = request.get_json()

    if not request_body.get("name"):
        abort(make_response({"message": "Organization requires a name"}, 400))

    if ("sector" not in request_body):
        abort(make_response(
            {"message": "Request body requires the following keys: 'name', 'sector'"}, 400))

    sector_data = request_body["sector"]

    try:
        OrgSector(int(sector_data))
    except ValueError:
        try:
            OrgSector[sector_data]
        except KeyError:
            abort(make_response({"message": "Invalid sector value"}, 400))

    new_org = Org.new_from_dict(request_body)

    db.session.add(new_org)
    db.session.commit()

    return make_response(jsonify(new_org.to_dict()), 201)