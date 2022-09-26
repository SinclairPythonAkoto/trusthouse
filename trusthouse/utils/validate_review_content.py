from trusthouse.models.review import Review
from ..extensions import db


def validate_review_content(review_content):
    """
    Checks if the user review content already exists wihtin the Review table.
    Return a boolean object.
    """
    response = db.session.query(
            db.session.query(Review).filter_by(review=review_content).exists()
        ).scalar()
    return response