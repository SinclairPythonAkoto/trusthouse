from ..extensions import db


# one to many relationship
class Buisness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    category = db.Column(db.String(30), nullable=False)
    services = db.Column(db.String(160), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))