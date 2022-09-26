from trusthouse.models.address import Address
from ..extensions import db


def validate_postcode_request(postcode):
    """
    Checks if the postcode exists within the Addres table.
    Returns a boolean object.
    """
    response = db.session.query(
            db.session.query(Address).filter_by(postcode=postcode).exists()
        ).scalar()
    return response
