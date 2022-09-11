from flask.views import MethodView
from trusthouse.models.address import Address
from flask import jsonify
from ..extensions import app


class DisplayAllAddressesAPI(MethodView):
    def get(self):
        all_address = Address.query.all()
        db_query_result = []
        for address in all_address:
            result = {
                'id': address.id,
                'Door Number': address.door_num,
                'Street Name': address.street,
                'Location': address.location,
                'Postcode': address.postcode,
            }
            db_query_result.append(result)
        data = {'All Addresses': db_query_result}
        return jsonify(data)


app.add_url_rule(
    '/api/address',
    view_func=DisplayAllAddressesAPI.as_view(
        name='display_address_API'
    ),
)