import requests
import time
import random
 
req_header = {
 
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1YzZhOTMzOWJiNDFkODAwM2I0MGVkNDUiLCJpc3MiOiJ0dG4tYWNjb3VudC12MiIsImlhdCI6MTU1MDUyMTgwMywidHlwZSI6InVzZXIiLCJjbGllbnQiOiJ0dG4tY29uc29sZSIsInNjb3BlIjpbImFwcHMiLCJnYXRld2F5cyIsInByb2ZpbGUiLCJjbGllbnRzIl0sImludGVyY2hhbmdlYWJsZSI6dHJ1ZSwidXNlcm5hbWUiOiJIVFdHLUtvbnN0YW56LUxvUmFXQU4tMiIsImVtYWlsIjoibmljb2xhaS5zdGVwaGFuQGh0d2cta29uc3RhbnouZGUiLCJjcmVhdGVkIjoiMjAxOS0wMi0xOFQxMToxMjo1Ny4zNzlaIiwidmFsaWQiOnRydWUsIl9pZCI6IjVjNmE5MzM5YmI0MWQ4MDAzYjQwZWQ0NSIsImV4cCI6MTU1MDUyNTQ2M30.YS_ZujH0Njrw5rvEAe7a7BTMbPc69ueo_F-K8RAFe1sGvRKDboAuGHmDzqZnKv3cQ2mx2kREXexiAYzRVud1Y_SMsmJo1CRFaM4qUsqS3GqvfYfS3K4Cc4Z5BsdmDj5LB1LyqAaIXdyVCW3lWlBIw0qkqoHVCCwY4WtVf8FrWF0W5iz75zQC162z5RrUJUQrUYHGGxEM1_XcRmihC_lur_G0r4_peBd6XcdW-jTQaDxXWUrH_os8fAJYL6MqBNL7LAfuyZrYRXt5M1V6Rg2gSHYV9desxmMVzlb_FW8wQkK6I4108ps0oQNO34oddgaN_MlmVyMO--4ZShB7r_it7IepVa4YwhNtMIYUI-gAxO00vUgGKyXZ_Q45j1380y6EexcMKq6EfQigSHT6lPPmyOhtv3aw0F28Jf1_B_3eS3XQzs8Ns_Q9MClSBXzV1FJbZVJVSW21Zf3vaF8w6c7-c15sA8w6I6UPBDynMw0jrGUffycaByUCk-Z8wKMMlYlQaCjG3_NiMVqsnhNOr6DI6wD8Dn2tD9yfo2fbEFYR3u0aNFpLUyaKDxcMrcQC0zggZnR0KhOcQ1LuKLf4F5x7U9_zUQjBb1T6qUlig694Rjmb7f87ZaxyE-bTaxK1hx1f2bZpr-UJSxdSEaElYZORYjlo731MZzVbcSfDJfKWNbs"
}
 
login = {"username": "HTWG-Konstanz-LoRaWAN-2", "password": "X4>8g6m?"}
distance_addresses = [
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp-2/devices/test_distance_0/uplink",
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp-2/devices/test_distance_1/uplink",
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp-2/devices/test_distance_3/uplink",
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp-2/devices/test_distance_3/uplink",
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp-2/devices/test_distance_4/uplink",
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp-2/devices/test_distance_5/uplink"]
 
mic_addresses = [
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp-2/devices/test_mic_0/uplink",
    "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp-2/devices/test_mic_1/uplink"]
 
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
    payload_mic = n
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
 
    #    for x in range (MINUTE * 1):  #60min
    #        #random_pattern()
    #        time.sleep(.1)
 
    #    # 12:00
    #    print("12:00")
    #    for x in range (MINUTE * 1): #60min
    #        #send_specific_dist_value(0, 0)
    #        #time.sleep(.1)
    #        #mic_level_plus1_random(1)
    #
    #    # 13:00
    #    print("13:00")
    #    for x in range (MINUTE * 1):
    ##        send_specific_dist_value(1, 0)
    ##        mic_level_plus1_random(MIC_LEVEL_2)
    ##        time.sleep(.1)
    #
    #    # 13:05
    #    print("13:05")
    #    for x in range (MINUTE * 1):
    #        send_specific_dist_value(2, 0)
    #        send_mic_level(4)
    #    time.sleep(.1)
    #
    #    #13:10
    #    for x in range(MINUTE * 1):
    #        send_specific_dist_value(3, 0)
    #        send_specific_dist_value(4, 0)
    #        send_specific_dist_value(5, 0)
    #        send_mic_level(5)
    #    time.sleep(.1)
    #
    #    #13:30
    #    for x in range(MINUTE * 1):
    #        send_specific_dist_value(4, 255)
    #        mic_level_plus1_random(4)
    #    time.sleep(.1)
    #
    #    # 13:40
    #    for x in range(MINUTE * 1):
    #        send_specific_dist_value(3, 255)
    #        mic_level_plus1_random(3)
    #    time.sleep(.1)
    #
    #    #13:45
    #    for x in range(MINUTE * 1):
    #        send_specific_dist_value(2, 255)
    #        mic_level_plus1_random(3)
    #    time.sleep(.1)
    #
    #    #13:45
    #    for x in range(MINUTE * 1):
    #        send_specific_dist_value(1, 255)
    #        mic_level_plus1_random(2)
    #    time.sleep(.1)
    #
    #    # 13:50
    #    for x in range(MINUTE * 1):
    #        send_specific_dist_value(0, 255)
    #        send_mic_level(2)
    #    time.sleep(.1)
    print("done perfect scenario")
 
 
# reset()
# prototype()
perfect_scenario()
 
# print("part2    ")
# for x in range(MINUTE * 2):
#     print("x")
#     send_specific_dist_value(0, 0)
#     send_specific_dist_value(1, 0)
#     send_specific_dist_value(2, 255)
#     send_specific_dist_value(3, 255)
#     send_specific_dist_value(4, 255)
#     time.sleep(.1)
#
# for x in range(MINUTE * 4):
#     print("x")
#     send_specific_dist_value(0, 0)
#     send_specific_dist_value(1, 0)
#     send_specific_dist_value(2, 0)
#     send_specific_dist_value(3, 255)
#     send_specific_dist_value(4, 255)
#     time.sleep(.1)
#
# for x in range(MINUTE * 2):
#     print("123")
#     send_specific_dist_value(0, 0)
#     send_specific_dist_value(1, 0)
#     send_specific_dist_value(2, 0)
#     send_specific_dist_value(3, 0)
#     send_specific_dist_value(4, 255)
#     time.sleep(.1)
