from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .types.event_type import EventType
from .types.subject import Subject

class Event(db.Model):
    id = db.Column(
        UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    name = db.Column(db.String)
    event_type = db.Column(db.Enum(EventType))
    subjects = db.Column(db.ARRAY(db.Enum(Subject)))
    date = db.Column(db.DateTime)
    # participants = db.relationship("Contact", secondary="event_attendance",  back_populates="events", viewonly=True)
    # participant_assoc = db.relationship("EventAttendance", back_populates="event")

    # participant_ids = db.Column(UUID(as_uuid = True), db.ForeignKey('contact.id'), nullable=True)
    # attended = db.relationship("Contact", back_populates="events_attended"),
    # completed = db.relationship("Contact", back_populates="events_completed"),


    @classmethod
    def new_from_dict(cls, data_dict):
        new_event = cls(
            name=data_dict["name"], 
            event_type=data_dict["type"],
            date=data_dict["date"], 
            )

        subject_data = data_dict.get("subjects")

        if subject_data:
            if type(subject_data) == list or type(subject_data) == tuple:
                subject_list = []
                for subject_id in subject_data:
                    subject_enum = Subject(subject_id) if (type(subject_id) == int) else Subject[subject_id]
                    subject_list.append(subject_enum)
                new_event.subjects = subject_list
            else:
                subject_enum = Subject(subject_data) if (type(subject_data) == int) else Subject[subject_data]
                new_event.subjects = [subject_enum]

        return new_event


    def to_dict(self):
        event_dict = {
                "name": self.name,
                "type": self.event_type,
                "subjects": self.subjects,
                "date": self.date,
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