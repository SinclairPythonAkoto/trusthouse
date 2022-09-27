from trusthouse.models.incident import Incident
from ..extensions import db, app
from datetime import datetime


def new_incident(category, description, address):
    """
    Creates a new incident entry, saving it into the Incident table.
    Each entry is linked to both Address & Maps tables.

    Returns the Incident object back to the user.
    """
    with app.app_context():
        new_incident_entry = Incident(
            category=category.lower(),
            description=description.lower(),
            date=datetime.now(),
            area=address,
        )
        db.session.add(new_incident_entry)
        db.session.commit()
    return new_incident_entry