import pytest
from app import create_app
from app import db
from flask.signals import request_finished


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
def one_contact(app):
    contact_dict = {
        "fname": "Nemonte",
        "lname": "Nenquimo",
        "age": 37,
        "gender": 1,
    }

    new_contact = Contact.new_from_dict(contact_dict)
    
    db.session.add(new_contact)
    db.session.commit()


def three_contacts(app):
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

    db.session.add_all([contact1, contact2, contact3])
    db.session.commit()

# def one_org(app):
#     org_dict = {
#         "name": "Abacus Inc.",
#         "age": 37,
#         "gender": 1,
#     }

#     new_org = Org.new_from_dict(org_dict)
    
#     db.session.add(new_org)
#     db.session.commit()