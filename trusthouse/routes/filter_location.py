from flask.views import MethodView
from trusthouse.models.review import Review
from trusthouse.utils.validate_location import validate_location_request
from trusthouse.utils.request_messages import error_message
from flask import render_template, request
from ..extensions import app


class FilterByLocation(MethodView):
    def post(self):
        user_location_request = request.form['searchLocation']
        response = validate_location_request(user_location_request)
        if response == False:
            void = error_message()[1]['Error']
            return render_template('searchReviewPage.html', void=void)
        filter_location = Review.query.all()
        return render_template(
            'searchReviewPage.html',
            user_location_request=user_location_request,
            filter_location=filter_location,
        )


app.add_url_rule(
    '/reviews/location',
    view_func=FilterByLocation.as_view(
        name='filter_location'
    ),
)