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


def readCurData():
    with open ('currentData', 'r') as f:
        lines = f.readlines()
        deviceandmessage = {}
        for line in lines:
            line = line.split(",")
            #if message isnt older than 5minutes?
#            print(str(line[PAYLOAD_RAW])[14:-1])
            payload = str(line[PAYLOAD_RAW])[14:-1]
#            print("raw trimmed: " + payload)
#            print("decoded: " + payloadConverter(payload))
            device = str(line[DEV_ID])[9:-1]
            deviceandmessage[device] = payloadConverter(payload)
        for entry in deviceandmessage:
            print(entry + " " + deviceandmessage[entry])

def transformMicData():
    pass


def payloadConverter(payload):
    decoded = base64.b64decode(payload) #now in hex representation
    decodedhex = decoded.hex()
    return decodedhex

def transformDistanceData(data):
    for value in data:
        payload = payloadConverter(value)


def evaluateData(tMicData, tdistanceData):
    pass

def sendData(resultData):
  pass #change time to gmt+1

def main():
    readCurData()

if __name__ == "__main__":
  main()
