import requests
import time
import random

req_header = {

    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1YmU5N2Q1MDVkMzU2ODAwM2IwMjNkM2QiLCJpc3MiOiJ0dG4tYWNjb3VudC12MiIsImlhdCI6MTU1MDU2ODk3NSwidHlwZSI6InVzZXIiLCJjbGllbnQiOiJ0dG4tY29uc29sZSIsInNjb3BlIjpbImFwcHMiLCJnYXRld2F5cyIsInByb2ZpbGUiLCJjbGllbnRzIl0sImludGVyY2hhbmdlYWJsZSI6dHJ1ZSwidXNlcm5hbWUiOiJIVFdHLUtvbnN0YW56LUxvUmFXQU4iLCJlbWFpbCI6Im1heHJvdGhAaHR3Zy1rb25zdGFuei5kZSIsImNyZWF0ZWQiOiIyMDE4LTExLTEyVDEzOjE3OjA0Ljk0MFoiLCJ2YWxpZCI6dHJ1ZSwiX2lkIjoiNWJlOTdkNTA1ZDM1NjgwMDNiMDIzZDNkIiwiZXhwIjoxNTUwNTcyNjM1fQ.ugGC3K44r51EP3MSskBeMhQEUABvrY1aoZpOr2O2AehdsnlX83HYicRokp__wxJT36PvMMH2CiawZQiKOjMfeRF-S-UOGcDbIyEyVI5MdM4tJYyPx1ML1J5GC4yISSXvqYm4X28NI0yfNKNGrUsl0niJ7DwrfvuRkAw-ChMhi-i9wyKhaOwxujDcpcDk0jZiewhURcaje31X72NK0JwWdYpQAA800Xpd9lxtEsMUZ8G6C0aB3PBrfUyyE6DM-ZX0sRAjuSCHG8aTWQkVVG8KzIlPy63TRIsS8ur2PxfgcH9TOS-gg6rEvS4grgiPTI5yVZoLv_Xg3dF_dRuC0mJdofGD2Sd50iQoZ8-rmVqB_pSR6fCcNSfqCioWRtomnjjQer2ff4WXzXpMAg1RVlh-kstgnAXh2Pvid7fdq0llJXEwGOw7hwhX9aaefcfUG8PXHu5FjWocaN2XgeUT0iYD6l2A4UPGyjPomzb_y8ilgCqrYsRvpIYBp0wala90jPp0Gb1NBlsOWzYc6oFpVMk_El5puVlJnrH6iiIwjsIttklN3EZROUE2Az80k6-AetEYFercEUAuKehdDDiILO2Dr-ucZk1ehChkxzUGm9g2sMZ0kDoPjF0ydEKfrKgKQuossp87sX2BYn0nxZOt1Vjn-4Yc_ecrMgjmtn-a97kDnaQ"}

login = {"username": "HTWG-Konstanz-LoRaWAN", "password": "X4>8g6m?"}
distance_addresses = [
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp/devices/test_distance_0/uplink",
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp/devices/test_distance_1/uplink",
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp/devices/test_distance_3/uplink",
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp/devices/test_distance_3/uplink",
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp/devices/test_distance_4/uplink",
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp/devices/test_distance_5/uplink"]

mic_addresses = [
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp/devices/test_mic_0/uplink",
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp/devices/test_mic_1/uplink"]

s = requests.Session()
response_login = s.post("https://account.thethingsnetwork.org/api/v2/users/login", data=login)

print(str(response_login.headers))

body_distance = {"fport": 1, "payload": "FFFF"}
body_mic = {"fport": 1, "payload": "00"}
MINUTE = 1  # the rate at which data is sent from each device (x times per minute)

MIC_LEVEL_0 = 0  # min value for mic
MIC_LEVEL_1 = 20  # no noise measured
MIC_LEVEL_2 = 60  # pretty quiet
MIC_LEVEL_3 = 100  # noticeable noise
MIC_LEVEL_4 = 140  # quite noisy
MIC_LEVEL_5 = 180  # probably a lot of people talking loudly
DISTANCE_MAX = 0
DISTANCE_MIN = 255
DISTANCE_TRIGGER = 150


# reset all sensors to simulate empty queue and room
def reset():
    for distance in range(len(distance_addresses)):
        response = s.post(distance_addresses[distance], json=body_distance, headers=req_header)
        print(str(response))
    for mic in range(len(mic_addresses)):
        response = s.post(mic_addresses[mic], json=body_mic, headers=req_header)


def prototype():
    payload_int_left = 255
    payload_int_right = 255
    payload_mic = 0
    for x in range(len(distance_addresses)):
        payload_int_left = 255
        payload_int_right = 255
        payload_mic = payload_mic + 50
        body_mic["payload"] = str(hex(payload_mic)[2:])
        for mic in range(len(mic_addresses)):
            response = s.post(mic_addresses[mic], json=body_mic, headers=req_header)
        for y in range(10):
            payload_int_left = payload_int_left - 20
            payload_int_right = payload_int_right - 20
            body_distance["payload"] = str(hex(payload_int_left)[2:]) + str(hex(payload_int_right)[2:])
            print(body_distance["payload"])
            time.sleep(.3)
            response = s.post(distance_addresses[x], json=body_distance, headers=req_header)
            print(str(response))
    body_distance["payload"] = "FF00"
    response = s.post(distance_addresses[4], json=body_distance, headers=req_header)
    time.sleep(3)
    body_distance["payload"] = "00FF"
    response = s.post(distance_addresses[3], json=body_distance, headers=req_header)

    print(str(response))


# not actually random but a pattern that doesn't lead to queues while triggering sensors below the threshold
def random_pattern():
    payload_int_left = 0
    payload_int_right = 0
    payload_mic = 0

    # initialize and send random distance values on all devices
    for x in range(len(distance_addresses)):
        payload_int_left = random.randint(DISTANCE_TRIGGER, DISTANCE_MIN)  # values below trigger
        payload_int_right = random.randint(DISTANCE_TRIGGER, DISTANCE_MIN)

        body_distance["payload"] = str(hex(payload_int_left)[2:]) + str(hex(payload_int_right)[2:])
        response = s.post(distance_addresses[x], json=body_distance, headers=req_header)
        time.sleep(.1)

    # initialize and send random mic values on all devices
    for mic in range(len(mic_addresses)):
        payload_mic = random.randint(MIC_LEVEL_0, MIC_LEVEL_2)  # assuming this level means hardly any noise

        body_mic["payload"] = str(hex(payload_mic)[2:])
        response = s.post(mic_addresses[mic], json=body_mic, headers=req_header)


# dist_dev = number from 0 - len(distance_addresses)
def random_above_threshold(dist_dev):
    payload_int_left = random.randint(DISTANCE_MAX, DISTANCE_TRIGGER)  # values below trigger
    payload_int_right = random.randint(DISTANCE_MAX, DISTANCE_TRIGGER)
    body_distance["payload"] = str(hex(payload_int_left)[2:]) + str(hex(payload_int_right)[2:])
    response = s.post(distance_addresses[dist_dev], json=body_distance, headers=req_header)


def random_below_threshold(dist_dev):
    # to add one byte pair above threshold
    payload_int_left_above = random.randint(DISTANCE_MAX, DISTANCE_TRIGGER)
    payload_int_right_above = random.randint(DISTANCE_MAX, DISTANCE_TRIGGER)

    # random values that are below the triggerpoint for the sensor
    payload_int_left = random.randint(DISTANCE_TRIGGER, DISTANCE_MIN)
    payload_int_right = random.randint(DISTANCE_TRIGGER, DISTANCE_MIN)
    payload_int_left2 = random.randint(DISTANCE_TRIGGER, DISTANCE_MIN)
    payload_int_right2 = random.randint(DISTANCE_TRIGGER, DISTANCE_MIN)
    payload_int_left3 = random.randint(DISTANCE_TRIGGER, DISTANCE_MIN)
    payload_int_right3 = random.randint(DISTANCE_TRIGGER, DISTANCE_MIN)

    # to ensure the one above threshold measurement can't change the mean of values above threshold
    payload_int_left4 = random.randint(230, DISTANCE_MIN)
    payload_int_right4 = random.randint(230, DISTANCE_MIN)

    body_distance["payload"] = \
        str(hex(payload_int_left_above)[2:]) \
        + str(hex(payload_int_right_above)[2:]) \
        + str(hex(payload_int_left)[2:]) \
        + str(hex(payload_int_right)[2:]) \
        + str(hex(payload_int_left2)[2:]) \
        + str(hex(payload_int_right2)[2:]) \
        + str(hex(payload_int_left3)[2:]) \
        + str(hex(payload_int_right3)[2:]) \
        + str(hex(payload_int_left4)[2:]) \
        + str(hex(payload_int_right4)[2:])

    response = s.post(distance_addresses[dist_dev], json=body_distance, headers=req_header)


def send_specific_dist_value(dist_dev, value):
    payload_int_left = value
    payload_int_right = value
    payload_int_left2 = value
    payload_int_right2 = value
    payload_int_left3 = value
    payload_int_right3 = value
    payload_int_left4 = value
    payload_int_right4 = value
    payload_int_left5 = value
    payload_int_right5 = value

    body_distance["payload"] = \
        str(hex(payload_int_left)[2:]) \
        + str(hex(payload_int_left2)[2:]) \
        + str(hex(payload_int_left3)[2:]) \
        + str(hex(payload_int_left4)[2:]) \
        + str(hex(payload_int_left5)[2:]) \
        + str(hex(payload_int_right)[2:]) \
        + str(hex(payload_int_right2)[2:]) \
        + str(hex(payload_int_right3)[2:]) \
        + str(hex(payload_int_right4)[2:]) \
        + str(hex(payload_int_right5)[2:])

    response = s.post(distance_addresses[dist_dev], json=body_distance, headers=req_header)
    print(str(response))


# sends a direct level of mic noise (0-5) rather than specific values because the specific values for the mic are rather uninteresting.
def send_mic_level(n):  # n = mic level
    payload_mic = n * 41
    for mic in range(len(mic_addresses)):
        body_mic["payload"] = str(hex(payload_mic)[2:])
        response = s.post(mic_addresses[mic], json=body_mic, headers=req_header)


def mic_level_plus1_random(n):
    x = random.randint(n - 20, n + 60)
    send_mic_level(x)


# first n devices are above threshold
def n_dists_above_threshold(n):
    for x in range(len(distance_addresses)):
        if x <= n:  # for all devices 1-n
            random_above_threshold(x)
        else:  # for the remaining devices
            random_above_threshold(x)


# one time sending each sensor represents 30seconds
# in the perfect scenario from 11:00 to 11:30 only seemingly random spikes on mic and distance sensors (a few people enter , some are just down in the cafeteria buying coffee while a few others go for an early lunch)
# 11:30 we see a gradual increase in noise and distance sensors. random pattern persists but the front sensors get triggered more and more which leads to queues being set for the first sensors.
# 11:35 - 12:00 increase to queue of 2
# 12:00-12:30 queue to 1
# 12:00-13:00 random below trigger and no queue
# 13:00-13:30 heavy queue building

def perfect_scenario():
    print("start perfect scenario")
    # reset
    send_specific_dist_value(0, 255)
    send_specific_dist_value(0, 255)
    send_specific_dist_value(0, 255)
    send_specific_dist_value(0, 255)
    send_specific_dist_value(1, 255)
    send_specific_dist_value(1, 255)
    send_specific_dist_value(1, 255)
    send_specific_dist_value(1, 255)
    send_specific_dist_value(1, 255)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(3, 255)
    send_specific_dist_value(3, 255)
    send_specific_dist_value(3, 255)
    send_specific_dist_value(3, 255)
    send_specific_dist_value(3, 255)
    send_specific_dist_value(4, 255)
    send_specific_dist_value(4, 255)
    send_specific_dist_value(4, 255)
    send_specific_dist_value(4, 255)
    send_specific_dist_value(4, 255)
    send_mic_level(0)
    send_mic_level(0)
    send_mic_level(0)
    send_mic_level(0)
    send_mic_level(0)
    time.sleep(.1)

    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(1)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)

    send_specific_dist_value(0, 0)
    send_specific_dist_value(0, 0)
    send_specific_dist_value(0, 0)
    send_specific_dist_value(0, 0)
    send_specific_dist_value(0, 0)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_specific_dist_value(1, 0)
    send_specific_dist_value(1, 0)
    send_specific_dist_value(1, 0)
    send_specific_dist_value(1, 0)
    send_specific_dist_value(1, 0)
    send_mic_level(4)
    send_mic_level(4)
    send_mic_level(4)
    send_mic_level(4)
    send_mic_level(4)
    send_specific_dist_value(2, 0)
    send_specific_dist_value(2, 0)
    send_specific_dist_value(2, 0)
    send_specific_dist_value(2, 0)
    send_specific_dist_value(2, 0)
    send_specific_dist_value(1, 0)
    send_specific_dist_value(1, 0)
    send_specific_dist_value(1, 0)
    send_specific_dist_value(1, 0)
    send_specific_dist_value(1, 0)
    send_specific_dist_value(3, 0)
    send_specific_dist_value(3, 0)
    send_specific_dist_value(3, 0)
    send_specific_dist_value(3, 0)
    send_specific_dist_value(3, 0)
    send_specific_dist_value(2, 0)
    send_specific_dist_value(2, 0)
    send_specific_dist_value(2, 0)
    send_specific_dist_value(2, 0)
    send_specific_dist_value(2, 0)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(2, 0)
    send_specific_dist_value(2, 0)
    send_specific_dist_value(2, 0)
    send_specific_dist_value(2, 0)
    send_specific_dist_value(2, 0)



    send_specific_dist_value(4, 0)
    send_specific_dist_value(4, 0)
    send_specific_dist_value(4, 0)
    send_specific_dist_value(4, 0)
    send_specific_dist_value(4, 0)
    send_specific_dist_value(4, 0)
    send_specific_dist_value(4, 0)
    send_specific_dist_value(4, 0)
    send_specific_dist_value(4, 0)
    send_specific_dist_value(4, 0)
    send_mic_level(5)
    send_mic_level(5)
    send_mic_level(5)
    send_mic_level(5)
    send_specific_dist_value(4, 0)
    send_specific_dist_value(4, 0)
    send_specific_dist_value(4, 0)
    send_specific_dist_value(4, 0)
    send_specific_dist_value(4, 0)
    send_specific_dist_value(4, 255)
    send_specific_dist_value(4, 255)
    send_specific_dist_value(4, 255)
    send_specific_dist_value(4, 255)
    send_specific_dist_value(4, 255)
    send_specific_dist_value(4, 255)
    send_specific_dist_value(4, 255)
    send_specific_dist_value(4, 255)
    send_specific_dist_value(4, 255)
    send_specific_dist_value(3, 255)
    send_specific_dist_value(3, 255)
    send_specific_dist_value(3, 255)
    send_specific_dist_value(3, 255)
    send_specific_dist_value(3, 255)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(1, 255)
    send_specific_dist_value(1, 255)
    send_specific_dist_value(1, 255)
    send_specific_dist_value(1, 255)
    send_specific_dist_value(1, 255)
    send_specific_dist_value(1, 255)
    send_specific_dist_value(0, 255)
    send_specific_dist_value(0, 255)
    send_specific_dist_value(0, 255)
    send_specific_dist_value(0, 255)
    send_specific_dist_value(0, 255)
    send_mic_level(4)
    send_mic_level(4)
    send_mic_level(4)
    send_mic_level(4)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(3)
    send_mic_level(2)
    send_mic_level(2)
    send_mic_level(2)


def perfect_scenario_full_send():
    send_specific_dist_value(0, 255)
    send_specific_dist_value(1, 255)
    send_specific_dist_value(2, 255)
    send_specific_dist_value(3, 255)
    send_specific_dist_value(4, 255)

    for x in range (MINUTE * 30):  #30min
       send_specific_dist_value(0, 0)
       mic_level_plus1_random(1)
       time.sleep(.1)

       # 11:30
    print("11:30")
    for x in range (MINUTE * 90):
        random_pattern()
        send_mic_level(0)


    #13:00
    for x in range (MINUTE * 5):
        send_specific_dist_value(0, 0)
        send_specific_dist_value(1, 255)
        send_specific_dist_value(2, 255)
        send_specific_dist_value(3, 255)
        send_specific_dist_value(4, 255)
        mic_level_plus1_random(1)
        time.sleep(.1)
    #13:05
    for x in range(MINUTE * 5):
        send_specific_dist_value(0, 0)
        send_specific_dist_value(1, 0)
        send_specific_dist_value(2, 255)
        send_specific_dist_value(3, 255)
        send_specific_dist_value(4, 255)
        mic_level_plus1_random(3)
        time.sleep(.1)

    #13:10
    for x in range(MINUTE * 2):
        send_specific_dist_value(0, 0)
        send_specific_dist_value(1, 0)
        send_specific_dist_value(2, 0)
        send_specific_dist_value(3, 255)
        send_specific_dist_value(4, 255)
        mic_level_plus1_random(3)
        time.sleep(.1)

    #13:12
    for x in range(MINUTE * 3):
        send_specific_dist_value(0, 0)
        send_specific_dist_value(1, 0)
        send_specific_dist_value(2, 0)
        send_specific_dist_value(3, 0)
        send_specific_dist_value(4, 255)
        mic_level_plus1_random(4)
        time.sleep(.1)

    #13:15
    for x in range(MINUTE * 5):
        send_specific_dist_value(0, 0)
        send_specific_dist_value(1, 0)
        send_specific_dist_value(2, 0)
        send_specific_dist_value(3, 0)
        send_specific_dist_value(4, 0)
        mic_level_plus1_random(4)
        time.sleep(.1)

    #13:18
    for x in range(MINUTE * 2):
        send_specific_dist_value(0, 0)
        send_specific_dist_value(1, 0)
        send_specific_dist_value(2, 0)
        send_specific_dist_value(3, 0)
        send_specific_dist_value(4, 255)
        mic_level_plus1_random(4)
        time.sleep(.1)

    #13:23
    for x in range(MINUTE * 2):
        send_specific_dist_value(0, 0)
        send_specific_dist_value(1, 0)
        send_specific_dist_value(2, 0)
        send_specific_dist_value(3, 255)
        send_specific_dist_value(4, 255)
        mic_level_plus1_random(3)
        time.sleep(.1)

    #13:25
    for x in range(MINUTE * 5):
        send_specific_dist_value(0, 0)
        send_specific_dist_value(1, 0)
        send_specific_dist_value(2, 255)
        send_specific_dist_value(3, 255)
        send_specific_dist_value(4, 255)
        mic_level_plus1_random(3)
        time.sleep(.1)

    # 13:28
    for x in range(MINUTE * 12):
        send_specific_dist_value(0, 0)
        send_specific_dist_value(1, 255)
        send_specific_dist_value(2, 255)
        send_specific_dist_value(3, 255)
        send_specific_dist_value(4, 255)
        mic_level_plus1_random(2)
        time.sleep(.1)

    for x in range(MINUTE * 20):
        random_pattern()
        mic_level_plus1_random(2)
    print("done perfect scenario")

#perfect_scenario()
perfect_scenario_full_send()
