import uuid

from sqlalchemy.dialects.postgresql import UUID, ARRAY

from app import db
from .types.org_sector import OrgSector
from .types.work_focus import WF


class Org(db.Model):
    id = db.Column(
        UUID(as_uuid = True), primary_key = True, default = uuid.uuid4)
    name = db.Column(db.String)
    org_sector = db.Column(db.Enum(OrgSector))
    foci = db.Column(db.ARRAY(db.Enum(WF, name="wf")))
    # need to set up association table for contacts 0..+ relationship

    def __repr__(self):
        return '<Org %r>' % self.name

    @classmethod
    def new_from_dict(cls, data_dict):
        return cls(
            name=data_dict["name"], 
            org_sector=data_dict["org_sector"],
            foci=data_dict["foci"]
            )

    def to_dict(self):
        org_dict = {
                "id": self.id,
                "name": self.name,
                "sector": self.org_sector,
                "foci": self.foci,
            }
        
        return org_dict
