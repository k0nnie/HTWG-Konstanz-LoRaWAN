import time
import ttn

app_id = "htwg-konstanz-testapp"
access_key = "ttn-account-v2.d7Q2pGiB97SPJFjr_WphmoaZKctmJRE93MhC6T9rP-g"

def uplink_callback(msg, client):
  print("Received uplink from ", msg.dev_id)
  print(msg)
  with open ("nodedata", "a") as f:
    f.write(str(msg[1]) + ", " + str(msg[5]) +", " + str(msg[6][0]) + "\n")

handler = ttn.HandlerClient(app_id, access_key)

# using mqtt client
mqtt_client = handler.data()
mqtt_client.set_uplink_callback(uplink_callback)
mqtt_client.connect()

input = input()
if input:
  mqtt_client.close()

# using application manager client
app_client =  handler.application()
my_app = app_client.get()
print(my_app)
my_devices = app_client.devices()
print(my_devices)
