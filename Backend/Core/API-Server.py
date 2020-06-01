from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from Backend.Requests.issCurrPos import currPos as issCurrentPosition
from Backend.Requests.rssFeed import rssFeed as rssFeed
from Backend.Requests.userPosition import getUserPosition as userPosition

class requestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        links = {
            "ISSpos": issCurrentPosition,
            "RSS": rssFeed,
            "userPosition": userPosition
        }
        try:
            data = links.get(self.path)
            code = 200
        except:
            data = '<?xml version="1.0" encoding="UTF-8"?>' \
                   '<message>' \
                   '<error>Error 400: Bad Request</error>' \
                   '</message>'
            code = 400

        self.send_response(code=code)
        self.send_header('Content-type', 'text/xml')
        self.end_headers()
        self.wfile.write(bytes(str(data), "utf-8"))



def startAPIServer():
    server_address = ('', 8081)
    httpd = ThreadingHTTPServer(server_address, requestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    startAPIServer()