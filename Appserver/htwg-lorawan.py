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

MIC_0 = 20
MIC_1 = 60
MIC_2 = 100
MIC_3 = 140
MIC_4 = 180

def readCurData():
    with open ('nodedata', 'r') as f:
        lines = f.readlines()
        deviceandmessage = {}
        for line in lines:
            line = line.split(",")
            #if message isnt older than 5minutes?
            payload = str(line[PAYLOAD_RAW])[14:-1]
            device = str(line[DEV_ID])[9:-1]
            deviceandmessage[device] = payloadConverter(payload)
        for entry in deviceandmessage:
#            print(entry + " " + deviceandmessage[entry])
            pass
        return deviceandmessage

def meanMic(mic):
    values = []
    values = [mic[i:i+2] for i in range(0, len(mic), 2)]
    mean = 0
    for value in values:
        mean = mean + int(value, 16)
    mean = mean / len(values)
    print(mean)
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
    print(result)
    return result

def payloadConverter(payload):
    decoded = base64.b64decode(payload) #now in hex representation
    decodedhex = decoded.hex()
    return decodedhex

def transformDistanceData(data):
    pass


def evaluateData(tMicData, tdistanceData):
    pass

def sendData(resultData):
  pass #change time to gmt+1

def main():
    data = readCurData()
    evaluateMicData(data)

if __name__ == "__main__":
  main()
