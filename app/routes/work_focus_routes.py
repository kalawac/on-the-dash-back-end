from app import db
from app.models.work_focus import WorkFocus
from .utils import validate_instance, append_dicts_to_list
from flask import Blueprint, jsonify, request, make_response, abort

bp = Blueprint("wf_bp", __name__, url_prefix="/wf")

@bp.route("", methods=["POST"], strict_slashes=False)
def create_wf_item():
    request_body = request.get_json()

    if not request_body.get("label") or request_body["label"]=="":
        abort(make_response({"message": "WorkFocus item requires label"}, 400))

    new_wf = WorkFocus(label=request_body["label"])

    db.session.add(new_wf)
    db.session.commit()

    return make_response(jsonify(new_wf.to_dict()), 201)


# no button on FE - delete before freeze?
@bp.route("/initial", methods=["POST"])
def create_initial_wf_items():
    db.session.add_all([
        WorkFocus(label='INDIGENOUS'),
        WorkFocus(label='LGBTI'),
        WorkFocus(label='RELIGIOUS_FREEDOM'),
        WorkFocus(label='WOMENS_RIGHTS'),
        WorkFocus(label='OTHER')
    ])
    db.session.commit()

    foci = WorkFocus.query.all()

    wf_response = append_dicts_to_list(foci)

    return make_response(jsonify(wf_response), 201)


@bp.route("", methods=["GET"], strict_slashes=False)
def get_all_work_foci():
    sort_query = request.args.get("sort")
    label_query = request.args.get("label")
    id_query = request.args.get("id")

    wf_query = WorkFocus.query

    if sort_query:
        if sort_query == "desc":
            wf_query = wf_query.order_by(WorkFocus.id.desc())

        if sort_query == "label":
            wf_query = wf_query.order_by(WorkFocus.label)
        elif sort_query == "label-desc":
            wf_query = wf_query.order_by(WorkFocus.label.desc())
    else:
        wf_query = wf_query.order_by(WorkFocus.id)

    if label_query:
        wf_query = wf_query.filter(WorkFocus.label.contains(label_query))
    
    if id_query:
        wf_query = wf_query.filter_by(id=id_query)

    foci = wf_query.all()

    if not foci:
        return jsonify([])

    wf_response = append_dicts_to_list(foci)

    return jsonify(wf_response)


@bp.route("/<id>", methods=["GET"], strict_slashes=False)
def get_work_focus_item(id):
    wf = validate_instance(WorkFocus, id)
    return wf.to_dict()


# use judiciously - include warning that it will reclassify all items, past and present
@bp.route("/<id>", methods=["PATCH"])
def update_work_focus_label(id):
    wf = validate_instance(WorkFocus, id)
    request_body = request.get_json()
    
    wf.label = request_body["label"]
    db.session.commit()
    return jsonify(wf.to_dict())


# don't make a button on this on FE - could mess up the database
@bp.route("/<id>", methods=["DELETE"])
def delete_work_focus_item(id):
    wf = validate_instance(WorkFocus, id)
    db.session.delete(wf)
    db.session.commit()
    return make_response({"message": f"<WorkFocus.{wf.label}: {id}> successfully deleted"}, 200)