import pytest
from werkzeug.exceptions import HTTPException
from app import db

def test_get_all_contacts_no_records(client):
    response = client.get("contacts")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_contacts_with_records(client, three_contacts_with_orgs_events):
    response = client.get("contacts")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["id"]
    assert response_body[1]["id"]
    assert response_body[2]["id"]
    assert response_body[3]["id"]
    assert response_body[4]["id"]
    assert response_body[0]["fname"] == "Nemonte"
    assert response_body[0]["lname"] == "Nenquimo"
    assert response_body[0]["age"] == 37
    assert response_body[0]["gender"] == 1
    assert response_body[0]["orgs"] == [1]
    assert response_body[0]["events"] == []
    assert response_body[1]["fname"] == "Kate"
    assert response_body[1]["lname"] == "Dylan"
    assert response_body[1]["age"] == 38
    assert response_body[1]["gender"] == 3
    assert response_body[1]["orgs"] == []
    assert response_body[1]["events"]
    assert response_body[2]["fname"] == "Nat"
    assert response_body[2]["lname"] == "Bentley"
    assert response_body[2]["age"] == 26
    assert response_body[2]["gender"] == 2
    assert response_body[2]["orgs"] == [2, 3]
    assert response_body[2]["events"]

def test_get_one_contact(client, one_contact):
    response = client.get("contacts/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"]
    assert response_body[0]["fname"] == "Nemonte"
    assert response_body[0]["lname"] == "Nenquimo"
    assert response_body[0]["age"] == 37
    assert response_body[0]["gender"] == 1
    assert response_body[0]["orgs"] == []
    assert response_body[0]["events"] == []


def test_get_one_contact_id_not_present(client, five_contacts):
    response = client.get("contacts/9")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Contact 9 not found"}

def test_get_one_contact_invalid_id(client, five_contacts):
    response = client.get("contacts/agnes")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": "Contact agnes invalid"}
    


def test_create_one_contact(client):
    response = client.post("contacts", json = {
        "fname": "Agnes",
        "lname": "Chow",
        "age": 26,
        "gender": 1,
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body["id"]
    assert response_body["fname"] == "Agnes"
    assert response_body["lname"] == "Chow"
    assert response_body["age"] == 26
    assert response_body["gender"] == 1
    assert response_body["orgs"] == []
    assert response_body["events"] == []


def test_update_contacts_label(client, five_contacts):
    contact_query = Contact.query.filter_by(fname="Mary").all()
    contact_id = contact_query.id

    response = client.put("contacts/{contact_id}", json = {
        "fname": "Robert",
        "lname": "Winthrop",
        "age": 42,
        "gender": 3,
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"]
    assert response_body[0]["fname"] == "Robert"
    assert response_body[0]["lname"] == "Winthrop"
    assert response_body[0]["age"] == 42
    assert response_body[0]["gender"] == 3
    assert response_body[0]["orgs"] == []
    assert response_body[0]["events"] == []


def test_delete_contacts(client, five_contacts):
    response = client.delete("contacts/3")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["message"] == 'Contact 3 Nat Bentley successfully deleted'