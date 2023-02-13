from app import db
from sqlalchemy.dialects.postgresql import UUID

# Association table for 0..* : 0..* relationship between Contact and Org

class xContactOrg(db.Model):
    __tablename__ = "con_org"
    org_id = db.Column(UUID(as_uuid = True), db.ForeignKey('org.id'), primary_key=True)
    contact_id = db.Column(UUID(as_uuid = True), db.ForeignKey('contact.id'), primary_key=True)