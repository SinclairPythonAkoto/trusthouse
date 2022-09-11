from flask.views import MethodView
from trusthouse.models.review import Review
from trusthouse.models.address import Address
from flask import jsonify
from ..extensions import app, db


class FilterByDoorAPI(MethodView):
    def get(self, door):
        user_door_request = door
        check_val = db.session.query(
            db.session.query(Address).filter_by(door_num=user_door_request).exists()
        ).scalar()
        if check_val == False:
            void = 'Error'
            message = 'No match found'
            data = {void:message}
            return jsonify(void)
        res = []
        get_reviews = Review.query.all()
        print(get_reviews)
        for review in get_reviews:
            if user_door_request == review.address.door_num:
                result = {
                    'id': review.id,
                    'Rating': review.rating,
                    'Review': review.review,
                    'Type': review.type,
                    'Date': review.date,
                    'Address ID': review.address_id,
                    'Address': {
                        'id': review.address.id,
                        'Door Number': review.address.door_num,
                        'Street': review.address.street,
                        'Postode': review.address.postcode,
                    },
                }
                res.append(result)
        success = 'Successful upload'
        message = 'Your address has been uploaded to Trust House.'
        data = {
            success:message,
            'Reviews by door number': res
        }
        return jsonify(data)


app.add_url_rule(
    '/api/door/<door>',
    view_func=FilterByDoorAPI.as_view(
        name='filter_door_API'
    ),
)