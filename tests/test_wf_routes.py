import pytest
from werkzeug.exceptions import HTTPException
from app import db
from app.models.work_focus import WorkFocus

def test_get_all_wf_no_records(client):
    response = client.get("wf")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_all_wf_with_records(client, initial_work_foci):
    response = client.get("wf")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 5
    assert response_body[0]["id"] == 1
    assert response_body[1]["id"] == 2
    assert response_body[2]["id"] == 3
    assert response_body[3]["id"] == 4
    assert response_body[4]["id"] == 5
    assert response_body[0]["label"] == "INDIGENOUS"
    assert response_body[1]["label"] == "LGBTI"
    assert response_body[2]["label"] == "RELIGIOUS_FREEDOM"
    assert response_body[3]["label"] == "WOMENS_RIGHTS"
    assert response_body[4]["label"] == "OTHER"

def test_get_one_wf(client, initial_work_foci):
    response = client.get("wf/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"] == 1
    assert response_body["label"] == "INDIGENOUS"


def test_get_one_wf_id_not_present(client, initial_work_foci):
    response = client.get("wf/9")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "WorkFocus 9 not found"}

def test_get_one_wf_invalid_id(client, initial_work_foci):
    response = client.get("wf/lgbti")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": "WorkFocus lgbti invalid"}
    


def test_create_one_wf(client):
    response = client.post("wf", json = {
        "label": "Youth",
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body["id"] == 1
    assert response_body["label"] == "Youth"


def test_update_wf_label(client, initial_work_foci):
    response = client.patch("wf/5", json = {
        "label": "Youth",
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"] == 5
    assert response_body["label"] == "Youth"


def test_delete_wf(client, initial_work_foci):
    response = client.delete("wf/3")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["message"] == '<WorkFocus.RELIGIOUS_FREEDOM: 3> deleted'