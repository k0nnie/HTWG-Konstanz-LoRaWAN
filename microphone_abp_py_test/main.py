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

# create an ABP authentication params
dev_addr = struct.unpack(">l", ubinascii.unhexlify('26011A3A'))[0]
nwk_swkey = ubinascii.unhexlify('D08901FD32BD9C9E06C9A87073DD5D75')
app_swkey = ubinascii.unhexlify('B78A3E8F26596A39A229A6CA376C2312')

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
        message = []
        for i in range(30):
            start_time = time.time()
            level = int(Microphone.senseLevel() / 16)
            message.append(level)
            time.sleep(1 - (time.time() - start_time))
            print(level)
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
        time.sleep(300 - (time.time() - start))
except KeyboardInterrupt:
#    s.close()
    exit(0)
