from flask import Flask


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trusthouse.sqlite3"
app.config["TRACK_MODIFICATIONS"] = True

# user interface
import trusthouse.routes.welcome_screen
import trusthouse.routes.homepage
import trusthouse.routes.create_review
import trusthouse.routes.display_reviews
import trusthouse.routes.display_locations
import trusthouse.routes.filter_ratings
import trusthouse.routes.filter_door
import trusthouse.routes.filter_street
import trusthouse.routes.filter_location
import trusthouse.routes.filter_postcode
import trusthouse.routes.trust_map
import trusthouse.routes.upload_address
# backend api
import trusthouse.api.display_addresses
import trusthouse.api.display_reviews
import trusthouse.api.filter_tenant
import trusthouse.api.filter_neighbour
import trusthouse.api.filter_visitor
import trusthouse.api.filter_rating
import trusthouse.api.filter_door
import trusthouse.api.filter_street
import trusthouse.api.filter_location
import trusthouse.api.filter_postcode
# create new address via backend api
import trusthouse.api.new_address