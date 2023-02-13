from datetime import date
import uuid

from sqlalchemy.dialects.postgresql import UUID

from app import db
from .contact import Contact
from .event_attendance import xEventAttendance
from .types.event_type import EventType
from .types.subject import Subject
from app.routes.utils import validate_UUID

class Event(db.Model):
    id = db.Column(
        UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    name = db.Column(db.String)
    event_type = db.Column(db.Enum(EventType))
    subjects = db.Column(db.ARRAY(db.Enum(Subject)))
    date = db.Column(db.Date)
    participants = db.relationship("xEventAttendance", back_populates="event")


    @classmethod
    def new_from_dict(cls, data_dict):
        return cls(
            name=data_dict["name"], 
            event_type=data_dict["event_type"],
            subjects=data_dict["subjects"],
            date=data_dict["date"],
            participants=[]
            )

    def get_attendance_dict(self):
        attendance_query = xEventAttendance.query.filter_by(event_id=self.id).all()
        attendance_dict = dict()

        for attendance_data in attendance_query:
            participant_id = str(attendance_data.participant_id)
            attendance_dict[participant_id] = attendance_data.to_participant_dict()
        
        return attendance_dict

    def to_dict(self):
        event_dict = {
                "id": self.id,
                "name": self.name,
                "type": self.event_type,
                "subjects": self.subjects,
                "date": date.isoformat(self.date),
                "participants": []
            }

        if self.participants:
            for event_att_instance in self.participants:
                contact_id = str(event_att_instance.participant_id),
                contact = validate_UUID(Contact, contact_id)
                contact_dict = dict(
                    id=str(contact.id), # contact_id seems to be a list with one element
                    fname=contact.fname,
                    lname=contact.lname,
                    age=contact.age,
                    gender=contact.gender,
                    attendance_data=event_att_instance.to_participant_dict()
                )
                event_dict["participants"].append(contact_dict)
        
        return event_dict