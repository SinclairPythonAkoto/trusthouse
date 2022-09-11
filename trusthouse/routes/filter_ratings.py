from flask.views import MethodView
from trusthouse.models.review import Review
from flask import render_template, request
from ..extensions import app, db


class FilterByRating(MethodView):
    def post(self):
        user_rating_request = request.form['searchRating']
        user_rating_request = int(user_rating_request)
        check_request = db.session.query(
            db.session.query(Review).filter_by(rating=user_rating_request).exists()
        ).scalar()
        if check_request == False:
            void = 'No match found.'
            return render_template('searchReviewPage.html', void=void)
        get_ratings = db.session.query(Review).filter_by(rating=user_rating_request).all()
        return render_template('searchReviewPage.html', get_ratings=get_ratings)


app.add_url_rule(
    '/reviews/rating',
    view_func=FilterByRating.as_view(
        name='filter_rating'
    ),
)