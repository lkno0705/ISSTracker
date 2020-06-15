import requests

# Nominatum API
API_URL = 'https://nominatim.openstreetmap.org/search?'

def geocoder(address):
    params = {"q": address,
            "format": 'json',
            "limit": 1}

# GET request
    response = requests.get(API_URL, params=params)
    response.raise_for_status()

    data = response.json()

# raise an exception, if location doesn't exist
    if len(data)==0:
        raise Exception ("No results found")
    else:
        longitude = data[0]['lon']
        latitude = data[0]['lat']

# return values longitude, latitude
        return {'longitude': float(longitude),
                'latitude': float(latitude)}
