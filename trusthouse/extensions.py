from flask_sqlalchemy import SQLAlchemy
from trusthouse import app


db = SQLAlchemy()

db.init_app(app)