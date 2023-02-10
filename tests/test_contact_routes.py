import pytest
from werkzeug.exceptions import HTTPException
from app import db

def test_get_all_contacts_no_records(client):
    response = client.get("contacts")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

# write route to sort on lname by default
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
    assert response_body[2]["events"] == []
    assert response_body[1]["fname"] == "Kate"
    assert response_body[1]["lname"] == "Dylan"
    assert response_body[1]["age"] == 38
    assert response_body[1]["gender"] == 3
    assert response_body[1]["orgs"] == []
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


@pytest.mark.skip() # sorting lname by default, so this is unnecessary
def test_get_all_contacts_sort_lname(client, five_contacts):
    queries = {'sort': 'lname'}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 5
    assert response_body[0]["lname"] == "Bentley"
    assert response_body[1]["lname"] == "Chow"
    assert response_body[2]["lname"] == "Dylan"
    assert response_body[3]["lname"] == "Nenquimo"
    assert response_body[4]["lname"] == "Seacole"


def test_get_all_contacts_sort_lname_desc(client, five_contacts):
    queries = {'sort': 'lname-desc'}
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
    assert response_body[0]["lname"] == "Bentley"
    assert response_body[1]["lname"] == "Nenquimo"


def test_get_all_contacts_filter_fname(client, five_contacts):
    queries = {'fname': 'ne'}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["fname"] == "Agnes"
    assert response_body[1]["fname"] == "Nemonte"


def test_get_all_contacts_filter_lname(client, five_contacts):
    queries = {'lname': 'le'}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["lname"] == "Bentley"
    assert response_body[1]["lname"] == "Seacole"


def test_get_all_contacts_filter_gender(client, four_contacts_with_orgs_events):
    queries = {'gender': '1'}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["lname"] == "Nenquimo"
    assert response_body[1]["lname"] == "Seacole"


def test_get_all_contacts_filter_single_org(client, four_contacts_with_orgs_events):
    queries = {'org': '3'}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["lname"] == "Bentley"
    assert response_body[1]["lname"] == "Seacole"


def test_get_all_contacts_filter_multiple_orgs_with_or(client, four_contacts_with_orgs_events):
    queries = {'org': '3+1'}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body[0]["lname"] == "Bentley"
    assert response_body[1]["lname"] == "Nenquimo"
    assert response_body[2]["lname"] == "Seacole"


def test_get_all_contacts_filter_multiple_orgs_with_and(client, four_contacts_with_orgs_events):
    queries = {'org': '2+3', 'lo': 'and'}
    response = client.get("contacts", query_string=queries)
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["lname"] == "Bentley"


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