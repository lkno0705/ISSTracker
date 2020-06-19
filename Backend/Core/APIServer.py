from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from Backend.Requests.issCurrPos import currPos as issCurrentPosition
from Backend.Requests.rssFeed import rssFeed as rssFeed
from Backend.Requests.ISSCountryPasses import ISScountryPasses
from Backend.Requests.userPosition import getUserPosition as userPosition
from Backend.Core.database import redisDB
from Backend.Requests.issPastPasses import pastPasses
from Backend.Requests.issFuturePasses import getFuturePass

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
            "ISSCountryPass": [
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
        # Dictonary containg Links assigned with their correct functions
        linksWithoutParams = {
            "/ISSpos": issCurrentPosition,
            "/RSS": rssFeed,
            "/userPosition": userPosition,
        }
        try:
            content_len = int(self.headers.get('Content-Length'))
            body = json.loads(self.rfile.read(content_len))  # TODO: Json.loads has to be replaced with XML Parser
        except TypeError:
            body = None
        # print(self.path.split("/"))
        requestName = self.path.split("/")[1]
        # Executing function based on link; Works kinda like a switch case statement
        function = linksWithoutParams.get(self.path)

        code = 1
        if function is not None and body is None:
            data = function()
            code = 200
        else:
            if self._checkData(requestName, body):
                code = 200
                if self.path == "/ISSDB":
                    data = redisDB().getData(body, self.path.strip("/"))
                elif self.path == "/GeoJson":
                    data = redisDB().getData(body, self.path.strip("/"))
                elif self.path == "/AstrosOnISS":
                    data = redisDB().getData(body, self.path.strip("/"))
                elif self.path == "/ISSCountryPass":
                    data = ISScountryPasses(requestData=body)
                elif self.path == "/RSS-Feed":
                    data = redisDB().getData(requestData=body, requestName=self.path.strip("/"))
                elif self.path == "/ISSpastPasses":
                    data = pastPasses().pastPasses(requestData=body)
                elif self.path == "/ISSfuturePasses":
                    data = getFuturePass(params=body["params"])
                # TODO: parse data to XML with XML parser
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
