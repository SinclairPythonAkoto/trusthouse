from flask.views import MethodView
from trusthouse.models.review import Review
from flask import jsonify
from ..extensions import app, db


class FilterByRatingAPI(MethodView):
    def get(self, rating):
        user_rating_request = int(rating)
        check_request = db.session.query(
            db.session.query(Review).filter_by(rating=user_rating_request).exists()
        ).scalar()
        if check_request == False:
            void = {'Void': 'No match found'}
            return jsonify(void)
        res = []
        get_reviews = Review.query.all()
        for review in get_reviews:
            if user_rating_request == review.rating:
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
        data = {'Reviews by Rating': res}
        return jsonify(data)


app.add_url_rule(
    '/api/rating/<rating>',
    view_func=FilterByRatingAPI.as_view(
        name='filter_rating_API'
    ),
)