from network import LoRa
import socket
import time
import ubinascii
from lib import Microphone
import struct

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
TIME_PERIOD = 60

# create an ABP authentication params
# node_02
# dev_addr = struct.unpack(">l", ubinascii.unhexlify('26011A3A'))[0]
# nwk_swkey = ubinascii.unhexlify('D08901FD32BD9C9E06C9A87073DD5D75')
# app_swkey = ubinascii.unhexlify('B78A3E8F26596A39A229A6CA376C2312')
# test_mic_0
dev_addr = struct.unpack(">l", ubinascii.unhexlify('26011ABE'))[0]
nwk_swkey = ubinascii.unhexlify('E6EAE44B46C78A2AF65DAC5B88D87B08')
app_swkey = ubinascii.unhexlify('1F12C9110961AE5BF02E7CAD15C15224')

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

try:
    while True:
        start = time.time()
        print("starting measurement")
        message = []
        for i in range(30):
            start_time = time.time()
            level = int(Microphone.senseLevel() / 16)
            if level == -1:
                print("Something went wrong with the ultrasonic detection.")
                break
            message.append(level)
            print(level)
            time.sleep(1 - (time.time() - start_time))
        print(ubinascii.hexlify(bytearray(message)))
        # make the socket blocking
        # (waits for the data to be sent and for the 2 receive windows to expire)
        s.setblocking(True)

        # send some data
        s.send(bytes(message))

        # make the socket non-blocking
        # (because if there's no data received it will block forever...)
        s.setblocking(False)
        # get any data received (if any...)
        data = s.recv(64)
        print(data)
        time.sleep(TIME_PERIOD - int(time.time() - start))
except KeyboardInterrupt:
    s.close()
    exit(0)
