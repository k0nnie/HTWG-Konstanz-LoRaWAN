					  
#!/bin/sh

import threading
import urllib.request
import os
import subprocess
import sys
#import thread

MicDevices = ["test_mic_0", "test_mic_1"]
DistanceDevices = ["test_distance_0", "test_distance_1"]

def getData(time, device): #requests all uplink data from a device that was sent [time] ago. 
    fullData = []
    resultData = []
    with open ('nodedata', 'r') as f:
        fullData = f.readlines()
        for line in fullData:
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
   # x = getData(None, "test_distance_0")
   # y = getData(None, 'test_distance_1')
   # fx = filterData(None, MicDevices)
   # fy = filterData(None, DistanceDevices)
   # print(str(fx) + "\n" + str(fy))
if __name__ == "__main__":
  main()






