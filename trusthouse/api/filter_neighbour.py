from flask.views import MethodView
from trusthouse.models.review import Review
from flask import jsonify
from ..extensions import app


class FilterByNeighbourAPI(MethodView):
    def get(self):
        all_reviews = Review.query.filter_by(type='neighbour')
        res = []
        count = 0
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
        data = {'Review by Neighbours': res}
        return jsonify(data)


app.add_url_rule(
    '/api/neighbour',
    view_func=FilterByNeighbourAPI.as_view(
        name='filter_neighbough_API'
    ),
)