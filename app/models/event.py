from datetime import date
import uuid

from sqlalchemy.dialects.postgresql import UUID

from app import db
from .types.event_type import EventType
from .types.subject import Subject

class Event(db.Model):
    id = db.Column(
        UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    name = db.Column(db.String)
    event_type = db.Column(db.Enum(EventType))
    subjects = db.Column(db.ARRAY(db.Enum(Subject)))
    date = db.Column(db.Date)
    # participants = db.relationship("Contact", secondary="event_attendance",  back_populates="events", viewonly=True)
    # participant_assoc = db.relationship("EventAttendance", back_populates="event")

    # participant_ids = db.Column(UUID(as_uuid = True), db.ForeignKey('contact.id'), nullable=True)
    # attended = db.relationship("Contact", back_populates="events_attended"),
    # completed = db.relationship("Contact", back_populates="events_completed"),


    @classmethod
    def new_from_dict(cls, data_dict):
        return cls(
            name=data_dict["name"], 
            event_type=data_dict["event_type"],
            subjects=data_dict["subjects"],
            date=data_dict["date"]
            )


    def to_dict(self):
        event_dict = {
                "id": self.id,
                "name": self.name,
                "type": self.event_type,
                "subjects": self.subjects,
                "date": date.isoformat(self.date),
                "participants": []
            }
        
        # if self.participants:
        #     for participant in self.participants:
        #         contact_dict = dict(
        #             id = contact.id,
        #             fname = contact.fname,
        #             lname = contact.lname,
        #             age = contact.age,
        #             gender = contact.gender
        #         )
        #         event_dict["participants"].append(contact_dict)
        
        return event_dict



## UTC does not have daylight saving time ever, so you can avoid that
## use ISO 8601 and save full date time object with time in UTC, even though I only want date
## call the object with just date and send it to FE like that, in ISO 8601 ('yyyy-mm-dd')
# use the standard datetime library