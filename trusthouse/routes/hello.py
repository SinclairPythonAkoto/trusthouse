from flask.views import MethodView
from ..extensions import app


class HelloWorld(MethodView):
    def get(self):
        return 'Hello world!'


app.add_url_rule('/hello', view_func=HelloWorld.as_view(name='hello_world'))