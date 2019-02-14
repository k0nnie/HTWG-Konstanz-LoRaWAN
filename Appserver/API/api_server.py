import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HOST_NAME = '192.52.33.75'
PORT_NUMBER = 8080

CURRENTDATA = "../currentdata"
DEBUGDATA = "../debugData"
PLOTRESULT = "../plotResult"

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/current': {'status': 200},
        }

        if self.path in paths:
            self.handle_http(paths[self.path]['status'], self.path)
        else:
            pass

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        data = ""
        with open(CURRENTDATA, "r") as f:
            nodeData = f.readlines()
        with open(DEBUGDATA, "r") as f:
            debugData = f.read()
        with open("main.html", "r") as f:
            main = f.read()
        with open(PLOTRESULT, "r") as f:
            plotResult = f.readlines()

        values = ""
        for i in range(len(plotResult)):
            plotResult[i] = plotResult[i][:-1]
            if i == 0:
                values = str(plotResult[0])
            else:
                values = values + "," + str(plotResult[i])

        count = ""
        for i in range(len(plotResult)):
            if i == 0:
                count = str(i)
            else:
                count = count + "," + str(i)

        message = main.format(Percentage=nodeData[0],PercentageQueueLeft=nodeData[1], PercentageQueueRight=nodeData[2], PercentageMic=nodeData[3], Count=str(count), Values=str(values))
        self.wfile.write(bytes(message, 'UTF-8'))

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
