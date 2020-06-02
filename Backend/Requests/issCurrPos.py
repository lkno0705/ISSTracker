import requests

def currPos():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()
    latitude = data['iss_position']['latitude']
    longitude = data['iss_position']['longitude']
    return latitude + "," + longitude
