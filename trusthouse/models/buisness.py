from ..extensions import db


# one to many relationship
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    category = db.Column(db.String(15), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))