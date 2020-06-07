import requests
from datetime import datetime

# ISS current location API URL
ISS_LOCATION_URL = 'http://api.open-notify.org/iss-now.json'


def currPos():

    # Get request to get the current position of ISS from 'http://api.open-notify.org/iss-now.json'
    response = requests.get(ISS_LOCATION_URL)
    status = response.status_code

    # If an API call was not successful raise an exception.
    if status != 200:
        raise Exception ("ISS API unreachable.")
    else:
        data = response.json()

        # Read data from response
        latitude = data['iss_position']['latitude']
        longitude = data['iss_position']['longitude']
        timestamp = data['timestamp']

        # Convert timestamp to datetime and format datetime
        dt_obj = datetime.fromtimestamp(timestamp).strftime(format = "%Y-%m-%d %H-%M-%S")

        # Create a dictionary with the values latitude, longitude, timestamp and return data in dictionary
        iss_dict={'latitude': float(latitude), 'longitude': float(longitude), 'timestamp': dt_obj}
        return iss_dict
