from flask.views import MethodView
from trusthouse.models.review import Review
from trusthouse.utils.validate_door import validate_door_request
from trusthouse.utils.request_messages import error_message, ok_message
from flask import jsonify
from ..extensions import app


class FilterByDoorAPI(MethodView):
    def get(self, door):
        user_door_request = door
        response = validate_door_request(user_door_request)
        if response == False:
            data = {
                'Search by door number': error_message()[1],
                'Status': error_message()[2],
            }
            return jsonify(data)
        user_door_result = []
        get_reviews = Review.query.all()
        for review in get_reviews:
            if user_door_request == review.address.door_num:
                db_result = {
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
                user_door_result.append(db_result)
        data = {
            'Search by door number': ok_message()[2],
            'Reviews by door number': user_door_result,
            'Status': ok_message()[3],
        }
        return jsonify(data)


app.add_url_rule(
    '/api/door/<door>',
    view_func=FilterByDoorAPI.as_view(
        name='filter_door_API'
    ),
)