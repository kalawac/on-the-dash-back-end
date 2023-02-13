from flask.signals import request_finished
import pytest

from app import create_app
from app import db
from app.models.contact import Contact
from app.models.org import Org
from app.models.event import Event
from app.routes.contact_routes import validate_request_body as validate_contact
from app.routes.org_routes import validate_request_body as validate_org
from app.routes.event_routes import validate_request_body as validate_event
# from app.models.event_attendance import xEventAttendance


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
    contact_dict = validate_contact({
        "fname": "Nemonte",
        "lname": "Nenquimo",
        "age": 37,
        "gender": 1,
    })

    new_contact = Contact.new_from_dict(contact_dict)
    
    db.session.add(new_contact)
    db.session.commit()


@pytest.fixture
def five_contacts(client):
    contact1 = Contact.new_from_dict(validate_contact({
        "fname": "Nemonte",
        "lname": "Nenquimo",
        "age": 37,
        "gender": 1,
    }))

    contact2 = Contact.new_from_dict(validate_contact({
        "fname": "Kate",
        "lname": "Dylan",
        "age": 38,
        "gender": 3,
    }))

    contact3 = Contact.new_from_dict(validate_contact({
        "fname": "Nat",
        "lname": "Bentley",
        "age": 26,
        "gender": 2,
    }))

    contact4 = Contact.new_from_dict(validate_contact({
        "fname": "Agnes",
        "lname": "Chow",
        "age": 26,
        "gender": 1,
    }))

    contact5 = Contact.new_from_dict(validate_contact({
        "fname": "Mary",
        "lname": "Seacole",
        "age": 52,
        "gender": 1,
    }))

    db.session.add_all([contact1, contact2, contact3, contact4, contact5])
    db.session.commit()


@pytest.fixture
def one_org(client):
    org_dict = validate_org({
        "name": "Abacus Inc.",
        "sector": 5,
        "foci": []
    })

    new_org = Org.new_from_dict(org_dict)
    
    db.session.add(new_org)
    db.session.commit()


@pytest.fixture
def three_orgs(client):
    db.session.add_all([
        Org.new_from_dict(validate_org({
            "name": "Babies for Boomerangs",
            "sector": 2,
            "foci": [1]
            })),
        Org.new_from_dict(validate_org({
            "name": "Catch Me!",
            "sector": 2,
            "foci": 2
            })),
        Org.new_from_dict(validate_org({
            "name": "Thriving",
            "sector": 7,
            "foci": [1, 4]
            })),
    ])
    db.session.commit()


@pytest.fixture
def one_event(client):
    event_dict = validate_event({
            "name": "How to Stop Time",
            "type": 4,
            "subjects": [1, 3, 9],
            "date": "2021-12-21"
            })

    new_event = Event.new_from_dict(event_dict)
    
    db.session.add(new_event)
    db.session.commit()


@pytest.fixture
def three_events(client):
    db.session.add_all([
        Event.new_from_dict(validate_event({
            "name": "How to Stop Time",
            "type": 4,
            "subjects": [1, 3, 9],
            "date": "2021-12-21"
            })),
        Event.new_from_dict(validate_event({
            "name": "How to Restart Time",
            "type": 4,
            "subjects": 2,
            "date": "2021-12-21"
            })),
        Event.new_from_dict(validate_event({
            "name": "Time Manipulation Support",
            "type": 3,
            "subjects": [1, 99],
            "date": "2020-02-10",
            })),
    ])
    db.session.commit()


@pytest.fixture
def four_contacts_with_orgs_events(client, three_orgs, one_event):
    orgs = Org.query.all()
    org_ids = [ str(org.id) for org in orgs ]

    o1 = org_ids[0]
    o2 = org_ids[1]
    o3 = org_ids[2]

    contact1 = Contact.new_from_dict(validate_contact({
        "fname": "Nemonte",
        "lname": "Nenquimo",
        "age": 37,
        "gender": 1,
        "orgs": [o1]
    }))

    contact2 = Contact.new_from_dict(validate_contact({
        "fname": "Kate",
        "lname": "Dylan",
        "age": 38,
        "gender": 3,
    }))

    contact3 = Contact.new_from_dict(validate_contact({
        "fname": "Mary",
        "lname": "Seacole",
        "age": 52,
        "gender": 1,
        "orgs": [o3]
    }))

    contact4 = Contact.new_from_dict(validate_contact({
        "fname": "Nat",
        "lname": "Bentley",
        "age": 26,
        "gender": 2,
        "orgs": [o2, o3]
    }))
    
    db.session.add_all([contact1, contact2, contact3, contact4])
    db.session.commit()

    # participants = Contact.query.all()
    # participant_ids = []

    # for participant in participants:
    #     participant_ids.append(participant.id)

    # event_list = Event.query.all()
    # event = event_list[0]

    # ea1 = xEventAttendance(
    #     event_id=event.id, 
    #     participant_id=participant_ids[1],
    #     attended=True,
    #     completed=False
    #     )

    # ea2 = xEventAttendance(
    #     event_id=event.id,
    #     participant_id=participant_ids[2],
    #     attended=True,
    #     completed=True
    #     )
    
    # db.session.add_all([ea1, ea2])
    # db.session.commit()