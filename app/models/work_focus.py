from app import db

class WorkFocus(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String)
    orgs = db.relationship("Org", back_populates="focus_rel")

    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            }