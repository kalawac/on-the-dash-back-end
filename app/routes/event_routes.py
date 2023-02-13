from flask import Blueprint, jsonify, request, make_response, abort
from datetime import date

from app import db
from app.models.event import Event
from app.models.contact import Contact
from app.models.event_attendance import xEventAttendance
from app.models.types.event_type import EventType
from app.models.types.subject import Subject
from .utils import validate_UUID, append_dicts_to_list


bp = Blueprint("events_bp", __name__, url_prefix="/events")

def validate_date(date_string):
    try:
        return date.fromisoformat(date_string)
    except (ValueError, TypeError):
        abort(make_response({"message": "Invalid date value submitted"}, 400))

def validate_type_enum(type_id):
    try:
        return EventType(int(type_id))
    except ValueError:
        try:
            return EventType[type_id]
        except KeyError:
            abort(make_response({"message": "Invalid type value submitted"}, 400))

def validate_subject_enum(subject_id):
    try:
        return Subject(int(subject_id))
    except ValueError:
        try:
            return Subject[subject_id]
        except KeyError:
            abort(make_response({"message": "Invalid work focus value(s) submitted"}, 400))

def validate_request_body(request_body):
    if not request_body.get("name"):
        abort(make_response({"message": "Event requires a name"}, 400))

    if not request_body.get("date"):
        abort(make_response({"message": "No date value received"}, 400))

    date_obj = validate_date(request_body["date"])

    if (("type" not in request_body) or ("subjects" not in request_body)):
        abort(make_response(
            {"message": "Request body requires the following keys: 'name', 'type', 'subjects', 'date'"}, 400))

    type_id = request_body["type"]
    type_enum = validate_type_enum(type_id)

    subject_data = request_body["subjects"]
    subject_list = []

    if subject_data:
        if type(subject_data) == list or type(subject_data) == tuple:
            for subject_id in subject_data:
                subject_enum = validate_subject_enum(subject_id)
                subject_list.append(subject_enum)
        else:
            subject_enum = validate_subject_enum(subject_data)
            subject_list.append(subject_enum)

    participant_data = request_body.get("participants", [])
    participant_dict = {}
    attendance_dict = {}

    if participant_data: # list of dictionaries
            for contact_dict in participant_data:
                contact_id = str(contact_dict["id"])
                participant = validate_UUID(Contact, contact_id)
                participant_dict[contact_id] = participant
                attendance_dict[contact_id] = contact_dict["attendance_data"]


    validated_dict = dict(
        name=request_body["name"],
        event_type=type_enum,
        subjects=subject_list,
        date=date_obj,
        participants=participant_dict,
        attendance=attendance_dict
    )

    return validated_dict

@bp.route("", methods=["POST"], strict_slashes=False)
def create_event():
    request_body = request.get_json()

    event_data = validate_request_body(request_body)

    event_dict = dict(
        name=event_data["name"],
        event_type=event_data["event_type"],
        subjects=event_data["subjects"],
        date=event_data["date"]
    )

    new_event = Event.new_from_dict(event_dict)

    participant_dict = event_data.get("participants")
    attendance_dict = event_data.get("attendance")

    if participant_dict:
        for contact_id in participant_dict.keys():
            if attendance_dict:
                new_event_att = xEventAttendance.attach_extra_data(attendance_dict[contact_id])
            else:
                new_event_att = xEventAttendance(
                    attended=False, completed=False)
            new_event_att.participant = participant_dict[contact_id]
            new_event.participants.append(new_event_att)


    db.session.add(new_event)
    db.session.commit()

    return make_response(jsonify(new_event.to_dict()), 201)

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
def get_all_events():
    sort_query = request.args.get("sort")
    name_query = request.args.get("name")
    type_query = request.args.get("type")
    subject_query = request.args.get("subject")
    logical_or = request.args.get("OR")

    event_query = Event.query

    if logical_or:
        existing_query = False

        if name_query:
            event_query = event_query.filter(Event.name.ilike(f'%{name_query}%'))
            existing_query = True
        
        if type_query:
            type_enum = validate_type_enum(type_query)

            if existing_query:
                q_type = Event.query.filter_by(event_type=type_enum)
                event_query = event_query.union(q_type)
            else:
                event_query = event_query.filter_by(event_type=type_enum)
                existing_query = True

        if subject_query:
            subject_plus_split = find_and_operator(subject_query)

            if subject_plus_split:
                query_items = subject_query.split(subject_plus_split)
                for subject_id in query_items:
                    subject_enum = validate_subject_enum(subject_id)
                    item_query = Event.query.filter(Event.subjects.any(subject_enum))
                
                if existing_query:
                    event_query = event_query.union(item_query)
                else:
                    event_query = item_query

            elif subject_query.find("_") > -1:
                query_items = subject_query.split["_"]
                for subject_id in query_items:
                    subject_enum = validate_subject_enum(subject_id)
                    item_query = Event.query.filter(Event.subjects.any(subject_enum))
                    event_query = event_query.union(item_query)

            else:
                subject_enum = validate_subject_enum(subject_query)
                if existing_query:
                    q_subject = Event.query.filter(Event.subjects.any(subject_enum))
                    event_query = event_query.union(q_subject)
                else:
                    event_query = event_query.filter(Event.subjects.any(subject_enum))

    else:
        if name_query:
            event_query = event_query.filter(Event.name.ilike(f'%{name_query}%'))
        
        if type_query:
            type_enum = validate_type_enum(type_query)
            event_query = event_query.filter_by(event_type=type_enum)

        if subject_query:
            subject_plus_split = find_and_operator(subject_query)

            if subject_plus_split:
                query_items = subject_query.split(subject_plus_split)
                
                for subject_id in query_items:
                    subject_enum = validate_subject_enum(subject_id)
                    event_query = event_query.filter(Event.subjects.any(subject_enum))
            elif subject_query.find("_") > -1:
                query_items = subject_query.split("_")
                for subject_id in query_items:
                    subject_enum = validate_subject_enum(subject_id)
                    item_query = Event.query.filter(Event.subjects.any(subject_enum))
                    event_query = event_query.union(item_query)
            else:
                subject_enum = validate_subject_enum(subject_query)
                event_query = event_query.filter(Event.subjects.any(subject_enum))

    if sort_query:
        if sort_query == "desc":
            event_query = event_query.order_by(Event.name.desc())
        
        if sort_query == "date":
            event_query = event_query.order_by(Event.date, Event.name)
        elif sort_query == "date-desc":
            event_query = event_query.order_by(Event.date.desc(), Event.name)
    else:
        event_query = event_query.order_by(Event.name)

    events = event_query.all()

    if not events:
        return jsonify([])

    events_response = append_dicts_to_list(events)

    return jsonify(events_response)


@bp.route("/<uuid:id>", methods=["GET"], strict_slashes=False)
def get_event(id):
    event = validate_UUID(Event, id)
    return event.to_dict()


@bp.route("/<uuid:id>", methods=["PUT"])
def update_event(id):
    event = validate_UUID(Event, id)
    request_body = request.get_json()
    
    event_dict = validate_request_body(request_body)

    participant_query = xEventAttendance.query.filter_by(event_id=event.id).delete()
    db.session.commit()

    event.name = event_dict["name"]
    event.event_type = event_dict["event_type"]
    event.subjects = event_dict["subjects"]
    event.date = event_dict["date"]
    event.participants = []

    participant_dict = event_dict.get("participants")
    attendance_dict = event_dict.get("attendance")

    if participant_dict:
        for contact_id in participant_dict.keys():
            if attendance_dict:
                new_event_att = xEventAttendance.attach_extra_data(attendance_dict[contact_id])
            else:
                new_event_att = xEventAttendance(
                    attended=False, completed=False)
            new_event_att.participant = participant_dict[contact_id]
            event.participants.append(new_event_att)

    db.session.add(event)
    db.session.commit()

    return jsonify(event.to_dict())


@bp.route("/<uuid:id>", methods=["DELETE"])
def delete_event(id):
    event = validate_UUID(Event, id)
    db.session.delete(event)
    db.session.commit()
    return make_response({"message": f"Event '{event.name}' successfully deleted"}, 200)


# xEventAttendance nested routes start here

# @bp.route("/<uuid:id>/participants", methods=["GET"], strict_slashes=False)
# def get_event_participant_id_list(id):
#     event = validate_UUID(Event, id)

#     if event.participants:
#         participant_list = [ str(contact.id) for contact in event.participants ]
#     else:
#         participant_list = []
    
#     return jsonify(participant_list)


# @bp.route("/<uuid:id>/attendance", methods=["GET"], strict_slashes=False)
# def get_event_attendance_data(id):
#     event = validate_UUID(Event, id)

#     if not event.participants:
#         return jsonify(dict())
        
#     return jsonify(event.get_attendance_dict())


# @bp.route("/<uuid:id>/attendance", methods=["PUT"], strict_slashes=False)
# def update_event_attendance_data(id):
#     event = validate_UUID(Event, id)
#     request_body = request.get_json()

#     if not event.participants:
#         return jsonify(dict())

#     participant_ids = set([ str(contact.id) for contact in event.participants ])

#     for (contact_id, attendance_data) in request_body.items():
#         contact = validate_UUID(Contact, contact_id)
        
#         if contact_id not in participant_ids:
#             abort(make_response({"message": "Submitted participant not in event participant list"}, 400))

#         attendance_instance = xEventAttendance.query.filter(
#             xEventAttendance.event_id == id, xEventAttendance.participant_id == contact_id)
#         attendance_instance.attended = attendance_data["attendance"]
#         attendance_instance.completed = attendance_data["completion"]
        
#         db.session.add(attendance_instance)
#         db.session.commit()
        
#     return jsonify(event.get_attendance_dict())

# TODO: make org-contact association table using this pattern
# TODO: drop event_attendance association table
# TODO: reconstruct event_attendance using association object
# TODO: on FE side, remember to make an Advanced Search page with forms
# to allow users easy access to advanced search features, as well as maybe look for some of the flags