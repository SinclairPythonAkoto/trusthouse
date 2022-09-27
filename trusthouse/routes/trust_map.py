import folium
from flask.views import MethodView
from trusthouse.models.maps import Maps
from trusthouse.models.buisness import Business
from trusthouse.models.incident import Incident
from geopy.geocoders import Nominatim
from ..extensions import app


class TrustHouseMap(MethodView):
    def get(self):
        coordinates = Maps.query.all()
        business_data = Business.query.all()
        incident_reports = Incident.query.all()
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
                popup=f'{data[0]},\n{geocode.location.postcode.upper()}',
                tooltip='check address',
                icon=folium.Icon(color='red', icon='home', prefix='fa') 
            ).add_to(map)

        # add buisness markers to map
        for trusthouse_map in coordinates:
            for buisness in business_data:
                if trusthouse_map.address_id == buisness.address_id:
                    folium.Marker(
                        location=[float(trusthouse_map.lat), float(trusthouse_map.lon)],
                        popup=f'{buisness.name.upper()},\n{buisness.category},\n{buisness.contact},\n{buisness.place.postcode.upper()}',
                        tooltip='View Buisness',
                        icon=folium.Icon(color='green', icon='gbp', prefix='fa')
                    ).add_to(map)

        # add incident marker to map
        for trusthouse_map in coordinates:
            for report in incident_reports:
                if trusthouse_map.address_id == report.address_id:
                    folium.Marker(
                        location=[float(trusthouse_map.lat), float(trusthouse_map.lon)],
                        popup=f'{report.category.upper()},\n{report.description},\n{report.area.street},\n{report.area.postcode},\n{report.date}',
                        tooltip='View Incident',
                        icon=folium.Icon(color='orange', icon='exclamation-triangle', prefix='fa')
                    ).add_to(map)
             
        return map._repr_html_()


app.add_url_rule(
    '/map',
    view_func=TrustHouseMap.as_view(
        name='trust_house_map'
    ),
)
