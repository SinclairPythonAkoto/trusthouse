from ..extensions import db


# one to one relationship
class Maps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lon = db.Column(db.String(15), nullable=False)
    lat = db.Column(db.String(15), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))