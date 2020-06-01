from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from Backend.Requests.issCurrPos import currPos as issCurrentPosition
from Backend.Requests.rssFeed import rssFeed as rssFeed
from Backend.Requests.userPosition import getUserPosition as userPosition

# Reimplementign Request Handler with custom Functions to handle GET Requests
class requestHandler(BaseHTTPRequestHandler):

    # Implements GET request
    def do_GET(self):
        # Dictonary containg Links assigned with their correct functions
        links = {
            "/ISSpos": issCurrentPosition,
            "/RSS": rssFeed,
            "/userPosition": userPosition
        }

        # Executing function based on link; Works kinda like a switch case statement
        function = links.get(self.path)
        if function is not None:
            data = function()
            code = 200
        else:
            # Setting Error Message
            data = '<?xml version="1.0" encoding="UTF-8"?>' \
                   '<message>' \
                   '<error>Error 400: Bad Request</error>' \
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
    server_address = ('', 8081)

    # Starting http server which handles every request in a seperate THREAD
    httpd = ThreadingHTTPServer(server_address, requestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
