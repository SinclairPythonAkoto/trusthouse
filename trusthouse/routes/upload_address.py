from flask.views import MethodView
from trusthouse.utils.validate_postcode import validate_postcode_request
from trusthouse.utils.validate_door import validate_door_request
from trusthouse.utils.get_coordinates import get_postcode_coordinates
from trusthouse.utils.create_address import create_new_address
from trusthouse.utils.create_map import create_new_map
from trusthouse.utils.request_messages import warning_message, error_message, ok_message
from flask import render_template, request, jsonify
from ..extensions import app


class UploadAddress(MethodView):
    def get(self):
        return render_template('newAddress.html')
    
    def post(self):
        door = request.form['doorNum']
        street_name = request.form['streetName']
        location = request.form['addressLocation']
        postcode = request.form['addressPostcode']

        # use the validation functions to check if door & postcode match or not 
        door_request = validate_door_request(door)
        postcode_request = validate_postcode_request(postcode)
        # if there is no preexisting postcode create new address.
        if postcode_request == False:
            # write fuction
            new_address = create_new_address(door, street_name, location, postcode)
            # write fuction
            user_postcode_coordinates = get_postcode_coordinates(postcode)
            # write fuction
            if user_postcode_coordinates == []:
                # write fuction
                data = {
                    'Incomplete upload': warning_message()[0], 
                    'Status':warning_message()[2]
                }
                return jsonify(data)
            elif user_postcode_coordinates:
                latitude = user_postcode_coordinates[0].get('lat')
                longitude = user_postcode_coordinates[0].get('lon')
                create_new_map(longitude, latitude, new_address)
                message = ok_message()[0]['Success']
                return render_template('newAddress.html', message=message)
            else:
                data = {
                    'Unexpected error': error_message()[0],
                    'status': error_message()[2], 
                }
                return jsonify(data)
        else:
            if door_request == False and postcode_request == True:
                new_address = create_new_address(door, street_name, location, postcode)
                user_postcode_coordinates = get_postcode_coordinates(postcode)
                # if there is an existing latitude & longitude
                if user_postcode_coordinates:
                    latitude = user_postcode_coordinates[0].get('lat')
                    longitude = user_postcode_coordinates[0].get('lon')
                    create_new_map(longitude, latitude, new_address)
                    message = ok_message()[0]['Success']
                    return render_template('newAddress.html', message=message)


app.add_url_rule(
    '/createAddress',
    view_func=UploadAddress.as_view(
        'upload_address',
    ),
)