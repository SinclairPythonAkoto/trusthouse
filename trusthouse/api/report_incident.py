from datetime import datetime
from flask.views import MethodView
from trusthouse.utils.validate_postcode import validate_postcode_request
from trusthouse.utils.get_coordinates import get_postcode_coordinates
from trusthouse.utils.create_address import create_new_address
from trusthouse.utils.create_map import create_new_map
from trusthouse.utils.create_incident import new_incident
from trusthouse.utils.request_messages import error_message, ok_message
from flask import jsonify
from ..extensions import app


class ReportIncident(MethodView):
    def get(self, category, description, door_num, streetname, location, postcode):
        incident = category
        description = description
        door_num = door_num
        streetname = streetname
        location = location 
        postcode = postcode

        # valiate the postcode
        check_postcode = validate_postcode_request(postcode)

        if check_postcode == False or True:
            user_postcode_coordinates = get_postcode_coordinates(postcode)
            if user_postcode_coordinates == []:
                message = error_message()[4]
                data = {
                    'Error': message
                }
                return jsonify(data)
            elif user_postcode_coordinates:
                new_address = create_new_address(
                    door_num.lower(),
                    streetname.lower(),
                    location.lower(),
                    postcode.lower(),
                )
                latitude = user_postcode_coordinates[0].get('lat')
                longitude = user_postcode_coordinates[0].get('lon')
                create_new_map(longitude, latitude, new_address)
                new_incident(incident, description, new_address)
                data = {
                    'Successful upload': ok_message()[4],
                    'Status': ok_message()[3],
                    'New Incident': {
                        'Incident': category.lower(),
                        'Description': description.lower(),
                        'Date': datetime.now(),
                        'Incident Address': {
                            'Door Number': door_num.lower(),
                            'Street': streetname.lower(),
                            'Location': location.lower(),
                            'Postcode': postcode.lower(),
                        },
                    }
                }
                return jsonify(data)


app.add_url_rule(
    '/api/report/<category>,<description>,<door_num>,<streetname>,<location>,<postcode>',
    view_func=ReportIncident.as_view(
        name='report_incident_API',
    )
)