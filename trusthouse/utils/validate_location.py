from trusthouse.models.address import Address
from ..extensions import db


def validate_location_request(location):
    """
    Checks if the location exists in the Address table.
    Returns a boolean object
    """
    response = db.session.query(
            db.session.query(Address).filter_by(location=location).exists()
        ).scalar()
    return response