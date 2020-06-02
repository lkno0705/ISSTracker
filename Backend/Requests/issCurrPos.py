import requests

def currPos():
    #Get request to get the current position of ISS from 'http://api.open-notify.org/iss-now.json'
    response = requests.get("http://api.open-notify.org/iss-now.json")
    data = response.json()

    # read data from response
    latitude = data['iss_position']['latitude']
    longitude = data['iss_position']['longitude']

    # return values as XML
    return "<iss_position>" + latitude + "," + longitude + "</iss_position>"
