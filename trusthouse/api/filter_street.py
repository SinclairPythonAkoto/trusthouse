from flask.views import MethodView
from trusthouse.models.review import Review
from trusthouse.models.address import Address
from flask import jsonify
from ..extensions import app, db


class FilterByStreetAPI(MethodView):
    def get(self, street):
        user_street_request = street
        check_val = db.session.query(
            db.session.query(Address).filter_by(street=user_street_request).exists()
        ).scalar()
        if check_val == False:
            void = {'void': 'no match found'}
            return jsonify(void)
        res = []
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
                res.append(result)
        data = {'Reviews by street name': res}
        return jsonify(data)


app.add_url_rule(
    '/api/street/<street>',
    view_func=FilterByStreetAPI.as_view(
        name='filter_street_API'
    ),
)