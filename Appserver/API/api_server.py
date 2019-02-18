import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import numpy as np

HOST_NAME = '192.52.33.75'
PORT_NUMBER = 8080

CURRENTDATA = "../currentdata"
CURRENTMOVEMENT = "../currentMovement"
DEBUGDATA = "../debugData"
PLOTRESULT = "../plotResult"
PLOTRESULTQUEUELEFT = "../plotResultQueueLeft"
PLOTRESULTQUEUERIGHT = "../plotResultQueueRight"
PLOTRESULTMIC = "../plotResultMic"
RAWDATA = "../rawData"

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/current': {'status': 200},
            '/dev':{ 'status': 200},
        }

        if self.path in paths:
            self.handle_http(paths[self.path]['status'], self.path)
        else:
            pass

    def convertResult(self, result):
        values = ""
        for i in range(len(result)):
            result[i] = result[i][:-1]
            if i == 0:
                values = str(result[0])
            else:
                values = values + "," + str(result[i])

        count = ""
        for i in range(len(result)):
            if i == 0:
                count = str(i)
            else:
                count = count + "," + str(i)

        return values, count

    def convertMovement(self, movement):
        if(str(movement[0]) == "1\n"):
            movementLeft = "Warteschlange <b>links</b> <font color=green>bewegt sich</font>"
        else:
            movementLeft = "Warteschlange <b>links</b> <font color=red>bewegt sich nicht</font>"

        if(str(movement[1]) == "1"):
            movementRight = "Warteschlange <b>rechts</b> <font color=green>bewegt sich</font>"
        else:
            movementRight = "Warteschlange <b>rechts</b> <font color=red>bewegt sich nicht</font>"
        return movementLeft, movementRight

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = ""
        if(str(path) == "/current"):
            data = ""
            with open(CURRENTDATA, "r") as f:
                nodeData = f.readlines()
            with open(DEBUGDATA, "r") as f:
                debugData = f.read()
            with open("main.html", "r") as f:
                main = f.read()
            with open(PLOTRESULT, "r") as f:
                plotResult = f.readlines()
            valuesResult, countResult = self.convertResult(plotResult)
            with open(CURRENTMOVEMENT, "r") as f:
                movement = f.readlines()

            movementLeft, movementRight = self.convertMovement(movement)
            message = main.format(Percentage=nodeData[0], Count=countResult, Values=valuesResult, MovementLeft=movementLeft, MovementRight=movementRight)
        elif(str(path) == "/dev"):
            data = ""
            with open(CURRENTDATA, "r") as f:
                nodeData = f.readlines()
            with open(DEBUGDATA, "r") as f:
                debugData = f.read()
            with open("dev.html", "r") as f:
                dev = f.read()
            with open(PLOTRESULT, "r") as f:
                plotResult = f.readlines()
            valuesResult, countResult = self.convertResult(plotResult)
            with open(PLOTRESULTQUEUELEFT, "r") as f:
                plotResultQueueLeft = f.readlines()
            valuesResultQueueLeft, countResultQueueLeft = self.convertResult(plotResultQueueLeft)
            with open(PLOTRESULTQUEUERIGHT, "r") as f:
                plotResultQueueRight = f.readlines()
            valuesResultQueueRight, countResultQueueRight = self.convertResult(plotResultQueueRight)
            with open(PLOTRESULTMIC, "r") as f:
                plotResultMic = f.readlines()
            valuesResultMic, countResultMic = self.convertResult(plotResultMic)
            with open(CURRENTMOVEMENT, "r") as f:
                movement = f.readlines()
            with open(RAWDATA, "r") as f:
                rawData = f.readlines()

           # print(str(plotResult))
           # valuesResult = np.fft.fft(plotResult)
           # print(str(valuesResult))

            movementLeft, movementRight = self.convertMovement(movement)
            message = dev.format(Percentage=nodeData[0] ,PercentageQueueLeft=nodeData[1], PercentageQueueRight=nodeData[2], PercentageMic=nodeData[3], Count=countResult, Values=valuesResult, CountQueueLeft=countResultQueueLeft, ValuesQueueLeft=valuesResultQueueLeft, CountQueueRight=countResultQueueRight, ValuesQueueRight=valuesResultQueueRight, CountMic=countResultMic, ValuesMic=valuesResultMic, MovementLeft=movementLeft, MovementRight=movementRight, RawDataLeft=rawData[0], RawDataRight=rawData[1], RawDataMic=rawData[2])

            #message = dev

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
