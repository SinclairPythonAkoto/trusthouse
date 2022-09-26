from trusthouse.models.review import Review
from ..extensions import db


def validate_rating_request(rating):
    """
    Checks if the user rating already exists wihtin the Review table.
    Return a boolean object.
    """
    response = db.session.query(
            db.session.query(Review).filter_by(rating=rating).exists()
        ).scalar()
    return response