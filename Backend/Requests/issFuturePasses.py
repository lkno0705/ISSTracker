import requests
from datetime import datetime
import pytz

ISS_API_URL = 'http://api.open-notify.org/iss-pass.json'

def getFuturePass(longitude, latitude, number=10):

    location = {'lat': latitude,
                'lon': longitude,
                'n': number}

    response = requests.get(ISS_API_URL, params=location).json()
#    return response
    if 'response' in response:
        data = []
        for a in response['response']:
            futurePass = a['risetime']
#        futurePass = response['response'][0]['risetime']
            futurePassDatetime = datetime.fromtimestamp(futurePass, tz=pytz.utc)
            data.append(futurePassDatetime)
        return data
    else:
        raise Exception ("No results found")



print (getFuturePass(122.3, 45))
