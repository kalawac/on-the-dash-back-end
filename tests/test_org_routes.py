import pytest
from werkzeug.exceptions import HTTPException
from app.models.org import Org
from app.models.contact import Contact
from app import db

def test_get_all_orgs_no_records(client):
    response = client.get("orgs")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_get_all_orgs_with_records(client, three_orgs):
    response = client.get("orgs")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["id"]
    assert response_body[1]["id"]
    assert response_body[2]["id"]
    assert response_body[2]["name"] == "Thriving"
    assert response_body[2]["sector"] == 7
    assert response_body[2]["foci"] == [1,4]
    assert response_body[1]["name"] == "Catch Me!"
    assert response_body[1]["sector"] == 2
    assert response_body[1]["foci"] == [2]
    assert response_body[0]["name"] == "Babies for Boomerangs"
    assert response_body[0]["sector"] == 2
    assert response_body[0]["foci"] == [1]


def test_get_all_orgs_sort_desc(client, three_orgs):
    queries = {'sort': 'desc'}
    response = client.get("orgs", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["name"] == "Thriving"
    assert response_body[1]["name"] == "Catch Me!"
    assert response_body[2]["name"] == "Babies for Boomerangs"


def test_get_all_orgs_filter_name(client, three_orgs):
    queries = {'name': 'me'}
    response = client.get("orgs", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] in ["Babies for Boomerangs", "Catch Me!"]
    assert response_body[1]["name"] in ["Babies for Boomerangs", "Catch Me!"]


def test_get_all_orgs_filter_sector(client, three_orgs):
    queries = {'sector': '2'}
    response = client.get("orgs", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] in ["Babies for Boomerangs", "Catch Me!"]
    assert response_body[1]["name"] in ["Babies for Boomerangs", "Catch Me!"]

# @pytest.mark.skip()
def test_get_all_orgs_filter_work_focus(client, three_orgs):
    queries = {'wf': '1'}
    response = client.get("orgs", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] in ["Babies for Boomerangs", "Thriving"]
    assert response_body[1]["name"] in ["Babies for Boomerangs", "Thriving"]

# @pytest.mark.skip()
def test_get_all_orgs_filter_work_foci_with_or(client, three_orgs):
    queries = {'wf': '1_2'}
    response = client.get("orgs", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["name"] == "Babies for Boomerangs"
    assert response_body[1]["name"] == "Catch Me!"
    assert response_body[2]["name"] == "Thriving"

# @pytest.mark.skip()
def test_get_all_orgs_filter_work_foci_with_and(client, three_orgs):
    queries = {'wf': '1+4'}
    response = client.get("orgs", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["name"] == "Thriving"


def test_get_all_orgs_combine_sort_filter(client, three_orgs):
    queries = {'sector': '2', 'sort': 'desc'}
    response = client.get("orgs", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["name"] == "Catch Me!"
    assert response_body[1]["name"] == "Babies for Boomerangs"


# @pytest.mark.skip()
def test_get_all_orgs_combine_filters_and(client, three_orgs):
    queries = {'sector': '2', 'wf': '2'}
    response = client.get("orgs", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["name"] == "Catch Me!"


# @pytest.mark.skip()
def test_get_all_orgs_combine_filters_or(client, three_orgs):
    queries = {'sector': '2', 'wf': '4', 'OR': True}
    response = client.get("orgs", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["name"] == "Babies for Boomerangs"
    assert response_body[1]["name"] == "Catch Me!"
    assert response_body[2]["name"] == "Thriving"


def test_get_one_org(client, one_org):
    org_query = Org.query.filter_by(name="Abacus Inc.").all()
    org_id = org_query[0].id
    test_url = "orgs/"+str(org_id)
    
    response = client.get(test_url)
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"]
    assert response_body["name"] == "Abacus Inc."
    assert response_body["sector"] == 5
    assert not response_body["foci"]
    # assert response_body["contacts"] == []


def test_get_one_org_id_not_present(client, three_orgs):
    response = client.get("orgs/9")
    response_body = response.get_json()

    assert response.status_code == 404

def test_get_one_org_invalid_id(client, three_orgs):
    response = client.get("orgs/Thriving")
    response_body = response.get_json()

    assert response.status_code == 404
    


def test_create_one_org(client):
    response = client.post("orgs", json = {
        "name": "Abacus Inc.",
        "sector": 5,
        "foci": []
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body["id"]
    assert response_body["name"] == "Abacus Inc."
    assert response_body["sector"] == 5
    assert not response_body["foci"]
    # assert response_body["contacts"] == []


def test_create_one_org_no_name_fails(client):
    response = client.post("orgs", json = {
        "naem": "Abacus Inc.",
        "sector": 5,
        "foci": []
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["message"] == "Organization requires a name"


def test_create_one_org_name_empty_string_fails(client):
    response = client.post("orgs", json = {
        "sector": 5,
        "foci": []
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["message"] == "Organization requires a name"


def test_update_org(client, three_orgs):
    org_query = Org.query.filter_by(name="Thriving").all()
    org_id = org_query[0].id
    test_url = "orgs/"+str(org_id)

    response = client.put(test_url, json = {
        "name": "Abacus Inc.",
        "sector": 5,
        "foci": []
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"] == str(org_id)
    assert response_body["name"] == "Abacus Inc."
    assert response_body["sector"] == 5
    assert not response_body["foci"]
    # assert response_body["contacts"] == []

# @pytest.mark.skip()
def test_update_org_with_wf(client, three_orgs):
    org_query = Org.query.filter_by(name="Thriving").all()
    org_id = org_query[0].id
    test_url = "orgs/"+str(org_id)

    response = client.put(test_url, json = {
        "name": "Abacus Inc.",
        "sector": 5,
        "foci": [1, 3, 99]
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"] == str(org_id)
    assert response_body["name"] == "Abacus Inc."
    assert response_body["sector"] == 5
    assert response_body["foci"] == [1,3,99]
    # assert response_body["contacts"] == []

@pytest.mark.skip()
def test_update_org_with_contacts(client, three_orgs, five_contacts):
    org_query = Org.query.filter_by(name="Thriving").all()
    org_id = org_query[0].id
    test_url = "orgs/"+str(org_id)

    contacts = Contact.query.all()
    contact_id_list = [contact.id for contact in contacts]

    response = client.put(test_url, json = {
        "name": "Abacus Inc.",
        "sector": 5,
        "foci": [1, 3, 5],
        "contact_ids": contact_id_list
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"] == str(org_id)
    assert response_body["name"] == "Abacus Inc."
    assert response_body["sector"] == 5
    assert response_body["foci"] == [1, 3, 5]
    assert len(response_body["contacts"]) == 5


def test_delete_org(client, three_orgs):
    org_query = Org.query.filter_by(name="Catch Me!").all()
    org_id = org_query[0].id
    test_url = "orgs/"+str(org_id)

    response = client.delete(test_url)
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["message"] == "Organization 'Catch Me!' successfully deleted"