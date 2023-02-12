import uuid

from sqlalchemy.dialects.postgresql import UUID

from app import db
from .types.gender import Gender

class Contact(db.Model):
    id = db.Column(
        UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    fname = db.Column(db.String)
    lname = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum(Gender))
    # org_ids = db.Column(UUID(as_uuid = True), db.ForeignKey('org.id')) # will come back as an empty list
    # orgs = db.relationship("Org", back_populates="contacts") # will probably come back as empty list, single ID may come back as None
    # events = db.relationship("Event", secondary="event_attendance", back_populates="participants", viewonly=True)
    # event_assoc = db.relationship("EventAttendance", back_populates="contact")

    # indicators = db.relationship("Indicator", back_populates="participants")

    def __repr__(self):
        return '<Contact %r>' % " ".join([self.fname,self.lname])

    @classmethod
    def new_from_dict(cls, data_dict):
        new_contact = cls(
            fname=data_dict["fname"], 
            lname=data_dict["lname"], 
            age=data_dict["age"] if data_dict["age"] else 0,
            gender=data_dict["gender"],
            )

        # if len(data_dict.get("org_ids", [])) >= 1:
        #     new_contact.orgs.extend(data_dict["org_ids"])
        
        return new_contact

    def to_dict(self):
        contact_dict = {
                "id": self.id,
                "fname": self.fname,
                "lname": self.lname,
                "age": self.age,
                "gender": self.gender,
                "orgs": [],
                "events": [],
            }
        
        # if self.org_ids:
        #     for org in self.orgs:
        #         contact_dict["orgs"].append(org.to_dict())

        # if self.events:
        #     for event in self.events:
        #         ev_dict = dict(
        #             id = event.id,
        #             name = event.name,
        #             event_type = event.event_type
        #         )
        #         contact_dict["events"].append(ev_dict)
        
        return contact_dict

# DEALING WITH INDICATORS FOR TABLES
# model that is the metadata for the dataset
# endpoint that returns that data as a huge list of JSON objects. something like the weather API reponse.
# bundle all the data needed per viz / table into a route -- list of columns names, list of data points