from flask.views import MethodView
from trusthouse.models.review import Review
from flask import jsonify

from trusthouse.utils.request_messages import ok_message
from ..extensions import app


class AllReviewsAPI(MethodView):
    def get(self):
        all_reviews = Review.query.all()
        review_result = []
        print(all_reviews)
        for review in all_reviews:
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
            review_result.append(result)
        data = {
            'Search all reviews': ok_message()[2],
            'Display Reviews': review_result,
            'Status': ok_message()[3],
        }
        return jsonify(data)


app.add_url_rule(
    '/api/reviews',
    view_func=AllReviewsAPI.as_view(
        name='review_API'
    ),
)