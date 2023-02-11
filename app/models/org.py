from app import db
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
from .types.org_sector import OrgSector
from .work_focus import WorkFocus
from .contact import Contact
from app.routes.utils import validate_intID, validate_UUID

# PostgreSQL Array of Enum has bug. Switched to relationship with model WorkFocus.

class Org(db.Model):
    id = db.Column(
        UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    name = db.Column(db.String)
    org_sector = db.Column(db.Enum(OrgSector))
    foci = db.Column(db.Integer, db.ForeignKey('work_focus.id'))
    focus_rel = db.relationship("WorkFocus", back_populates="orgs")
    contacts = db.relationship("Contact", back_populates="orgs")

    def __repr__(self):
        return '<Org %r>' % self.name

    @classmethod
    def new_from_dict(cls, data_dict):
        new_org = cls(
            name=data_dict["name"], 
            org_sector=data_dict["sector"],
            )

        if len(data_dict.get("foci", [])) >= 1:
            for wf_id in data_dict["foci"]:
                wf = validate_intID(WorkFocus, wf_id)
                new_org.focus_rel.append(wf)

        if len(data_dict.get("contact_ids", [])) >= 1:
            for contact_id in data_dict["contact_ids"]:
                contact = validate_UUID(Contact, contact_id)

                if contact not in org.contacts:
                    new_org.contacts.append(contact)
        
        return new_org

    def to_dict(self):
        org_dict = {
                "id": self.id,
                "name": self.name,
                "sector": self.org_sector,
                "foci": self.foci,
                "contacts": [],
            }
        
        if self.contacts:
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
