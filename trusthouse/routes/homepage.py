from flask.views import MethodView
from flask import render_template
from ..extensions import app


class Home(MethodView):
    def get(self):
        return render_template('homePage.html')


app.add_url_rule(
    '/home',
    view_func=Home.as_view(
        name='homepage'
    ),
)