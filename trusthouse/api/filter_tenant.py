from flask.views import MethodView
from trusthouse.models.review import Review
from trusthouse.utils.request_messages import ok_message
from flask import jsonify
from ..extensions import app


class FilterByTenantAPI(MethodView):
    def get(self):
        all_reviews = Review.query.filter_by(type='tenant')
        tenant_results = []
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
            tenant_results.append(result)
        data = {
            'Search reviews by tenants': ok_message()[2],
            'Reviews by tenants': tenant_results,
            'Status': ok_message()[3],
        }
        return jsonify(data)


app.add_url_rule(
    '/api/tenant',
    view_func=FilterByTenantAPI.as_view(
        name='filter_tenant_API'
    ),
)