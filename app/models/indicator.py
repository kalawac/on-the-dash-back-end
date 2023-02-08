from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Indicator(db.Model):
    id = db.Column(
        UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    name = db.Column(db.String)
    # definition = db.Column(db.String)