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

NODEDATA = 'nodedata'
CURRENTDATA = 'currentdata'

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

def readCurData():
    with open (NODEDATA, 'r') as f:
        lines = f.readlines()
        deviceandmessage = {}
        for line in lines:
            line = line.split(",")
            #if message isnt older than 5minutes?
            payload = str(line[PAYLOAD_RAW])[14:-1]
            device = str(line[DEV_ID])[9:-1]
            deviceandmessage[device] = payloadConverter(payload)
   # f.close()
    return deviceandmessage

def meanMic(mic):
    values = []
    values = [mic[i:i+2] for i in range(0, len(mic), 2)]
    mean = 0
    for value in values:
        mean = mean + int(value, 16)
    mean = mean / len(values)
    print("Mic mean: " + str(mean))
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
    #print(result)
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

def getResult(deviceValues, devices):
    left = []
    right = []
    queueLeft = 0
    queueRight = 0
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
    for ele in left:
        if ele >= SENSOR_SENSITIVITY:
            queueLeft = queueLeft + 1
        else:
            break
    for ele in right:
        if ele >= SENSOR_SENSITIVITY:
            queueRight = queueRight + 1
        else:
            break
    return queueLeft, queueRight

def evaluateDistanceData(data):
    devices = []
    deviceValues = {}
    for entry in data:
        if "dist" in entry:
            devices.append(entry)
    devices.sort()
    for device in devices:
        deviceValues[device] = transformDistanceData(data[device])
        #print(str(device) + str(deviceValues[device]))
   # leftqueue, rightqueue = getResult(deviceValues, devices)
    #print("queue left: " + str(leftqueue) + " queue right: " + str(rightqueue))
    return getResult(deviceValues, devices)

def evaluateData(tMicData, tdistanceData):
    pass

def sendData(resultData):
  pass #change time to gmt+1

def main():
    data = readCurData()
    micData = evaluateMicData(data)
    print(micData)
    leftQueue, rightQueue = evaluateDistanceData(data)
    print("ql: " + str(leftQueue) + " rq: " + str(rightQueue))
    os.remove(CURRENTDATA)
    with open(CURRENTDATA, "w+") as f:
        f.write("MicData: " + str(micData) + "\n")
        f.write("Left Queue: " + str(leftQueue) + ", Right Queue: " + str(rightQueue) + "\n")
if __name__ == "__main__":
  main()
