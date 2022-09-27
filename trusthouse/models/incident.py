from ..extensions import db


# one to many relationship with address
class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(15), nullable=False) # this should be one word
    description = db.Column(db.String(40), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
