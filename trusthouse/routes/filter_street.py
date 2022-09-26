from flask.views import MethodView
from trusthouse.models.review import Review
from trusthouse.utils.validate_street import validate_street_request
from trusthouse.utils.request_messages import error_message
from flask import render_template, request
from ..extensions import app


class FilterByStreetName(MethodView):
    def post(self):
        user_street_request = request.form['searchStreetName']
        response = validate_street_request(user_street_request)
        if response == False:
            void = error_message()[1]['Error']
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