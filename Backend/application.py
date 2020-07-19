from flask import Flask, Response
from flask import request as frequest
from Backend.Requests.issCurrPos import currPos as issCurrentPosition
from Backend.Requests.rssFeed import rssFeed as rssFeed
from Backend.Requests.ISSCountryPasses import ISScountryPasses
from Backend.Requests.userPosition import getUserPosition as userPosition
from Backend.Core.database import redisDB
from Backend.Requests.issPastPasses import pastPasses
from Backend.Requests.issFuturePasses import getFuturePass
from Backend.Core.XMLParser import reformatData, parseRequestParamsXMLToDic, XMLvalidate
from Backend.Requests.addressGeocoding import geocoder
import multiprocessing
from Backend.Core.polling import polling
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path='')
cors = CORS(app)
BadRequest = '<?xml version="1.0" encoding="UTF-8"?>' \
             '<message>' \
             '<error>Error 400: Bad Request</error>' \
             '<description></description>' \
             '</message>'

multiprocessing.Process(target=polling).start()


def makeResponse(data, status):
    return Response(data, status=status, content_type='text/xml')  # headers={}


def _checkData(requestName, data):
    correct = False
    allowedKeys = {
        "ISSDB": [
            "startTime",
            "endTime",
        ],
        "ISSpos": True,
        "AstrosOnISS": True,
        "CountryList": True,
        "GeoJson": [
            "country"
        ],
        "ISSCountryPasses": [
            "startTime",
            "endTime",
            "country"
        ],
        "RSS-Feed": [
            "startID",
            "endID"
        ],
        "ISSpastPasses": [
            "latitude",
            "longitude",
            "radius"
        ],
        "ISSfuturePasses": [
            "latitude",
            "longitude",
            "number"
        ],
        "GeocodingAddress": [
            "q"
        ]
    }

    if allowedKeys[requestName] is not None:
        if data is not None:
            if "params" in data and data["params"] is not None:
                for key in allowedKeys[requestName]:
                    correct = True if key in data["params"] and data["params"][key] is not None else False
                    if not correct:
                        break
            # print(correct)
            return correct
        elif allowedKeys[requestName] is True:
            return True
        else:
            return False
    else:
        return False


@app.route('/<requestName>', methods=['GET', 'POST'])
@cross_origin()  # Adds 'Access-Control-Allow-Origin': '*' to answer
def request(requestName):
    if frequest.method == 'GET':
        if requestName == 'AstrosOnISS':
            return makeResponse(
                data=reformatData(requestData=redisDB().getData(None, requestName), requestName=requestName),
                status=200)
        elif requestName == 'ISSpos':
            return makeResponse(data=reformatData(requestData=issCurrentPosition(), requestName=requestName),
                                status=200)
        elif requestName == "CountryList":
            return makeResponse(
                data=reformatData(requestData=redisDB().getData(None, requestName), requestName=requestName),
                status=200)
        else:
            return makeResponse(BadRequest, 400)

    elif frequest.method == 'POST':
        resp = ""
        try:
            body = parseRequestParamsXMLToDic(frequest.data)
        except TypeError:
            body = None

        if body == "INVALID XML" or not _checkData(requestName=requestName, data=body):
            return makeResponse(BadRequest, 400)
        else:
            if requestName == "ISSCountryPasses":
                resp = reformatData(requestData=ISScountryPasses(requestData=body), requestName=requestName)
            elif requestName == "ISSDB":
                resp = reformatData(requestData=redisDB().getData(body, requestName), requestName=requestName)
            elif requestName == "GeoJson":
                resp = reformatData(requestData=redisDB().getData(body, requestName), requestName=requestName)
            elif requestName == "RSS-Feed":
                resp = reformatData(requestData=redisDB().getData(requestData=body, requestName=requestName),
                                    requestName=requestName)
            elif requestName == "ISSpastPasses":
                resp = reformatData(requestData=pastPasses().pastPasses(requestData=body), requestName=requestName)
            elif requestName == "ISSfuturePasses":
                resp = reformatData(requestData=getFuturePass(params=body["params"]), requestName=requestName)
            elif requestName == "GeocodingAddress":
                resp = reformatData(requestData=geocoder(params=body["params"]), requestName=requestName)
            else:
                return makeResponse(BadRequest, 400)
            if XMLvalidate(resp) and not resp == "":
                return makeResponse(data=resp, status=200)
            else:
                return makeResponse(data='<?xml version="1.0" encoding="UTF-8"?>' \
                                  '<message>' \
                                  '<error>Error 500: Bad XML Response</error>' \
                                  '<description>An Error occured while validating the XML file</description>' \
                                  '</message>', status=500)
