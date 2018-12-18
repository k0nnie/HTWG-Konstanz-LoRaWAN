import time
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = '192.52.33.75'
PORT_NUMBER = 8080

CURRENTDATA = "../Appserver/currentdata"

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/current': {'status': 200},
           # '/bar': {'status': 302},
           # '/baz': {'status': 404},
           # '/qux': {'status': 500}
        }

        if self.path in paths:
            #self.respond(paths[self.path])
            self.handle_http(paths[self.path]['status'], self.path)
        else:
 #           self.respond({'status': 500})
            pass

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        data = ""
        with open(CURRENTDATA, "r") as f:
            data = f.read()

        content = '''
        <html><head><title>HTWG LoraWAN</title></head>
        <body>
        <p>Current Data: {}</p>
        </body></html>
        '''.format(data)
        self.wfile.write(bytes(content, 'UTF-8'))

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
