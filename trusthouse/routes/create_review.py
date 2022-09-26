from flask.views import MethodView
from trusthouse.utils.validate_door import validate_door_request
from trusthouse.utils.validate_postcode import validate_postcode_request
from trusthouse.utils.create_address import create_new_address
from trusthouse.utils.get_coordinates import get_postcode_coordinates
from trusthouse.utils.create_map import create_new_map
from trusthouse.utils.create_review import create_new_review
from trusthouse.utils.request_messages import error_message, ok_message, warning_message
from flask import render_template, request
from ..extensions import app


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
        check_door = validate_door_request(door)
        check_postcode = validate_postcode_request(postcode)

        if check_postcode == False:
            new_address = create_new_address(
                door.lower(),
                street_name.lower(),
                town_city.lower(),
                postcode.lower(),
            )
            # get latitude & logitude from user postcode
            user_postcode_coordinates = get_postcode_coordinates(postcode)
            # if there is NOT an existing latitude & longitude
            if user_postcode_coordinates == []:
                message = warning_message()[0]['Warning']
                return render_template('writeReviewPage.html', message=message)
            # if there IS existing longitute & latitude
            elif user_postcode_coordinates:
                latitude = user_postcode_coordinates[0].get('lat')
                longitude = user_postcode_coordinates[0].get('lon')
                print(longitude, latitude, new_address)
                create_new_map(longitude, latitude, new_address)
                create_new_review(review_rating, review_text, review_type, new_address)
                message = ok_message()[1]['Success']
                return render_template('writeReviewPage.html', message=message)
            else:
                message = error_message()[0]['Error']
                return render_template('writeReviewPage.html', message=message)
        else:
            if check_door == False and check_postcode == True:
                new_address = create_new_address(
                    door.lower(),
                    street_name.lower(),
                    town_city.lower(),
                    postcode.lower(),
                )
                user_postcode_coordinates = get_postcode_coordinates(postcode)
                create_new_review(review_rating, review_text, review_type, new_address)
                message = ok_message()[1]['Success']
                return render_template('writeReviewPage.html', message=message)
                
    

app.add_url_rule(
    '/writeReview',
    view_func=WriteReview.as_view(
        name='write_review'
    ),
)