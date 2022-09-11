import requests
from flask.views import MethodView
from trusthouse.models.address import Address
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
            response = requests.get(f"{BASE_URL}&postalcode={postcode}&country=united kingdom")
            data = response.json()
            # if there is an existing latitude & longitude
            if data == None:
                # creating the json response for just address, no coordinates
                warning = 'Warning'
                message = 'Your address has been uploaded to Trust House, but the coordinates to your postcode could not be saved.'
                data = {warning:message}
                return jsonify(data)
            elif data != None:
                # creating the json response
                success = 'Successful upload'
                message = 'Your address has been uploaded to Trust House.'
                data = {success: message}
                return jsonify(data)
            else:
                void = 'Error'
                message = 'Something went wrong, please check & try again'
                data = {void:message}
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
                if data != None:
                    success = 'Successful upload'
                    message = 'Your address has been uploaded to Trust House.'
                    data = {success: message}
                    return jsonify(data)
            else:
                if door == get_door_num[0].door_num and postcode == get_postcode[0].postcode:
                    message = 'This address is already in the system.'
                    void = 'Error'
                    data = {void:message}
                    return jsonify(data)


app.add_url_rule(
    '/api/new-address/<address_door_num>,<address_street_name>,<address_location>,<address_postcode>',
    view_func=NewAddressAPI.as_view(
        name='create_new_address'
    ),
)