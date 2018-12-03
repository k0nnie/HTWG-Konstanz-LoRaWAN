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

MicDevices = ["test_mic_0", "test_mic_1"]
DistanceDevices = ["test_distance_0", "test_distance_1"]
AllDevices = MicDevices + DistanceDevices

LAST30SECONDS = datetime.timedelta(seconds=30)
LAST5MINUTES = datetime.timedelta(minutes=5)
LASTHOUR = datetime.timedelta(hours=1)
LAST2HOURS = datetime.timedelta(hours=2)
LASTDAY = datetime.timedelta(days=1)
LASTWEEK = datetime.timedelta(weeks=1)


def timeToDatetime(time):
    tmp = str(time).replace(":" , "-").replace("T" , "-").replace("." , "-")
    tmp = tmp.split("-")
    result = datetime.datetime(int(tmp[0]),int(tmp[1]), int(tmp[2]), int(tmp[3]), int(tmp[4]), int(tmp[5])) #ignoring microseconds to evade possible crashes
   # print(str(result))
    return result

def getData(time, device): #requests all uplink data from a device that was sent [time] ago.
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


def filterData(time, devices):
    data = []
    for device in devices:
        data.append(getData(time, device))
    return data

def transformMicData(data): #creates array from messages, decodes payload, change time format to date:hh:mm:ss, 
  pass

def transformDistanceData():
  pass

def evaluateData(tMicData, tdistanceData):
  pass

def sendData(resultData): #send finished data or plots
  pass #change time to gmt+1

def main():


    x = getData(LAST2HOURS, "test_distance_0")
    print(str(x))
   # y = getData(None, 'test_distance_1')
   # fx = filterData(None, MicDevices)
   # fy = filterData(None, DistanceDevices)
   # print(str(fx) + "\n" + str(fy))
if __name__ == "__main__":
  main()






