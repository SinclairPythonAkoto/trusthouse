import requests

def get_postcode_coordinates(postcode):
    """
    Takes the user's postcode request and uses the OpenStreetMap API to get the latitude * longitude.
    Returns a JSON object or empyty list if there is no match from the response.
    """
    BASE_URL = 'https://nominatim.openstreetmap.org/search?format=json'

    response = requests.get(f"{BASE_URL}&postalcode={postcode}&country=united kingdom")
    data = response.json()

    return data