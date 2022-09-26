from trusthouse.models.address import Address
from ..extensions import db


def validate_door_request(door):
    """
    Checks if the postcode exists within the Address table.
    Returns a boolean object.
    """
    response = db.session.query(
            db.session.query(Address).filter_by(door_num=door).exists()
        ).scalar()
    return response