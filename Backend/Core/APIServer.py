from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from Backend.Requests.issCurrPos import currPos as issCurrentPosition
from Backend.Requests.rssFeed import rssFeed as rssFeed
from Backend.Requests.ISSCountryPasses import ISScountryPasses
from Backend.Requests.userPosition import getUserPosition as userPosition
from Backend.Core.database import redisDB
from Backend.Requests.issPastPasses import pastPasses
from Backend.Requests.issFuturePasses import getFuturePass
from Backend.Core.XMLParser import reformatData, parseRequestParamsXMLToDic

import json

# Reimplementign Request Handler with custom Functions to handle GET Requests
class requestHandler(BaseHTTPRequestHandler):

    # checks request body
    def _checkData(self, requestName, data):
        correct = False
        allowedKeys = {
            "ISSDB": [
                "startTime",
                "endTime",
            ],
            "ISSpos": True,
            "AstrosOnISS": True,
            "GeoJson": [
                "country"
            ],
            "ISSCountryPasses": [
                "startTime",
                "endTime",
                "country"
            ],
            "RSS-Feed": [
                "time",
                "numberOfItems"
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


    # Implements GET request
    def do_GET(self):
        try:
            content_len = int(self.headers.get('Content-Length'))
            body = parseRequestParamsXMLToDic(self.rfile.read(content_len))
        except TypeError:
            body = None
        # print(self.path.split("/"))
        requestName = self.path.split("/")[1]

        code = 1
        if self._checkData(requestName.strip("?"), body):
            code = 200
            if self.path == "/?ISSDB":
                data = redisDB().getData(body, self.path.strip("/?"))
            elif self.path == "/?GeoJson":
                data = redisDB().getData(body, self.path.strip("/?"))
            elif self.path == "/?AstrosOnISS":
                data = redisDB().getData(body, self.path.strip("/?"))
            elif self.path == "/?ISSCountryPasses":
                data = ISScountryPasses(requestData=body)
            elif self.path == "/?RSS-Feed":
                data = redisDB().getData(requestData=body, requestName=self.path.strip("/?"))
            elif self.path == "/?ISSpastPasses":
                data = pastPasses().pastPasses(requestData=body)
            elif self.path == "/?ISSfuturePasses":
                data = getFuturePass(params=body["params"])
            elif self.path == "/?ISSpos":
                data = issCurrentPosition()

            data = reformatData(requestData=data, requestName=self.path.strip("/?"))

        else:
            # Setting Error Message if Body data is incorrect
            data = '<?xml version="1.0" encoding="UTF-8"?>' \
                   '<message>' \
                   '<error>Error 400: Bad Request</error>' \
                   '<description>Incorrect parameters!</description>' \
                   '</message>'
            code = 400
        if code == 1:
            # Setting Error Message
            data = '<?xml version="1.0" encoding="UTF-8"?>' \
                   '<message>' \
                   '<error>Error 400: Bad Request</error>' \
                   '<description></description>' \
                   '</message>'
            code = 400

        # set response code
        self.send_response(code=code)

        # set http header to define body content type as XML
        self.send_header('Content-type', 'text/xml')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # send body
        self.wfile.write(bytes(str(data), "utf-8"))



def startAPIServer():
    # Setting Server address to localhost:8081
    server_address = ('', 8082)

    # Starting http server which handles every request in a seperate THREAD
    httpd = ThreadingHTTPServer(server_address, requestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
