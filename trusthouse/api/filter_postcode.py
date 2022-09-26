from flask.views import MethodView
from trusthouse.models.review import Review
from trusthouse.utils.validate_postcode import validate_postcode_request
from trusthouse.utils.request_messages import ok_message, error_message
from flask import jsonify
from ..extensions import app


class FilterByPostcodeAPI(MethodView):
    def get(self, postcode):
        user_postcode_request = postcode
        response = validate_postcode_request(user_postcode_request)
        if response == False:
            data = {
                'Search by postcode': error_message()[1],
                'Status': error_message()[2],
            }
            return jsonify(data)
        user_postcode_result = []
        get_reviews = Review.query.all()
        for review in get_reviews:
            if user_postcode_request == review.address.postcode:
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
                user_postcode_result.append(result)
        data = {
            'Search by postcode': ok_message()[2],
            'Reviews by postcode': user_postcode_result,
            'Status': ok_message()[3],
        }
        return jsonify(data)

app.add_url_rule(
    '/api/postcode/<postcode>',
    view_func=FilterByPostcodeAPI.as_view(
        name='filter_postcode_API'
    )
)