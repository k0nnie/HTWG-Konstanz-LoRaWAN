import time
import ttn
import evaluateData

app_id = "htwg-konstanz-testapp-2"
access_key = "ttn-account-v2.ovmX0Bec96ipOedV41TcPP7xDlj-iuiV95DeVdS3HYU"

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
