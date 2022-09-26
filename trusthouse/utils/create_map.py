from trusthouse.models.maps import Maps
from ..extensions import db ,app 


def create_new_map(longitude, latitude, address):
    """
    Creates a new map entry, storing it in the Maps table.
    The coordinates derived from the user postcode request.
    Each entry is linked to the Address id.

    Returns the Maps object after saving it.
    """
    with app.app_context():
        new_map_entry = Maps(
            lon=longitude,
            lat=latitude,
            location=address,
        )
        db.session.add(new_map_entry)
        db.session.commit()
    return new_map_entry