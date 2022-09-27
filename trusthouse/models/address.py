from ..extensions import db


# one to one relationship
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    door_num = db.Column(db.String(35), nullable=False)
    street = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    postcode = db.Column(db.String(10), nullable=False)
    geo_map = db.relationship('Maps', backref='location', uselist=False)
    reviews = db.relationship('Review', backref='address')
    buisnesses = db.relationship('Business', backref='place')
    incident = db.relationship('Incident', backref='area')

    