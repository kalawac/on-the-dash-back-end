import pytest
# from operator import itemgetter, attrgetter
from app import db
from app.models.contact import Contact
from app.models.org import Org


def test_create_contact_no_orgs_no_events(client):
    test_response = {
        "fname": "Mary",
        "lname": "Seacole",
        "age": 52,
        "gender": 1,
        "orgs": [],
        "events": [],
    }

    result = Contact(
        fname=test_response["fname"],
        lname=test_response["lname"],
        age=test_response["age"],
        gender=test_response["gender"],
        )

    db.session.add(result)
    db.session.commit()

    assert result.id
    assert result.fname == "Mary"
    assert result.lname == "Seacole"
    assert result.age == 52
    assert result.gender == 1

# @pytest.mark.skip()
def test_contact_from_dict_no_orgs_no_events(client):
    test_response = {
    "fname": "Mary",
    "lname": "Seacole",
    "age": 52,
    "gender": 1,
    "orgs": [],
    "events": [],
    }

    result = Contact.new_from_dict(test_response)

    db.session.add(result)
    db.session.commit()

    assert result.fname == "Mary"
    assert result.lname == "Seacole"
    assert result.age == 52
    assert result.gender == 1

@pytest.mark.skip()
def test_create_contact_no_lname_raises_error(client):
    test_response = {
        "fname": "Agnes",
        "age": 26,
        "gender": 1,
    }

    result = Contact(
    fname=test_response["fname"],
    age=test_response["age"],
    gender=test_response["gender"],
    )

    with pytest.raises():
        db.session.add(result)
        db.session.commit()

# @pytest.mark.skip()
def test_contact_from_dict_no_lname_raises_error(client):
    test_response = {
        "fname": "Agnes",
        "age": 26,
        "gender": 1,
    }

    with pytest.raises(KeyError, match = "lname"):
        result = Contact.new_from_dict(test_response)

# @pytest.mark.skip()
def test_contact_to_dict_no_orgs_no_events(client):
    test_response = {
        "fname": "Agnes",
        "lname": "Chow",
        "age": 26,
        "gender": 1,
    }

    new_contact = Contact.new_from_dict(test_response)

    db.session.add(new_contact)
    db.session.commit()

    result = new_contact.to_dict()

    assert len(result) == 7
    assert result["fname"] == "Agnes"
    assert result["lname"] == "Chow"
    assert result["age"] == 26
    assert result["gender"] == 1
    assert result["orgs"] == []
    assert result["events"] == []


def test_contact_repr(client):
    test_response = {
        "fname": "Agnes",
        "lname": "Chow",
        "age": 26,
        "gender": 1,
    }

    new_contact = Contact(
        fname=test_response["fname"],
        lname=test_response["lname"],
        age=test_response["age"],
        gender=test_response["gender"],
        )

    db.session.add(new_contact)
    db.session.commit()

    result = f'{new_contact} is from Hong Kong'

    assert result == "<Contact 'Agnes Chow'> is from Hong Kong"

def test_create_org(client):
    work_focus = WF(4)

    test_response = {
        "name": "Org 1",
        "sector": 2,
        "focus": (work_focus,),
    }

    result = Org.new_from_dict(test_response)

    db.session.add(result)
    db.session.commit()

    assert result.id