import pytest
# from operator import itemgetter, attrgetter
from app import db
from app.models.contact import Contact
from app.models.org import Org
from app.models.types.work_focus import WF

# need routes to write models with relationships

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
        orgs=test_response["orgs"]
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
        "orgs": [],
        "events": [],
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
        "orgs": [],
        "events": [],
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


# @pytest.mark.skip()
def test_contact_repr(client):
    test_response = {
        "fname": "Agnes",
        "lname": "Chow",
        "age": 26,
        "gender": 1,
        "orgs": [],
        "events": [],
    }

    new_contact = Contact(
        fname=test_response["fname"],
        lname=test_response["lname"],
        age=test_response["age"],
        gender=test_response["gender"],
        orgs=test_response["orgs"]
        )

    db.session.add(new_contact)
    db.session.commit()

    result = f'{new_contact} is from Hong Kong'

    assert result == "<Contact 'Agnes Chow'> is from Hong Kong"


# @pytest.mark.skip()
def test_create_org_no_work_focus(client):
    test_response = {
            "name": "Babies for Boomerangs",
            "sector": 2,
            "foci": None
            }

    result = Org(
        name=test_response["name"],
        org_sector=test_response["sector"],
        )

    db.session.add(result)
    db.session.commit()

    assert result.id
    assert result.name == "Babies for Boomerangs"
    assert result.org_sector == 2
    assert not result.foci


# @pytest.mark.skip()
def test_create_org_from_dict_empty_work_focus(client):
    test_response = {
            "name": "Babies for Boomerangs",
            "org_sector": 2,
            "foci": []
            }

    result = Org.new_from_dict(test_response)

    db.session.add(result)
    db.session.commit()

    assert result.id
    assert result.name == "Babies for Boomerangs"
    assert result.org_sector == 2
    assert not result.foci


# @pytest.mark.skip()
def test_create_org_from_dict_one_work_focus(client):
    test_response = {
            "name": "Babies for Boomerangs",
            "org_sector": 2,
            "foci": [1]
            }

    result = Org.new_from_dict(test_response)

    db.session.add(result)
    db.session.commit()

    assert result.id
    assert result.name == "Babies for Boomerangs"
    assert result.org_sector == 2
    assert result.foci == [1]


# @pytest.mark.skip()
def test_create_org_from_dict_work_foci(client):
    test_response = {
            "name": "Babies for Boomerangs",
            "org_sector": 2,
            "foci": [1,2,3]
            }

    result = Org.new_from_dict(test_response)

    db.session.add(result)
    db.session.commit()

    assert result.id
    assert result.name == "Babies for Boomerangs"
    assert result.org_sector == 2
    assert result.foci == [1,2,3]