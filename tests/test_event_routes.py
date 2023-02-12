import pytest
from werkzeug.exceptions import HTTPException
from app.models.event import Event
from app.models.contact import Contact
from app import db
import uuid
from datetime import date

def test_get_all_events_no_records(client):
    response = client.get("events")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_get_all_events_with_records(client, three_events):
    response = client.get("events")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["id"]
    assert response_body[1]["id"]
    assert response_body[2]["id"]
    assert response_body[0]["name"] == "How to Restart Time"
    assert response_body[0]["type"] == 4
    assert response_body[0]["subjects"] == [2]
    assert (date.fromisoformat(response_body[0]["date"]) == 
        date.fromisoformat("2021-12-21"))
    assert response_body[1]["name"] == "How to Stop Time"
    assert response_body[1]["type"] == 4
    assert response_body[1]["subjects"] == [1, 3, 9]
    assert (date.fromisoformat(response_body[1]["date"]) == 
        date.fromisoformat("2021-12-21"))
    assert response_body[2]["name"] == "Time Manipulation Support"
    assert response_body[2]["type"] == 3
    assert response_body[2]["subjects"] == [1,99]
    assert (date.fromisoformat(response_body[2]["date"]) == 
        date.fromisoformat("2023-02-10"))


def test_get_all_events_sort_desc(client, three_events):
    queries = {'sort': 'desc'}
    response = client.get("events", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["name"] == "Time Manipulation Support"
    assert response_body[1]["name"] == "How to Stop Time"
    assert response_body[2]["name"] == "How to Restart Time"


def test_get_all_events_sort_date(client, three_events):
    queries = {'sort': 'date'}
    response = client.get("events", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["name"] == "How to Stop Time"
    assert response_body[1]["name"] == "How to Restart Time"
    assert response_body[2]["name"] == "Time Manipulation Support"


def test_get_all_events_sort_date_desc(client, three_events):
    queries = {'sort': 'date-desc'}
    response = client.get("events", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[2]["name"] == "How to Stop Time"
    assert response_body[1]["name"] == "How to Restart Time"
    assert response_body[0]["name"] == "Time Manipulation Support"


def test_get_all_events_filter_name(client, three_events):
    queries = {'name': 'st'}
    response = client.get("events", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] in ["How to Stop Time", "How to Restart Time"]
    assert response_body[1]["name"] in ["How to Stop Time", "How to Restart Time"]


def test_get_all_events_filter_type(client, three_events):
    queries = {'type': '4'}
    response = client.get("events", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] in ["How to Stop Time", "How to Restart Time"]
    assert response_body[1]["name"] in ["How to Stop Time", "How to Restart Time"]

# @pytest.mark.skip()
def test_get_all_events_filter_subject(client, three_events):
    queries = {'subject': '1'}
    response = client.get("events", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] in ["How to Stop Time", "Time Manipulation Support"]
    assert response_body[1]["name"] in ["How to Stop Time", "Time Manipulation Support"]

# @pytest.mark.skip()
def test_get_all_events_filter_subjects_with_or(client, three_events):
    queries = {'subject': '99_2'}
    response = client.get("events", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[1]["name"] in ["How to Restart Time", "Time Manipulation Support"]
    assert response_body[2]["name"] in ["How to Restart Time", "Time Manipulation Support"]

# @pytest.mark.skip()
def test_get_all_events_filter_subjects_with_and(client, three_events):
    queries = {'subject': '1+9'}
    response = client.get("events", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["name"] == "How to Stop Time"


def test_get_all_events_combine_sort_filter(client, three_events):
    queries = {'type': '4', 'sort': 'desc'}
    response = client.get("events", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == "How to Stop Time"
    assert response_body[1]["name"] == "How to Restart Time"


# @pytest.mark.skip()
def test_get_all_events_combine_filters_and(client, three_events):
    queries = {'type': '2', 'subject': '2'}
    response = client.get("events", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["name"] == "How to Restart Time"


# @pytest.mark.skip()
def test_get_all_events_combine_filters_or(client, three_events):
    queries = {'type': '4', 'subject': '99', 'OR': True}
    response = client.get("events", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["name"] == "How to Restart Time"
    assert response_body[1]["name"] == "How to Stop Time"
    assert response_body[2]["name"] == "Time Manipulation Support"


def test_get_one_event(client, one_event):
    event_query = Event.query.filter_by(name="How to Stop Time").all()
    event_id = event_query[0].id
    test_url = "events/"+str(event_id)
    
    response = client.get(test_url)
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"]
    assert response_body["name"] == "How to Stop Time"
    assert response_body["type"] == 4
    assert response_body["subjects"] == [1, 3, 9]
    assert (date.fromisoformat(response_body["date"]) == 
        date.fromisoformat("2021-12-21"))


def test_get_one_event_id_not_uuid(client, three_events):
    response = client.get("events/9")
    response_body = response.get_json()

    assert response.status_code == 404


def test_get_one_event_uuid_id_not_present(client, one_event):
    random_uuid = uuid.uuid4()

    event_query = Event.query.all()
    event_id = event_query[0].id

    if event_id == random_uuid:
        random_uuid = uuid.uuid4()

    test_url = "events/"+str(random_uuid)

    response = client.get(test_url)
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body["message"] == f"Event with id {random_uuid} not found"


def test_get_one_event_invalid_id(client, three_events):
    response = client.get("events/Time Manipulation Support")
    response_body = response.get_json()

    assert response.status_code == 404


def test_create_one_event(client):
    response = client.post("events", json = {
        "name": "How to Stop Time",
        "type": 4,
        "subjects": [],
        "date": "2021-12-21"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body["id"]
    assert response_body["name"] == "How to Stop Time"
    assert response_body["type"] == 4
    assert not response_body["subjects"]
    assert (date.fromisoformat(response_body["date"]) == 
        date.fromisoformat("2021-12-21"))


def test_create_one_event_no_name_fails(client):
    response = client.post("events", json = {
        "naem": "How to Stop Time",
        "type": 4,
        "subjects": [],
        "date": "2021-12-21"
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["message"] == "Event requires a name"


def test_create_one_event_name_empty_string_fails(client):
    response = client.post("events", json = {
        "type": 4,
        "subjects": [],
        "date": "2021-12-21"
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["message"] == "Event requires a name"


def test_update_event(client, three_events):
    event_query = Event.query.filter_by(name="Time Manipulation Support").all()
    event_id = event_query[0].id
    test_url = "events/"+str(event_id)

    response = client.put(test_url, json = {
        "name": "Time Stopping Techniques",
        "type": 1,
        "subjects": [],
        "date": "2022-03-18"
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"] == str(event_id)
    assert response_body["name"] == "Time Stopping Techniques"
    assert response_body["type"] == 1
    assert not response_body["subjects"]
    assert (date.fromisoformat(response_body["date"]) == 
        date.fromisoformat("2022-03-18"))

# @pytest.mark.skip()
def test_update_event_with_subject(client, three_events):
    event_query = Event.query.filter_by(name="Time Manipulation Support").all()
    event_id = event_query[0].id
    test_url = "events/"+str(event_id)

    response = client.put(test_url, json = {
        "name": "Time Stopping Techniques",
        "type": 1,
        "subjects": [2, 7],
        "date": "2022-03-18"
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"] == str(event_id)
    assert response_body["name"] == "Time Stopping Techniques"
    assert response_body["type"] == 1
    assert response_body["subjects"] == [2, 7]
    assert response_body["date"] == "2022-03-18"
    assert (date.fromisoformat(response_body["date"]) == 
        date.fromisoformat("2022-03-18"))


@pytest.mark.skip()
def test_update_event_with_contacts(client, three_events, five_contacts):
    event_query = Event.query.filter_by(name="Time Manipulation Support").all()
    event_id = event_query[0].id
    test_url = "events/"+str(event_id)

    contacts = Contact.query.all()
    contact_id_list = [contact.id for contact in contacts]

    response = client.put(test_url, json = {
        "name": "How to Stop Time",
        "type": 4,
        "subjects": [1, 3, 4],
        "participants": contact_id_list
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"] == str(event_id)
    assert response_body["name"] == "How to Stop Time"
    assert response_body["type"] == 4
    assert response_body["subjects"] == [1, 3, 4]
    assert len(response_body["participants"]) == 5


def test_delete_event(client, three_events):
    event_query = Event.query.filter_by(name="How to Restart Time").all()
    event_id = event_query[0].id
    test_url = "events/"+str(event_id)

    response = client.delete(test_url)
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["message"] == "Event 'How to Restart Time' successfully deleted"