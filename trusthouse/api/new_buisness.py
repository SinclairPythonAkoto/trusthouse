from flask.views import MethodView
from trusthouse.utils.validate_postcode import validate_postcode_request
from trusthouse.utils.get_coordinates import get_postcode_coordinates
from trusthouse.utils.create_address import create_new_address
from trusthouse.utils.create_map import create_new_map
from trusthouse.utils.create_buisness import create_new_buisness
from trusthouse.utils.request_messages import error_message, ok_message
from flask import jsonify
from ..extensions import app


class NewBuisnessAPI(MethodView):
    def get( self, buisness_name, category, services, contact, door_num, streetname, location, postcode):
        name = buisness_name
        category = category
        services = services
        contact = contact
        door_num = door_num
        streetname = streetname
        location = location
        postcode = postcode

        # check if the business name & address already exists
        check_postcode = validate_postcode_request(postcode)

        if check_postcode == False or True:
            # if there is no coordinates do send error message
            user_postcode_coordinates = get_postcode_coordinates(postcode)
            if user_postcode_coordinates == []:
                message = error_message()[3]
                data = {
                    'Error': message
                }
                return jsonify(data)
            # save address, map & buisness details if coordinates found
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
                create_new_buisness(
                    name.lower(),
                    category.lower(),
                    services.lower(),
                    contact.lower(),
                    new_address,
                )
                data = {
                    'Successful upload': ok_message()[4],
                    'Status': ok_message()[3],
                    'New Upload': {
                        'Business Name': name.lower(),
                        'Business Category': category.lower(),
                        'Services': services.lower(),
                        'Contact': contact.lower(),
                        'Business Address': {
                            'Door Number': door_num.lower(),
                            'Street': streetname.lower(),
                            'Location': location.lower(),
                            'Postcode': postcode.lower(),
                        },
                    },
                }
                return jsonify(data)


app.add_url_rule(
    '/api/new-business/<buisness_name>,<category>,<services>,<contact>,<door_num>,<streetname>,<location>,<postcode>',
    view_func=NewBuisnessAPI.as_view(
        name='create_new_buisness'
    )
)

'''
- name
- category
- services
- contact
- door num
- streetname
- location
- postcode
'''