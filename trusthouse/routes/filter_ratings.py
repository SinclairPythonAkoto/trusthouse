from flask.views import MethodView
from trusthouse.models.review import Review
from trusthouse.utils.validate_rating import validate_rating_request
from trusthouse.utils.request_messages import error_message
from flask import render_template, request
from ..extensions import app, db


class FilterByRating(MethodView):
    def post(self):
        user_rating_request = request.form['searchRating']
        user_rating_request = int(user_rating_request)
        response = validate_rating_request(user_rating_request)
        if response == False:
            void = error_message()[1]['Error']
            return render_template('searchReviewPage.html', void=void)
        get_ratings = db.session.query(Review).filter_by(rating=user_rating_request).all()
        return render_template('searchReviewPage.html', get_ratings=get_ratings)


app.add_url_rule(
    '/reviews/rating',
    view_func=FilterByRating.as_view(
        name='filter_rating'
    ),
)