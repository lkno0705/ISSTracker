import requests
from datetime import datetime

# ISS pass API URL
ISS_API_URL = 'http://api.open-notify.org/iss-pass.json'

def getFuturePass(params):

    location = {'lat': params['latitude'],
                'lon': params['longitude'],
                'n': params['number'] if 'number' in params else 5}

# read data from response and return future pass datetime
    response = requests.get(ISS_API_URL, params=location).json()

    if 'response' in response:
        data = []
        for a in response['response']:
            futurePass = a['risetime']
            passDuration = a['duration']
            futurePassDatetime = datetime.utcfromtimestamp(futurePass).strftime(format="%Y-%m-%d %H-%M-%S")
            dict = {'futurePassDatetime': futurePassDatetime,
                    'duration': passDuration}
            data.append(dict)
        return data
    else:
        raise Exception ("No results found")
