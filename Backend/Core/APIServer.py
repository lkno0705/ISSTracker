from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from Backend.Requests.issCurrPos import currPos as issCurrentPosition
from Backend.Requests.rssFeed import rssFeed as rssFeed
from Backend.Requests.userPosition import getUserPosition as userPosition

import json

# Reimplementign Request Handler with custom Functions to handle GET Requests
class requestHandler(BaseHTTPRequestHandler):

    def _checkData(self, requestName, data):
        correct = False
        allowedKeys = {
            "ISSDB": [
                "startTime",
                "endTime",
                "numberOfItems"
            ],
            "ISSpos": None
        }

        if allowedKeys[requestName] is not None:
            if "params" in data and data["params"] is not None:
                for key in allowedKeys[requestName]:
                    correct = True if key in data["params"] and data["params"][key] is not None else False
                    if not correct:
                        break
            print(correct)
            return correct
        else:
            return True


    # Implements GET request
    def do_GET(self):
        # Dictonary containg Links assigned with their correct functions
        links = {
            "/ISSpos": issCurrentPosition,
            "/RSS": rssFeed,
            "/userPosition": userPosition,
            "/ISSDB": issCurrentPosition  # TODO: Has to be replaced with DB-request
        }
        try:
            content_len = int(self.headers.get('Content-Length'))
            body = json.loads(self.rfile.read(content_len))  # TODO: Json.loads has to be replaced with XML Parser
        except TypeError:
            body = {}
        print(self.path.split("/"))
        requestName = self.path.split("/")[1]
        # Executing function based on link; Works kinda like a switch case statement
        function = links.get(self.path)
        if function is not None and self._checkData(requestName, body):
            data = function()
            code = 200
        else:
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
