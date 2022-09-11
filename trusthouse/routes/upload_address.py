import requests
from datetime import datetime
from flask.views import MethodView
from trusthouse.models.address import Address
from trusthouse.models.maps import Maps
from trusthouse.models.review import Review
from flask import render_template, request, jsonify
from ..extensions import app, db


class UploadAddress(MethodView):
    def get(self):
        return render_template('newAddress.html')
    
    def post(self):
        door = request.form['doorNum']
        street_name = request.form['streetName']
        location = request.form['addressLocation']
        postcode = request.form['addressPostcode']

        # get data to check if new review already exists
        get_door_num = Address.query.filter_by(door_num=door).all()
        get_postcode = Address.query.filter_by(postcode=postcode).all()

        BASE_URL = 'https://nominatim.openstreetmap.org/search?format=json'

        if len(get_postcode) == 0:
            new_address = Address(
                door_num=door.lower(),
                street=street_name.lower(),
                location=location.lower(),
                postcode=postcode.lower(),
            )
            db.session.add(new_address)
            db.session.commit()
            # get latitude & logitude from user postcode
            response = requests.get(f"{BASE_URL}&postalcode={postcode}&country=united kingdom")
            data = response.json()
            # if there is an existing latitude & longitude
            if data == []:
                warning = 'Warning'
                message = 'Your address has been uploaded to Trust House, but the coordinates to your postcode could not be saved.'
                data = {warning:message}
                return jsonify(data)
            elif data != []:
                print(data)
                latitude = data[0].get('lat')
                longitude = data[0].get('lon')
                new_geo_map = Maps(
                    lon=longitude,
                    lat=latitude,
                    location=new_address,
                )
                db.session.add(new_geo_map)
                db.session.commit()
                message = 'Your address has been uploaded to Trust House.'
                return render_template('newAddress.html', message=message)
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
                    location=location.lower(),
                    postcode=postcode.lower(),
                )
                db.session.add(new_address)
                db.session.commit()
                response = requests.get(f"{BASE_URL}&postalcode={postcode}&country=united kingdom")
                data = response.json()
                # if there is an existing latitude & longitude
                if data[0]:
                    latitude = data[0].get('lat')
                    longitude = data[0].get('lon')
                    new_geo_map = Maps(
                        lon=longitude,
                        lat=latitude,
                        location=new_address,
                    )
                    db.session.add(new_geo_map)
                    db.session.commit()
                    message = 'Your review has been uploaded!'
                    return render_template('newAddress.html', message=message)


app.add_url_rule(
    '/createAddress',
    view_func=UploadAddress.as_view(
        'upload_address',
    ),
)