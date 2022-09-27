from re import template
from flask.views import MethodView
from flask import render_template, url_for
from ..extensions import app


class TrustHouseAPI(MethodView):
    def get(self):
        return render_template('trustHouseAPI.html')


app.add_url_rule(
    '/trusthouseAPI',
    view_func=TrustHouseAPI.as_view(
        name='trusthouse_api',
    ),
)