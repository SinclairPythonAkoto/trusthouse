from flask.views import MethodView
from trusthouse.models.address import Address
from flask import render_template
from ..extensions import app


class DisplayListedLocations(MethodView):
    def post(self):
        listed_locations = Address.query.all()
        return render_template('searchReviewPage.html', listed_locations=listed_locations)


app.add_url_rule(
    '/reviews/all/location',
    view_func=DisplayListedLocations.as_view(
        name='listed_locations'
    )
)