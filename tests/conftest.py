import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.contact import Contact
from app.models.org import Org
from app.models.work_focus import WorkFocus
from app.models.event import Event
from app.models.event_attendance import EventAttendance


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


@pytest.fixture
def one_event(client):
    event_dict = {
            "name": "How to Stop Time",
            "type": 4,
            "subjects": 1, # can only have one subject for now
            "date": "2021-12-21T00:00:00.000Z"
            }

    new_event = Event.new_from_dict(event_dict)
    
    db.session.add(new_event)
    db.session.commit()


@pytest.fixture
def three_events(client):
    db.session.add_all([
        Event.new_from_dict({
            "name": "How to Stop Time",
            "type": 4,
            "subjects": 1, # can only have one subject at a time for now
            "date": "2021-12-21T00:00:00.000Z"
            }),
        Event.new_from_dict({
            "name": "How to Restart Time",
            "type": 4,
            "subjects": 2,
            "date": "2021-12-21T00:27:00.000Z"
            }),
        Event.new_from_dict({
            "name": "Time Manipulation Support",
            "type": 3,
            "subjects": 99,
            "date": "2023-02-10T04:03:30.079Z",
            }),
    ])
    db.session.commit()


@pytest.fixture
def four_contacts_with_orgs_events(client, three_orgs, one_event):
    contact1 = Contact.new_from_dict({
        "fname": "Nemonte",
        "lname": "Nenquimo",
        "age": 37,
        "gender": 1,
        "orgs": [1]
    })

    contact2 = Contact.new_from_dict({
        "fname": "Kate",
        "lname": "Dylan",
        "age": 38,
        "gender": 3,
    })

    contact3 = Contact.new_from_dict({
        "fname": "Mary",
        "lname": "Seacole",
        "age": 52,
        "gender": 1,
        "orgs": [3]
    })

    contact4 = Contact.new_from_dict({
        "fname": "Nat",
        "lname": "Bentley",
        "age": 26,
        "gender": 2,
        "orgs": [2,3]
    })
    
    db.session.add_all([contact1, contact2, contact3, contact4])
    db.session.commit()

    participants = Contact.query.all()
    participant_ids = []

    for participant in participants:
        participant_ids.append(participant.id)

    event_list = Event.query.all()
    event = event_list[0]

    ea1 = EventAttendance(
        event_id=event.id, 
        participant_id=participant_ids[1],
        attended=True,
        completed=False
        )

    ea2 = EventAttendance(
        event_id=event.id,
        participant_id=participant_ids[2],
        attended=True,
        completed=True
        )
    
    db.session.add_all([ea1, ea2])
    db.session.commit()