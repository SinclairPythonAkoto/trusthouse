from flask.views import MethodView
from trusthouse.models.review import Review
from flask import jsonify
from ..extensions import app


class AllReviewsAPI(MethodView):
    def get(self):
        all_reviews = Review.query.all()
        res = []
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
            res.append(result)
        data = {'All reviews': res}
        return jsonify(data)


app.add_url_rule(
    '/api/reviews',
    view_func=AllReviewsAPI.as_view(
        name='review_API'
    ),
)