import pytest
from werkzeug.exceptions import HTTPException
from app import db

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


def test_get_all_wf_sort_desc(client, initial_work_foci):
    queries = {'sort': 'desc'}
    response = client.get("wf", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 5
    assert response_body[0]["id"] == 5
    assert response_body[1]["id"] == 4
    assert response_body[2]["id"] == 3
    assert response_body[3]["id"] == 2
    assert response_body[4]["id"] == 1
    assert response_body[0]["label"] == "OTHER"
    assert response_body[1]["label"] == "WOMENS_RIGHTS"
    assert response_body[2]["label"] == "RELIGIOUS_FREEDOM"
    assert response_body[3]["label"] == "LGBTI"
    assert response_body[4]["label"] == "INDIGENOUS"


def test_get_all_wf_sort_label(client, initial_work_foci):
    queries = {'sort': 'label'}
    response = client.get("wf", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 5
    assert response_body[0]["id"] == 1
    assert response_body[1]["id"] == 2
    assert response_body[2]["id"] == 5
    assert response_body[3]["id"] == 3
    assert response_body[4]["id"] == 4
    assert response_body[0]["label"] == "INDIGENOUS"
    assert response_body[1]["label"] == "LGBTI"
    assert response_body[2]["label"] == "OTHER"
    assert response_body[3]["label"] == "RELIGIOUS_FREEDOM"
    assert response_body[4]["label"] == "WOMENS_RIGHTS"


def test_get_all_wf_sort_label_desc(client, initial_work_foci):
    queries = {'sort': 'label-desc'}
    response = client.get("wf", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 5
    assert response_body[4]["id"] == 1
    assert response_body[3]["id"] == 2
    assert response_body[2]["id"] == 5
    assert response_body[1]["id"] == 3
    assert response_body[0]["id"] == 4
    assert response_body[4]["label"] == "INDIGENOUS"
    assert response_body[3]["label"] == "LGBTI"
    assert response_body[2]["label"] == "OTHER"
    assert response_body[1]["label"] == "RELIGIOUS_FREEDOM"
    assert response_body[0]["label"] == "WOMENS_RIGHTS"


def test_get_all_wf_filter_label(client, initial_work_foci):
    queries = {'label': 'OM'}
    response = client.get("wf", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["id"] == 3
    assert response_body[0]["label"] == "RELIGIOUS_FREEDOM"
    assert response_body[1]["id"] == 4
    assert response_body[1]["label"] == "WOMENS_RIGHTS"


def test_get_all_wf_filter_id(client, initial_work_foci):
    queries = {'id': '4'}
    response = client.get("wf", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["id"] == 4
    assert response_body[0]["label"] == "WOMENS_RIGHTS"


def test_get_all_wf_combine_sort_filter_label(client, initial_work_foci):
    queries = {'sort': 'desc', 'label': 'OM'}
    response = client.get("wf", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[1]["id"] == 3
    assert response_body[1]["label"] == "RELIGIOUS_FREEDOM"
    assert response_body[0]["id"] == 4
    assert response_body[0]["label"] == "WOMENS_RIGHTS"


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


def test_create_one_wf_no_label_fails(client):
    response = client.post("wf", json = {
        "lable": "Youth",
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["message"] == "WorkFocus item requires label"


def test_create_one_wf_label_empty_string_fails(client):
    response = client.post("wf", json = {
        "label": "",
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["message"] == "WorkFocus item requires label"


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
    assert response_body["message"] == "<WorkFocus.RELIGIOUS_FREEDOM: 3> successfully deleted"