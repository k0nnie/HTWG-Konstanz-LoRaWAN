import requests
import time

req_header = {
"authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1YmU5N2Q1MDVkMzU2ODAwM2IwMjNkM2QiLCJpc3MiOiJ0dG4tYWNjb3VudC12MiIsImlhdCI6MTU1MDE0NTk0NCwidHlwZSI6InVzZXIiLCJjbGllbnQiOiJ0dG4tY29uc29sZSIsInNjb3BlIjpbImFwcHMiLCJnYXRld2F5cyIsInByb2ZpbGUiLCJjbGllbnRzIl0sImludGVyY2hhbmdlYWJsZSI6dHJ1ZSwidXNlcm5hbWUiOiJIVFdHLUtvbnN0YW56LUxvUmFXQU4iLCJlbWFpbCI6Im1heHJvdGhAaHR3Zy1rb25zdGFuei5kZSIsImNyZWF0ZWQiOiIyMDE4LTExLTEyVDEzOjE3OjA0Ljk0MFoiLCJ2YWxpZCI6dHJ1ZSwiX2lkIjoiNWJlOTdkNTA1ZDM1NjgwMDNiMDIzZDNkIiwiZXhwIjoxNTUwMTQ5NjA0fQ.i4lNY2-JHpbRQG1QbBzz4t2r8kMRr3e3uz7BU0VTqrkqDnyCTssCCibxllKf6loRcq3iS5oPXe0PvRzvfvZ5Wl58PpqEB518AA5VMMeqlMrDMl5tLP8jg8kJGlyEk_upkGQHRSP8MXjWm-erNoQEC0Wnz0l1y1JF_VEfdLGrYwZZc7RDCgqXnPcGu8OrnJ5ls6cmF16kUhiEvpZu9Wl7dNwpG6wtUP0lizNcGQ-abVdK0SNLcgZfeGR0AvFqXhDc1OrXzbVKElvcqPrBAaVse2fNsSKjRieOJUZczP3PWQ-Uui9cNXlxb9FKWgse_0ZpTCoAR_fIBKbLsWO3HV65Lm4iSCDbBkPwH4kzw2yzAVG3dzdBN0Jg6gtJ5v75OTPbYHalqcIlp_y0yIH2qxPunhJ1RdA167roGVtWYAj1IHNQ-xEzx0_R8TzdY735QCS99GSDvXUr2M7-z89GWYanxT6nWluNj-bqcD-3FNblUyjEEpKPNBtGQEOF9aSlsqMrBOXaWrHsmYzFZ7YOr5lQp4bxnsF7Ld0SEB88W9yvCuFZ7WmQVSA7z9wuui7kZ1XnCDw0w1xwtBqCTQ8m6xCO5ejfOkNUx_9oh1VJ8fx-7j_XkAQxgu3wO8cIJNNoTJXq37SEzv2-IciRIxRYrzYP5hUR8lNMBbxm3TgaJFqKLvI"
}

login = {"username":"HTWG-Konstanz-LoRaWAN","password":"X4>8g6m?"}

distance_addresses = ["https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp/devices/test_distance_0/uplink", 
             "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp/devices/test_distance_1/uplink",
             "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp/devices/test_distance_3/uplink",
             "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp/devices/test_distance_4/uplink",
             "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp/devices/test_distance_5/uplink"]

mic_addresses = ["https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp/devices/test_mic_0/uplink",
                 "https://console.thethingsnetwork.org/api/applications/htwg-konstanz-testapp/devices/test_mic_1/uplink"]

s = requests.Session()
response_login = s.post("https://account.thethingsnetwork.org/api/v2/users/login", data=login )

print(str(response_login.headers))

body_distance = {"fport":1,"payload":"FFFF"}
body_mic = {"fport":1,"payload":"00"}

#reset all sensors to simulate empty queue and room
for distance in range(len(distance_addresses)):
        response = s.post(distance_addresses[distance], json= body_distance, headers=req_header)
        print(str(response))
for mic in range(len(mic_addresses)):
        response = s.post(mic_addresses[mic], json= body_mic, headers=req_header)


payload_int_left = 255
payload_int_right = 255
payload_mic = 0
for x in range(len(distance_addresses)):
    payload_int_left = 255
    payload_int_right = 255
    payload_mic = payload_mic + 50
    body_mic["payload"] = str(hex(payload_mic)[2:])
    for mic in range(len(mic_addresses)):
        response = s.post(mic_addresses[mic], json= body_mic, headers=req_header)
    for y in range(10):
        payload_int_left = payload_int_left - 20
        payload_int_right = payload_int_right - 20
        body_distance["payload"] = str(hex(payload_int_left)[2:]) + str(hex(payload_int_right)[2:])
        print(body_distance["payload"])
        time.sleep(.3)
        response = s.post(distance_addresses[x], json= body_distance, headers=req_header)
        print(str(response))
body_distance["payload"] = "FF00"
response = s.post(distance_addresses[4], json= body_distance, headers=req_header)
time.sleep(3)
body_distance["payload"] = "00FF"
response = s.post(distance_addresses[3], json= body_distance, headers=req_header)
    
print(str(response))
