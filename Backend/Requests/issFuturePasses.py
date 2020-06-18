import requests
from datetime import datetime

# ISS pass API URL
ISS_API_URL = 'http://api.open-notify.org/iss-pass.json'

def getFuturePass(longitude, latitude, number=10):

    location = {'lat': latitude,
                'lon': longitude,
                'n': number}

# read data from response and return future pass datetime
    response = requests.get(ISS_API_URL, params=location).json()

    if 'response' in response:
        data = []
        for a in response['response']:
            futurePass = a['risetime']
            futurePassDatetime = datetime.utcfromtimestamp(futurePass).strftime(format="%Y-%m-%d %H-%M-%S")
            data.append(futurePassDatetime)
        return data
    else:
        raise Exception ("No results found")
