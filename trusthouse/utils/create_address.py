from trusthouse.models.address import Address
from ..extensions import db, app


def create_new_address(door, street, location, postcode):
    """
    Creates a new address entry, storing it in the Address table

    Resturns the Address object after saving it.
    """
    with app.app_context():
        new_address_entry = Address(
                    door_num=door.lower(),
                    street=street.lower(),
                    location=location.lower(),
                    postcode=postcode.lower(),
                )
        db.session.add(new_address_entry)
        db.session.commit()
    return new_address_entry