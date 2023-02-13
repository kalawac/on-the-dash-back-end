from app import db
from sqlalchemy.dialects.postgresql import UUID

# Association table for 0..* : 0..* relationship between Contact and Event

class xEventAttendance(db.Model):
    __tablename__ = "event_att"
    event_id = db.Column(UUID(as_uuid = True), db.ForeignKey('event.id'), primary_key=True)
    participant_id = db.Column(UUID(as_uuid = True), db.ForeignKey('contact.id'), primary_key=True)
    attended = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)
    participant = relationship("Contact", back_populates="events")
    event = relationship("Event", back_populates="participants")


    # @classmethod
    # def new_from_dict(cls, data_dict):
    #     return cls(
    #         event_id=data_dict["event_id"], 
    #         participant_id=data_dict["participant_id"]
    #         )

    # def to_dict(self):
    #     event_attendance_dict = dict()

    #     event_attendance_dict[self.participant_id] = dict(
    #         attendance=self.attended,
    #         completion=self.completed
    #         )
    #     return event_attendance_dict

    # def to_participant_dict(self):
    #     return dict(
    #         attendance=self.attended,
    #         completion=self.completed
    #         )