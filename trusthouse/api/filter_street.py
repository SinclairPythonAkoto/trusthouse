from flask.views import MethodView
from trusthouse.models.review import Review
from trusthouse.utils.validate_street import validate_street_request
from trusthouse.utils.request_messages import error_message, ok_message
from flask import jsonify
from ..extensions import app


class FilterByStreetAPI(MethodView):
    def get(self, street):
        user_street_request = street
        response = validate_street_request(user_street_request)
        if response == False:
            void = {
                'Search by street name': error_message()[1],
                'Status': error_message()[2],
            }
            return jsonify(void)
        user_street_restult = []
        get_reviews = Review.query.all()
        for review in get_reviews:
            if user_street_request == review.address.street:
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
                user_street_restult.append(result)
        data = {
            'Search by street name': ok_message()[2],
            'Reviews by street name': user_street_restult,
            'Status': ok_message()[3],
        }
        return jsonify(data)


app.add_url_rule(
    '/api/street/<street>',
    view_func=FilterByStreetAPI.as_view(
        name='filter_street_API'
    ),
)