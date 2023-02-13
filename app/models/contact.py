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
    orgs = db.relationship("Org", secondary="con_org", back_populates="contacts")
    events = db.relationship("xEventAttendance", back_populates="participant")

    # indicators = db.relationship("Indicator", secondary="ind_con" back_populates="participants")
    # I actually suspect that indicators relationship will be more like events (association object)

    def __repr__(self):
        return '<Contact %r>' % " ".join([self.fname,self.lname])

    @classmethod
    def new_from_dict(cls, data_dict):
        return cls(
            fname=data_dict["fname"], 
            lname=data_dict["lname"], 
            age=data_dict["age"] if data_dict["age"] else 0,
            gender=data_dict["gender"],
            orgs=data_dict.get("orgs", [])
            )

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
        
        if self.orgs:
            for org in self.orgs:
                org_dict = {
                    "id": str(org.id),
                    "name": org.name
                }
                contact_dict["orgs"].append(org_dict)

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