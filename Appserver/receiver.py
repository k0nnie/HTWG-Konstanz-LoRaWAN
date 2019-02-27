import time
import ttn
import evaluateData

app_id = "htwg-konstanz-testapp"
access_key = "ttn-account-v2.d7Q2pGiB97SPJFjr_WphmoaZKctmJRE93MhC6T9rP-g"

def uplink_callback(msg, client):
  print("Received uplink from ", msg.dev_id)
  with open ("nodedata", "a+") as f:
    f.write(str(msg) + "\n")
  evaluateData.main()
handler = ttn.HandlerClient(app_id, access_key)

# using mqtt client
mqtt_client = handler.data()
mqtt_client.set_uplink_callback(uplink_callback)
mqtt_client.connect()

while True:
    pass
