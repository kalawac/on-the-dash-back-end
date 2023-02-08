from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .types.event_type import EventType

class Event(db.Model):
    id = db.Column(
        UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    name = db.Column(db.String)
    event_type = db.Column(db.Enum(EventType))
    subjects = db.Column(db.Enum(EventType))
    date = db.Column(db.DateTime)
    participants = db.relationship("Contact", secondary="event_attendance",  back_populates="events", viewonly=True)
    participant_assoc = db.relationship("EventAttendance", back_populates="event")

    # participant_ids = db.Column(UUID(as_uuid = True), db.ForeignKey('contact.id'), nullable=True)
    # attended = db.relationship("Contact", back_populates="events_attended"),
    # completed = db.relationship("Contact", back_populates="events_completed"),


    @classmethod
    def new_from_dict(cls, data_dict):
        new_org = cls(
            name=data_dict["name"], 
            work_focus=data_dict["work_focus"], 
            )

        if len(data_dict.get("contact_ids", [])) >= 1:
            new_org.contact_ids = data_dict["contact_ids"]
        
        return new_org

    def to_dict(self):
        org_dict = {
                "id": self.id,
                "name": self.name,
                "work_focus": self.work_focus,
                "contacts": [],
            }
        
        if contact_ids:
            for contact in self.contacts:
                contact_dict = dict(
                    id = contact.id,
                    fname = contact.fname,
                    lname = contact.lname,
                    age = contact.age,
                    gender = contact.gender
                )
                org_dict["contacts"].append(contact_dict)



## UTC does not have daylight saving time ever, so you can avoid that
## use ISO 8601 and save full date time object with time in UTC, even though I only want date
## call the object with just date and send it to FE like that, in ISO 8601 ('yyyy-mm-dd')
# use the standard datetime library