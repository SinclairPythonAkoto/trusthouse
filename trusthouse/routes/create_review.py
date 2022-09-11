import requests
from datetime import datetime
from flask.views import MethodView
from trusthouse.models.address import Address
from trusthouse.models.maps import Maps
from trusthouse.models.review import Review
from flask import render_template, request
from ..extensions import app, db


class WriteReview(MethodView):
    def get(self):
        return render_template('writeReviewPage.html')
    
    def post(self):
        # address data
        door = request.form['propertyNumber']
        street_name = request.form['streetName']
        town_city = request.form['town_city']
        postcode = request.form['postcode']
        # review data
        review_rating = request.form['rating']
        review_rating = int(review_rating)
        review_text = request.form['reviewText']
        review_type = request.form['selection']

        # get data to check if new review already exists
        get_door_num = Address.query.filter_by(door_num=door).all()
        get_postcode = Address.query.filter_by(postcode=postcode).all()
        get_review_content = Review.query.filter_by(review=review_text).all()

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
                new_review = Review(
                    rating=review_rating,
                    review=review_text,
                    type=review_type,
                    date=datetime.now(),
                    address=new_address,
                )
                db.session.add(new_review)
                db.session.commit()
                message = 'Your review has been uploaded!'
                return render_template('writeReviewPage.html', message=message)
            else:
                new_review = Review(
                    rating=review_rating,
                    review=review_text,
                    type=review_type,
                    date=datetime.now(),
                    address=new_address,
                )
                db.session.add(new_review)
                db.session.commit()
                message = 'Your review has been uploaded!'
                return render_template('writeReviewPage.html', message=message)
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
                    new_review = Review(
                        rating=review_rating,
                        review=review_text,
                        type=review_type,
                        date=datetime.now(),
                        address=new_address,
                    )
                    db.session.add(new_review)
                    db.session.commit()
                    message = 'Your review has been uploaded!'
                    return render_template('writeReviewPage.html', message=message)
            else:
                if door == get_door_num[0].door_num and postcode == get_postcode[0].postcode:
                    if len(get_review_content) != 0:
                        new_review = Review(
                            rating=review_rating,
                            review=review_text,
                            type=review_type,
                            date=datetime.now(),
                            address=get_postcode[0],
                        )
                        db.session.add(new_review)
                        db.session.commit()
                        message = 'A new review has been added to an existing postcode.'
                        return render_template('writeReviewPage.html', message=message)
                    new_review = Review(
                        rating=review_rating,
                        review=review_text,
                        type=review_type,
                        date=datetime.now(),
                        address=get_postcode[0],
                    )
                    db.session.add(new_review)
                    db.session.commit()
                    message = 'A new review has been added'
                    return render_template('writeReviewPage.html', message=message)
    

app.add_url_rule(
    '/writeReview',
    view_func=WriteReview.as_view(
        name='write_review'
    ),
)