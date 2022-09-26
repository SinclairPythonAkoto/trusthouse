from flask.views import MethodView
from trusthouse.models.review import Review
from trusthouse.utils.validate_location import validate_location_request
from trusthouse.utils.request_messages import error_message, ok_message
from flask import jsonify
from ..extensions import app


class FilterByLocationAPI(MethodView):
    def get(self, location):
        user_location_request = location
        response = validate_location_request(user_location_request)
        if response == False:
            data = {
                'Search by location': error_message()[1],
                'Status': error_message()[2],
            }
            return jsonify(data)
        user_location_result = []
        get_reviews = Review.query.all()
        for review in get_reviews:
            if user_location_request == review.address.location:
                result = {
                    'id': review.id,
                    'Rating': review.rating,
                    'Review': review.review,
                    'Type': review.type,
                    'Date': review.date,
                    'Address ID': review.address_id,
                    'Address': {
                        'id': review.address.id,
                        'Door Number': review.address.street,
                        'Street': review.address.street,
                        'Postode': review.address.postcode,
                    },
                }
                user_location_result.append(result)
        data = {
            'Search by loction': ok_message()[2],
            'Reviews by location': user_location_result,
            'Status': ok_message()[3],
        }
        return jsonify(data)

app.add_url_rule(
    '/api/location/<location>',
    view_func=FilterByLocationAPI.as_view(
        name='filter_location_API'
    ),
)