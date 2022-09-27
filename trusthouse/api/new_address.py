import requests
from flask.views import MethodView
from trusthouse.models.address import Address
from trusthouse.utils.get_coordinates import get_postcode_coordinates
from trusthouse.utils.request_messages import warning_message, error_message, ok_message
from flask import jsonify
from ..extensions import app, db


class NewAddressAPI(MethodView):
    def get(self, address_door_num, address_street_name, address_location, address_postcode):
        # address data
        door = address_door_num
        street_name = address_street_name
        town_city = address_location
        postcode = address_postcode

        # get data to check if new review already exists
        get_door_num = Address.query.filter_by(door_num=door).all()
        get_postcode = Address.query.filter_by(postcode=postcode).all()

        BASE_URL = 'https://nominatim.openstreetmap.org/search?format=json'

        if len(get_postcode) == 0:
            new_address = Address(
                door_num=door.lower(),
                street=street_name.lower(),
                location=town_city.lower(),
                postcode=postcode.lower(),
            )
            db.session.add(new_address)
            db.session.commit()
            # get latitude & logitude from user postcode
            user_postcode_coordinates = get_postcode_coordinates(postcode)

            # if there is an existing latitude & longitude
            if user_postcode_coordinates == None:
                # creating the json response for just address, no coordinates
                data = {
                    'Incomplete upload': warning_message()[0],
                    'Status': warning_message()[1]
                }
                return jsonify(data)
            elif user_postcode_coordinates != None:
                # creating the json response
                data = {
                    'Successful upload': ok_message()[0],
                    'Status': ok_message()[2],
                }
                return jsonify(data)
            else:
                data = {
                'Search by door number': error_message()[0],
                'Status': error_message()[3],
                }
                return jsonify(data)
        else:
            if not get_door_num and postcode == get_postcode[0].postcode:
                new_address = Address(
                    door_num=door.lower(),
                    street=street_name.lower(),
                    location=town_city.lower(),
                    postcode=postcode.lower(),
                )
                db.session.add(new_address)
                db.session.commit()
                response = requests.get(f"{BASE_URL}&postalcode={postcode}&country=united kingdom")
                data = response.json()
                # if there is an existing latitude & longitude
                if user_postcode_coordinates != None:
                    data = {
                        'Add new address': ok_message()[0]['Success'],
                        'Status': ok_message()[3]
                    }
                    return jsonify(data)
            else:
                if door == get_door_num[0].door_num and postcode == get_postcode[0].postcode:
                    message = 'This address is already in the system.'
                    void = 'Error'
                    data = {void:message}
                    return jsonify(data)


app.add_url_rule(
    '/api/new/address/<address_door_num>,<address_street_name>,<address_location>,<address_postcode>',
    view_func=NewAddressAPI.as_view(
        name='create_new_address'
    ),
)