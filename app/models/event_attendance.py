# from app import db
# from sqlalchemy.dialects.postgresql import UUID

# # Association table for 0..* : 0..* relationship between Contact and Event

# class EventAttendance(db.Model):
#     event_id = db.Column(UUID(as_uuid = True), db.ForeignKey('event.id'), primary_key=True)
#     participant_id = db.Column(UUID(as_uuid = True), db.ForeignKey('contact.id'), primary_key=True)
#     event = db.relationship("Event", back_populates="participant_assoc")
#     contact = db.relationship("Contact", back_populates="event_assoc")
#     attended = db.Column(db.Boolean, default=False)
#     completed = db.Column(db.Boolean, default=False)
