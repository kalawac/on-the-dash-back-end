from app import db
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from .types.org_sector import OrgSector
from .types.work_focus import WF

class Org(db.Model):
    id = db.Column(
        UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    name = db.Column(db.String)
    org_sector = db.Column(db.Enum(OrgSector))
    work_focus = db.Column(db.ARRAY(db.Enum("WF", name="wf_enum")))
    contacts = db.relationship("Contact", back_populates="orgs")

    @classmethod
    def new_from_dict(cls, data_dict):
        new_org = cls(
            name=data_dict["name"], 
            org_sector=data_dict["sector"],
            work_focus=data_dict["focus"], 
            )

        if len(data_dict.get("contact_ids", [])) >= 1:
            new_org.contact_ids = data_dict["contact_ids"]
        
        return new_org

    def to_dict(self):
        org_dict = {
                "id": self.id,
                "name": self.name,
                "sector": self.org_sector,
                "focus": self.work_focus,
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
        
        return org_dict
