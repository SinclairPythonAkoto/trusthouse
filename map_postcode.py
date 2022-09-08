# test to get the longitude & latitude of a postcode and then plot it in a map


import requests
from geopy.geocoders import Nominatim
from pprint import pprint

BASE_URL = 'https://nominatim.openstreetmap.org/search?format=json'

# initialize Nominatim API
geolocator = Nominatim(user_agent='geoapiExercises')


# postcode = 'SW1A 0AA'
london = 'cr0 2up'

# response = requests.get(f"{BASE_URL}&postalcode={postcode}&country=united kingdom")
response2 = requests.get(f"{BASE_URL}&postalcode={london}&country=united kingdom")

# data = response.json()
data2 = response2.json()
pprint(data2)

# scotland location
# latitude = data[0].get('lat')
# longitude = data[0].get('lon')

# london location
latitude2 = data2[0].get('lat')
longitude2 = data2[0].get('lon')

# get info from longitude & latitude
# location = geolocator.reverse(latitude2 + ',' + longitude2)
location = geolocator.reverse(f'{latitude2},{longitude2}')

location = str(location)

data = location.split(',')
print(data[1])
# print(type(location))

# print((longitude, latitude))

import folium

# scotland = float(latitude), float(longitude)
london = float(latitude2), float(longitude2)

# # creating a map opbject
# m = folium.Map(
#     location=scotland,
#     width=800,
#     height=400,
# )

# folium.Map(scotland, popup='Glasgow Postcode').add_to(m)
# folium.Map(london, popup='London Postcode').add_to(m)

# m._repr_html_()


'''
you can change the layout of the map inside the Map object you can add:

# for black & white map
tiles='Stamen Toner'

# hybrid map
tiles='Stamen Terrain'


example in a flask route

@app.route('/map')
def show_map():
    postcode = 'G42 9AY'
    response = requests.get(f"{BASE_URL}&postalcode={postcode}&country=united kingdom")
    data = response.json()
    latitude = data[0].get('lat')
    longitude = data[0].get('lon')
    scotland = float(latitude), float(longitude)
    map = folium.Map(
        location=scotland,
        tiles='Stamen Terrain',
        zoom_start=12,
    )
    folium.Marker(
        location=scotland,   # or [45.54356, 12.45678]
        popup='Glasgow Location',
    ).add_to(map)
    return map._repr_html_()

'''