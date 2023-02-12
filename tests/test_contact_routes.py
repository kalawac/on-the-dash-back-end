import pytest
from werkzeug.exceptions import HTTPException
from app.models.contact import Contact
from app import db
import uuid

def test_get_all_contacts_no_records(client):
    response = client.get("contacts")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


@pytest.mark.skip()
def test_get_all_contacts_with_records(client, four_contacts_with_orgs_events):
    response = client.get("contacts")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 4
    assert response_body[0]["id"]
    assert response_body[1]["id"]
    assert response_body[2]["id"]
    assert response_body[3]["id"]
    assert response_body[2]["fname"] == "Nemonte"
    assert response_body[2]["lname"] == "Nenquimo"
    assert response_body[2]["age"] == 37
    assert response_body[2]["gender"] == 1
    assert response_body[2]["orgs"] == [1]
    assert not response_body[2]["events"]
    assert response_body[1]["fname"] == "Kate"
    assert response_body[1]["lname"] == "Dylan"
    assert response_body[1]["age"] == 38
    assert response_body[1]["gender"] == 3
    assert not response_body[1]["orgs"]
    assert response_body[1]["events"]
    assert response_body[0]["fname"] == "Nat"
    assert response_body[0]["lname"] == "Bentley"
    assert response_body[0]["age"] == 26
    assert response_body[0]["gender"] == 2
    assert response_body[0]["orgs"] == [2, 3]
    assert response_body[0]["events"]


def test_get_all_contacts_sort_fname(client, five_contacts):
    queries = {'sort': 'fname'}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 5
    assert response_body[0]["fname"] == "Agnes"
    assert response_body[1]["fname"] == "Kate"
    assert response_body[2]["fname"] == "Mary"
    assert response_body[3]["fname"] == "Nat"
    assert response_body[4]["fname"] == "Nemonte"


def test_get_all_contacts_sort_fname_desc(client, five_contacts):
    queries = {'sort': 'fname-desc'}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 5
    assert response_body[4]["fname"] == "Agnes"
    assert response_body[3]["fname"] == "Kate"
    assert response_body[2]["fname"] == "Mary"
    assert response_body[1]["fname"] == "Nat"
    assert response_body[0]["fname"] == "Nemonte"


def test_get_all_contacts_sort_lname_desc(client, five_contacts):
    queries = {'sort': 'desc'}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 5
    assert response_body[4]["lname"] == "Bentley"
    assert response_body[3]["lname"] == "Chow"
    assert response_body[2]["lname"] == "Dylan"
    assert response_body[1]["lname"] == "Nenquimo"
    assert response_body[0]["lname"] == "Seacole"



def test_get_all_contacts_filter_name(client, five_contacts):
    queries = {'name': 'nt'}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["lname"] in ["Bentley", "Nenquimo"]
    assert response_body[1]["lname"] in ["Bentley", "Nenquimo"]


def test_get_all_contacts_filter_fname(client, five_contacts):
    queries = {'fname': 'ne'}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["fname"] in ["Agnes", "Nemonte"]
    assert response_body[1]["fname"] in ["Agnes", "Nemonte"]


def test_get_all_contacts_filter_lname(client, five_contacts):
    queries = {'lname': 'le'}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["lname"] == "Bentley"
    assert response_body[1]["lname"] == "Seacole"


@pytest.mark.skip()
def test_get_all_contacts_filter_gender(client, four_contacts_with_orgs_events):
    queries = {'gender': '1'}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["lname"] == "Nenquimo"
    assert response_body[1]["lname"] == "Seacole"

# this is going to be painful to test without knowing the uuids
@pytest.mark.skip()
def test_get_all_contacts_filter_single_org(client, four_contacts_with_orgs_events):
    queries = {'org': '3'} # uuid, not 3!
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["lname"] == "Bentley"
    assert response_body[1]["lname"] == "Seacole"


@pytest.mark.skip()
def test_get_all_contacts_filter_multiple_orgs_with_or(client, four_contacts_with_orgs_events):
    queries = {'org': '3_1'} # convert to uuids
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["lname"] == "Bentley"
    assert response_body[1]["lname"] == "Nenquimo"
    assert response_body[2]["lname"] == "Seacole"


@pytest.mark.skip()
def test_get_all_contacts_filter_multiple_orgs_with_and(client, four_contacts_with_orgs_events):
    queries = {'org': '2+3'} # convert to uuids
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["lname"] == "Bentley"


# working with sort and lname
@pytest.mark.skip()
def test_get_all_contacts_combine_sort_filter(client, four_contacts_with_orgs_events):
    queries = {'org': '3+1', 'sort': 'fname'} # convert to uuids
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["fname"] == "Mary"
    assert response_body[1]["fname"] == "Nat"
    assert response_body[2]["fname"] == "Nemonte"


@pytest.mark.skip()
def test_get_all_contacts_combine_filters_and(client, four_contacts_with_orgs_events):
    queries = {'lname': 'le', 'gender': '1'}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["lname"] == "Seacole"


@pytest.mark.skip()
def test_get_all_contacts_combine_filters_or(client, four_contacts_with_orgs_events):
    queries = {'lname': 'le', 'gender': '1', 'OR': True}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["lname"] == "Bentley"
    assert response_body[1]["lname"] == "Nenquimo"
    assert response_body[2]["lname"] == "Seacole"


def test_get_one_contact(client, one_contact):
    contact_query = Contact.query.filter_by(fname="Nemonte").all()
    contact_id = contact_query[0].id
    test_url = "contacts/"+str(contact_id)
    
    response = client.get(test_url)
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"]
    assert response_body["fname"] == "Nemonte"
    assert response_body["lname"] == "Nenquimo"
    assert response_body["age"] == 37
    assert response_body["gender"] == 1
    assert response_body["orgs"] == []
    assert response_body["events"] == []


def test_get_one_contact_id_not_uuid(client, five_contacts):
    response = client.get("contacts/9")
    response_body = response.get_json()

    assert response.status_code == 404


def test_get_one_contact_uuid_id_not_present(client, one_contact):
    random_uuid = uuid.uuid4()

    contact_query = Contact.query.all()
    contact_id = contact_query[0].id

    if contact_id == random_uuid:
        random_uuid = uuid.uuid4()

    test_url = "contacts/"+str(random_uuid)

    response = client.get(test_url)
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body["message"] == f"Contact with id {random_uuid} not found"


def test_get_one_contact_invalid_id(client, five_contacts):
    response = client.get("contacts/agnes")
    response_body = response.get_json()

    assert response.status_code == 404
    


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
    assert not response_body["orgs"]
    assert not response_body["events"]


def test_create_one_contact_no_lname_fails(client):
    response = client.post("contacts", json = {
        "fname": "Agnes",
        "age": 26,
        "gender": 1,
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["message"] == "Contact requires last name"


def test_create_one_contact_lname_empty_string_fails(client):
    response = client.post("contacts", json = {
        "fname": "Agnes",
        "lname": "",
        "age": 26,
        "gender": 1,
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["message"] == "Contact requires last name"


def test_update_contact(client, five_contacts):
    contact_query = Contact.query.filter_by(fname="Mary").all()
    contact_id = contact_query[0].id
    test_url = "contacts/"+str(contact_id)

    response = client.put(test_url, json = {
        "fname": "Robert",
        "lname": "Winthrop",
        "age": 42,
        "gender": 3,
    })
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["id"] == str(contact_id)
    assert response_body["fname"] == "Robert"
    assert response_body["lname"] == "Winthrop"
    assert response_body["age"] == 42
    assert response_body["gender"] == 3
    assert not response_body["orgs"]
    assert not response_body["events"]


def test_delete_contact(client, five_contacts):
    contact_query = Contact.query.filter_by(fname="Nat").all()
    contact_id = contact_query[0].id
    test_url = "contacts/"+str(contact_id)

    response = client.delete(test_url)
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["message"] == 'Contact Nat Bentley successfully deleted'