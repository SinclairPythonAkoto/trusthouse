from flask.views import MethodView
from trusthouse.models.review import Review
from flask import render_template
from ..extensions import app


class DisplayAllReviews(MethodView):
    def get(self):
        return render_template('searchReviewPage.html')
    def post(self):
        get_reviews = Review.query.all()
        return render_template('searchReviewPage.html', get_reviews=get_reviews)


app.add_url_rule(
    '/viewReview',
    view_func=DisplayAllReviews.as_view(
        name='view_reviews'
    ),
)
app.add_url_rule(
    '/reviews/all', view_func=DisplayAllReviews.as_view(
        name='all_reviews'
    ),
)