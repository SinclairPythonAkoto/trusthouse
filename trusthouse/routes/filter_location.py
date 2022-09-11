from flask.views import MethodView
from trusthouse.models.address import Address
from trusthouse.models.review import Review
from flask import render_template, request
from ..extensions import app, db


class FilterByLocation(MethodView):
    def post(self):
        user_location_request = request.form['searchLocation']
        check_request = db.session.query(
            db.session.query(Address).filter_by(location=user_location_request).exists()
        ).scalar()
        if check_request == False:
            void = 'No match found.'
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