from flask.views import MethodView
from flask import render_template
from ..extensions import app


class LandingPage(MethodView):
    def get(self):
        return render_template('landingPage.html')


app.add_url_rule(
    '/',
    view_func=LandingPage.as_view(
        name='landingpage'
    ),
)