#!/bin/sh
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

#index to get specifc data of uplink msg
APP_ID=0
DEV_ID=1
HARDWARE_SERIAL=2
PORT=3
COUNTER=4
PAYLOAD_RAW=5
META_DATA=6


#transforms the time string from our uplink message to datetime
def timeToDatetime(time):
    tmp = str(time).replace(":" , "-").replace("T" , "-").replace("." , "-")
    tmp = tmp.split("-")
    result = datetime.datetime(int(tmp[0]),int(tmp[1]), int(tmp[2]), int(tmp[3]), int(tmp[4]), int(tmp[5])) #ignoring microseconds to evade possible crashes
    return result

#loads data from nodedata file if time and device requirements are met.
def getData(time, device):
    fullData = []
    resultData = []
    with open ('nodedata', 'r') as f:
        fullData = f.readlines()
        for line in fullData:
            lineTime = line.split(',')
            lineTime = lineTime[-1]
            lineTime = timeToDatetime(lineTime)
            if (datetime.datetime.now() - lineTime) <= time:
                if line.startswith(str(device)):
                    resultData.append(line)
    return resultData

#allows to filter data to match multiple devices and one timedelta
def filterData(time, devices): #all data with filterData(ALLTIME, ALLDEVICES) but better (ALLTIME, MICDEVICES) + (ALLTIME, DISTANCEDEVICES)
    data = []
    for device in devices:
        data.append(getData(time, device))
    return data

def transformMicData():
    pass

def transformDistanceData(data):
    payloadConverter(value)

def payloadConverter(msg):
    tmp  = str(msg).split(",")
    payload = tmp[PAYLOAD_RAW]
    print(payload)
    decoded = base64.b64decode(payload) #now in hex representation
    decodedhex = ""
    for c in decoded:
        print(str(hex(c))[2:])
        decodedhex = decodedhex + str(hex(c))[2:]
    print(decodedhex)

def evaluateData(tMicData, tdistanceData):
    pass

def sendData(resultData):
  pass #change time to gmt+1

def main():

    x = getData(LASTWEEK, "test_distance_0")
    transformDistanceData(x)

if __name__ == "__main__":
  main()
