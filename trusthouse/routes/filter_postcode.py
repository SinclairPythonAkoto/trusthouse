from flask import render_template, request
from flask.views import MethodView
from trusthouse.models.address import Address
from trusthouse.models.review import Review
from ..extensions import app, db


class FilterByPostcode(MethodView):
    def post(self):
        user_postcode_request = request.form['searchPostcode']
        check_request = db.session.query(
            db.session.query(Address).filter_by(postcode=user_postcode_request).exists()
        ).scalar()
        if check_request == False:
            void = 'No match found.'
            return render_template('searchReviewPage.html', void=void)
        filter_postcode = Review.query.all()
        return render_template(
            'searchReviewPage.html',
            user_postcode_request=user_postcode_request,
            filter_postcode=filter_postcode,
        )


app.add_url_rule(
    '/reviews/postcode',
    view_func=FilterByPostcode.as_view(
        name='filter_postcode'
    ),
)