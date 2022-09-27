from trusthouse.models.buisness import Business
from ..extensions import db, app

def create_new_buisness(buisness_name, buisness_category, contact_details, address):
    """
    Creates a new buisness entry, storing it in the Buisness table.
    Each new entry is linked to the Address id and Maps id.

    Returns the Buisness object back to the user.
    """
    with app.app_context():
        new_buisness_entry = Business(
            name=buisness_name.lower(),
            category=buisness_category.lower(),
            contact=contact_details.lower(),
            place=address,
        )
        db.session.add(new_buisness_entry)
        db.session.commit()
    return new_buisness_entry