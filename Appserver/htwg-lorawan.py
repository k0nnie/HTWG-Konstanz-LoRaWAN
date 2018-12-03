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

MICDEVICES = ["test_mic_0", "test_mic_1"]
DISTANCEDEVICES = ["test_distance_0", "test_distance_1"]
ALLDEVICES = MICDEVICES + DISTANCEDEVICES

#timedeltas to request the latest data
LAST30SECONDS = datetime.timedelta(seconds=30)
LAST5MINUTES = datetime.timedelta(minutes=5)
LASTHOUR = datetime.timedelta(hours=1)
LAST2HOURS = datetime.timedelta(hours=2)
LASTDAY = datetime.timedelta(days=1)
LASTWEEK = datetime.timedelta(weeks=1)
ALLTIME = datetime.timedelta(days=99999) #roughly 274 years :)

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
def filterData(time, devices): #all data with filterData(ALLTIME, ALLDEVICES)
    data = []
    for device in devices:
        data.append(getData(time, device))
    return data

def transformMicData(data):
  pass

def transformDistanceData():
  pass

def evaluateData(tMicData, tdistanceData):
  pass

def sendData(resultData):
  pass #change time to gmt+1

def main():


    x = getData(LAST2HOURS, "test_distance_0")
    print(str(x))

if __name__ == "__main__":
  main()






