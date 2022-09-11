from flask.views import MethodView
from trusthouse.models.address import Address
from trusthouse.models.review import Review
from flask import render_template, request
from ..extensions import app, db


class FilterByStreetName(MethodView):
    def post(self):
        user_street_request = request.form['searchStreetName']
        check_request = db.session.query(
            db.session.query(Address).filter_by(street=user_street_request).exists()
        ).scalar()
        if check_request == False:
            void = 'No match found.'
            return render_template('searchReviewPage.html', void=void)
        filter_street = Review.query.all()
        return render_template(
            'searchReviewPage.html',
            user_street_request=user_street_request,
            filter_street=filter_street,
        )


app.add_url_rule(
    '/reviews/street',
    view_func=FilterByStreetName.as_view(
        name='filter_street'
    ),
)