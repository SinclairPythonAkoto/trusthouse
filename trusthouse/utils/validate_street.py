from trusthouse.models.address import Address
from ..extensions import db


def validate_street_request(street):
    """
    Checks if the street name already exists in the Address table.
    Returns a boolean object.
    """
    response = db.session.query(
            db.session.query(Address).filter_by(street=street).exists()
        ).scalar()
    return response