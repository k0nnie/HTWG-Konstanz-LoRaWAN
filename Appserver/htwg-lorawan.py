#!/bin/sh

import threading
import urllib.request
import os
import subprocess
import sys
#import thread

class GetData:
  def __init__(self):
    self.pid = None

  def dataPolling(self):
    #catches any uplinks to TTN through our app
    self.pid = subprocess.Popen([sys.executable,  'receiver.py'])

  def getDataTTN(self):
    #subprocess.call('./getTTNdata.sh')
    pass

class TransformData:

  def DataFromXMinutes(rawdata): #stores data from the past X minutes seperatly so the most recent values can be used for transformation
    pass
  def transformData(rawdata): #contains main algorithm that needs to be callibrated to the real world situation
    pass
  def plotData(transformedData):
    pass
  def sendData(resultData): #send finished data or plots
    pass

def main():

  data = GetData()
  data.dataPolling()

  while(True):
    print("chose an option: \n")
    x = input()
    print(str(x))

if __name__ == "__main__":
  main()


#main

#routine to poll data in a thread and make it accessible for data transformation
#call transformation and plotting and sending in intervals of X minutes or via trigger (if new data arrives and gets processed)
