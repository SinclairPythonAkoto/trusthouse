from trusthouse.models.buisness import Buisness
from ..extensions import db


def validate_business_name(business_name):
    '''
    Check if the buisness name exists in the Buisness table.
    Return a boolean object.
    '''
    response = db.session.query(
            db.session.query(Buisness).filter_by(name=business_name).exists()
        ).scalar()
    return response