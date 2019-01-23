from network import LoRa
import socket
import time
import ubinascii
from lib import Ultrasonic

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
# lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an OTAA authentication parameters
app_eui = ubinascii.unhexlify('70B3D54993092D31')
app_key = ubinascii.unhexlify('80F8F7183265476FE3423BF374C31EAC')

# join a network using OTAA (Over the Air Activation)
# lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
# while not lora.has_joined():
#     time.sleep(2.5)
#     print('Not yet joined...')

# create a LoRa socket
# s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
# s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

try:
    while True:
        start = time.time()
        message = []
        for i in range(30):
            start_time = time.time()
            level = Ultrasonic.measureDistance()
            message.append(level)
            time.sleep(1 - (time.time() - start_time))
            print(level)
        s = ubinascii.hexlify(bytearray(message))
        print(s)
        print(len(s))
        # make the socket blocking
        # (waits for the data to be sent and for the 2 receive windows to expire)
#        s.setblocking(True)

        # send some data
#        s.send(level)

        # make the socket non-blocking
        # (because if there's no data received it will block forever...)
#        s.setblocking(False)
        # get any data received (if any...)
#        data = s.recv(64)
#        print(data)
        time.sleep(300 - (time.time() - start))
except KeyboardInterrupt:
#    s.close()
    exit(0)


