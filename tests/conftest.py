import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.contact import Contact
from app.models.org import Org
from app.models.work_focus import WorkFocus


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def one_contact(client):
    contact_dict = {
        "fname": "Nemonte",
        "lname": "Nenquimo",
        "age": 37,
        "gender": 1,
    }

    new_contact = Contact.new_from_dict(contact_dict)
    
    db.session.add(new_contact)
    db.session.commit()


@pytest.fixture
def five_contacts(client):
    contact1 = Contact.new_from_dict({
        "fname": "Nemonte",
        "lname": "Nenquimo",
        "age": 37,
        "gender": 1,
    })

    contact2 = Contact.new_from_dict({
        "fname": "Kate",
        "lname": "Dylan",
        "age": 38,
        "gender": 3,
    })

    contact3 = Contact.new_from_dict({
        "fname": "Nat",
        "lname": "Bentley",
        "age": 26,
        "gender": 2,
    })

    contact4 = Contact.new_from_dict({
        "fname": "Agnes",
        "lname": "Chow",
        "age": 26,
        "gender": 1,
    })

    contact5 = Contact.new_from_dict({
        "fname": "Mary",
        "lname": "Seacole",
        "age": 52,
        "gender": 1,
    })

    db.session.add_all([contact1, contact2, contact3])
    db.session.commit()


@pytest.fixture
def one_org(client):
    org_dict = {
        "name": "Abacus Inc.",
        "sector": 5,
    }

    new_org = Org.new_from_dict(org_dict)
    
    db.session.add(new_org)
    db.session.commit()


@pytest.fixture
def three_orgs(client):
    db.session.add_all([
        Org.new_from_dict({
            "name": "Babies for Boomerangs",
            "sector": 2,
            }),
        Org.new_from_dict({
            "name": "Catch Me!",
            "sector": 2,
            }),
        Org.new_from_dict({
            "name": "Thriving",
            "sector": 7,
            }),
    ])
    db.session.commit()


@pytest.fixture
def initial_work_foci(client):
    
    wf1 = WorkFocus(label='INDIGENOUS')
    wf2 = WorkFocus(label='LGBTI')
    wf3 = WorkFocus(label='RELIGIOUS_FREEDOM')
    wf4 = WorkFocus(label='WOMENS_RIGHTS')
    wf5 = WorkFocus(label='OTHER')
    
    db.session.add_all([wf1, wf2, wf3, wf4, wf5])
    db.session.commit()