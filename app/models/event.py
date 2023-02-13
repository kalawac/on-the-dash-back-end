from datetime import date
import uuid

from sqlalchemy.dialects.postgresql import UUID

from app import db
# from .event_attendance import EventAttendance
from .types.event_type import EventType
from .types.subject import Subject

class Event(db.Model):
    id = db.Column(
        UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    name = db.Column(db.String)
    event_type = db.Column(db.Enum(EventType))
    subjects = db.Column(db.ARRAY(db.Enum(Subject)))
    date = db.Column(db.Date)
    # participants = db.relationship("Contact", secondary="event_attendance",  back_populates="events")

    # participant_ids = db.Column(UUID(as_uuid = True), db.ForeignKey('contact.id'), nullable=True)
    # attended = db.relationship("Contact", back_populates="events_attended"),
    # completed = db.relationship("Contact", back_populates="events_completed"),


    @classmethod
    def new_from_dict(cls, data_dict):
        return cls(
            name=data_dict["name"], 
            event_type=data_dict["event_type"],
            subjects=data_dict["subjects"],
            date=data_dict["date"],
            # participants = data_dict["participants"]
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
        #     attendance_query = EventAttendance.query.filter_by(event_id=self.id).all()
        #     attendance_dict = dict()

        #     for attendance_data in attendance_query:
        #         participant_id = str(attendance_data.participant_id)
        #         print(participant_id)
        #         attendance_dict[participant_id] = attendance_data.to_participant_dict()
        
        #     print(attendance_dict)

        #     for contact in self.participants:
        #         contact_dict = dict(
        #             id=str(contact.id),
        #             fname=contact.fname,
        #             lname=contact.lname,
        #             age=contact.age,
        #             gender=contact.gender,
        #             attendance_data=attendance_dict[str(contact.id)]
        #         )
        #         print(str(contact.id))
        #         event_dict["participants"].append(contact_dict)
        
        return event_dict