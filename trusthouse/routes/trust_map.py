import folium
from flask.views import MethodView
from trusthouse.models.maps import Maps
from geopy.geocoders import Nominatim
from ..extensions import app


class TrustHouseMap(MethodView):
    def get(self):
        coordinates = Maps.query.all()
        longitude = '-0.1244477'
        latitude = '51.4994252'
        location = float(latitude), float(longitude)
        map = folium.Map(
            location=location,
            tiles='Stamen Terrain',
            zoom_start=9,
        )
        geolocator = Nominatim(user_agent='geoapiExercises')
        for geocode in coordinates:
            long = geocode.lon
            lat = geocode.lat
            # get street name from latitude & longitude
            street_location = geolocator.reverse(f'{lat},{long}')
            street_location = str(street_location)
            data = street_location.split(',')

            # adding the points to the map
            folium.Marker(
                location=[float(lat), float(long)],
                popup=f'{data[1]}, {geocode.location.postcode.upper()}',
                tooltip='check address',
                icon=folium.Icon(color='red', icon='home', prefix='fa') 
            ).add_to(map)
        return map._repr_html_()


app.add_url_rule(
    '/trusthouse-map',
    view_func=TrustHouseMap.as_view(
        name='trust_house_map'
    ),
)