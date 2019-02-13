from datetime import date, tzinfo, timedelta
import time
import datetime
import threading
import urllib.request
import os
import subprocess
import sys
#import thread
import base64
import codecs

MICDEVICES = ["test_mic_0", "test_mic_1"]
DISTANCEDEVICES = ["test_distance_0", "test_distance_1"]
#WLANDEVICE = []
ALLDEVICES = MICDEVICES + DISTANCEDEVICES

#timedeltas to request the latest data
LAST30SECONDS = datetime.timedelta(seconds=30)
LAST5MINUTES = datetime.timedelta(minutes=5)
LASTHOUR = datetime.timedelta(hours=1)
LAST2HOURS = datetime.timedelta(hours=2)
LASTDAY = datetime.timedelta(days=1)
LASTWEEK = datetime.timedelta(weeks=1)
ALLTIME = datetime.timedelta(days=99999) #roughly 274 years :)

NODEDATA = 'nodedata'
CURRENTDATA = 'currentdata'
LASTDATA = 'lastData'

#index to get specifc data of uplink msg
APP_ID=0
DEV_ID=1
HARDWARE_SERIAL=2
PORT=3
COUNTER=4
PAYLOAD_RAW=5
META_DATA=6

MIC_0 = 20
MIC_1 = 60
MIC_2 = 100
MIC_3 = 140
MIC_4 = 180

MIN_DISTANCE_TRIGGER = 150 #value for distance sensor that counts as 1 
SENSOR_SENSITIVITY = 0.5 #mean of 1, 0 values that we count as people standing in front of the sensor over a period of time

WEIGHT_DISTANCE_LEFT = 3
WEIGHT_DISTANCE_RIGHT = 3
WEIGHT_MIC_DATA = 1

def readCurData():
    with open (NODEDATA, 'r+') as f:
        lines = f.readlines()
        deviceandmessage = {}
        for line in lines:
            line = line.split(",")
            #if message isnt older than 5minutes?
            payload = str(line[PAYLOAD_RAW])[14:-1]
            device = str(line[DEV_ID])[9:-1]
            deviceandmessage[device] = payloadConverter(payload)
    return deviceandmessage

def readLastData():
    with open (LASTDATA, 'r+') as f:
        line = f.readlines()
        lastDataLeft = line[0]
        lastDataRight = line[1]
    lastDataLeft = lastDataLeft.replace("[", "")
    lastDataLeft = lastDataLeft.replace("]", "")
    lastDataLeft = lastDataLeft.replace(" ", "")
    lastDataLeft = lastDataLeft.split(",")
    lastDataRight = lastDataRight.replace("[", "")
    lastDataRight = lastDataRight.replace("]", "")
    lastDataRight = lastDataRight.replace(" ", "")
    lastDataRight = lastDataRight.split(",")
    return lastDataLeft, lastDataRight
       # line = line.replace("]", "")
        #line = line.replace("[", "")
    #return list(map(int, str(line)))

def meanMic(mic):
    values = []
    values = [mic[i:i+2] for i in range(0, len(mic), 2)]
    mean = 0
    for value in values:
        mean = mean + int(value, 16)
    mean = mean / len(values)
    return mean

def volume(mean):
    volume = 0
    if mean >= MIC_0:
        volume = 1
    if mean >= MIC_1:
        volume = 2
    if mean >= MIC_2:
        volume = 3
    if mean >= MIC_3:
        volume = 4
    if mean >= MIC_4:
        volume = 5
    return volume

def evaluateMicData(data):
    mics = []
    for entry in data:
        if "mic" in entry:
            mics.append(entry)
    mean = 0
    for mic in mics:
        mean = mean + meanMic(data[mic])
    mean = mean / len(mics)
    result = volume(mean)
    return result

def payloadConverter(payload):
    decoded = base64.b64decode(payload) #now in hex representation
    decodedhex = decoded.hex()
    return decodedhex

def calculateDistance(value):
    result = 0
    if value <= MIN_DISTANCE_TRIGGER:
        result = 1
    return result

def transformDistanceData(dist):
    values = []
    result = []
    values = [dist[i:i+2] for i in range(0, len(dist), 2)] #splits payload into bytes
    for value in values:
        value = int(value, 16)
        value = calculateDistance(value)
        result.append(value)
    return result[:int(len(result)/2)], result[int(len(result)/2):] #splits list in left and right at n/2 elements

def getResult(deviceValues, devices, lastDataLeft, lastDataRight):
    print("test")
    left = []
    right = []
    #laenge der wirklichen queue
    queueLeft = 0
    queueRight = 0
    #anzahl der Zahlen > SENSOR_SENSITIVITY
    countQueueLeft = 0
    countQueueRight = 0
    #laenge der last queue
    lastQueueLeft = 0
    lastQueueRight = 0
    #anazhl der Zahlen > SENSOR_SENSITIVITY der last queue
    countLastQueueLeft = 0
    countLastQueueRight = 0
    foundZero = False
    for device in devices:
        values = deviceValues[device]
        tmpLeft = values[0]
        tmpRight = values[1]
        sumLeft = 0
        sumRight = 0
        for element in tmpLeft: #same amount of values in tmpLeft and tmpRight
            sumLeft = sumLeft + element
        for element in tmpRight:
            sumRight = sumRight + element
        left.append(sumLeft / len(tmpLeft))
        right.append(sumRight / len(tmpRight))
    print("left: " + str(left) + " right " + str(right))
    with open (LASTDATA, "w+") as f:
        f.write(str(left) + "\n")
        f.write(str(right))
    for ele in left:
        if ele >= SENSOR_SENSITIVITY:
            countQueueLeft = countQueueLeft + 1
            if(not foundZero):
                queueLeft = queueLeft + 1
        else:
            foundZero = True
    foundZero = False
    for ele in right:
        if ele >= SENSOR_SENSITIVITY:
            countQueueRight = countQueueRight + 1
            if(not foundZero):
                queueRight = queueRight + 1
        else:
            foundZero = True
    

    foundZero = False
    for ele in lastDataLeft:
        if float(ele) >= SENSOR_SENSITIVITY:
            lastQueueLeft = lastQueueLeft + 1
            if(not foundZero):
                countLastQueueLeft = countLastQueueLeft + 1
        else:
            foundZero = True
    foundZero = False
    for ele in lastDataRight:
        if float(ele) >= SENSOR_SENSITIVITY:
            lastQueueRight = lastQueueRight + 1
            if (not foundZero):
                countLastQueueRight = countLastQueueRight + 1
        else:
            foundZero = True

    #pruefen, ob eine Luecke von genau 1 (nicht am Ende) entstanden ist, dann alte Laenge der queue behalten
    #aendert nur den queue wert, nicht die last data fuer naechsten aufruf
    countRestQueue = 0
    if((lastQueueLeft - countQueueLeft) == 1):
        if((len(left)) >= countLastQueueLeft):
            for element in left[countLastQueueLeft:]:
                if(element < SENSOR_SENSITIVITY):
                    countRestQueue = countRestQueue + 1
                else:
                    countRestQueue = 0
            if(countRestQueue < 2):
                if(left[countLastQueueLeft - 1] >= SENSOR_SENSITIVITY):
                    queueLeft = countLastQueueLeft

    print("Queue Left: " + str(queueLeft))
    return queueLeft, queueRight

def evaluateDistanceData(data, lastDataLeft, lastDataRight):
    devices = []
    deviceValues = {}
    for entry in data:
        if "dist" in entry:
            devices.append(entry)
    devices.sort()
    for device in devices:
        deviceValues[device] = transformDistanceData(data[device])
    #save current data for next step
    #with open (LASTDATA, "w+") as f:
    #    for key in deviceValues:
    #        f.write(str(deviceValues[key][0]))
    #        f.write(str(deviceValues[key][1]))
    return getResult(deviceValues, devices, lastDataLeft, lastDataRight)

def evaluateData(micData, leftQueue, rightQueue):
    result = round(((leftQueue * WEIGHT_DISTANCE_LEFT + rightQueue * WEIGHT_DISTANCE_RIGHT + micData * WEIGHT_MIC_DATA) / (WEIGHT_DISTANCE_LEFT + WEIGHT_DISTANCE_RIGHT + WEIGHT_MIC_DATA)) * 20, 2)
    return result

def sendData(resultData):
  pass #change time to gmt+1

def main():
    print("test main")
    data = readCurData()
    lastDataLeft, lastDataRight = readLastData()
    print("read")
    print(str(data))
    print(str(lastDataLeft) + str(lastDataRight))
    micData = evaluateMicData(data)
    print(micData)
    leftQueue, rightQueue = evaluateDistanceData(data, lastDataLeft, lastDataRight)
    print("ql: " + str(leftQueue) + " rq: " + str(rightQueue))
   # result = round(((micData * 20) + (leftQueue * 20) + (rightQueue * 20)) / 3, 2)
    #print(result)
    result = evaluateData(micData, leftQueue, rightQueue)
    print(str(result))
    os.remove(CURRENTDATA)
    #with open(CURRENTDATA, "w+") as f:
    #    f.write("MicData: " + str(micData) + "\n")
     #   f.write("Left Queue: " + str(leftQueue) + ", Right Queue: " + str(rightQueue) + "\n")
    with open(CURRENTDATA, "w+") as f:
        f.write(str(result))
if __name__ == "__main__":
  main()
