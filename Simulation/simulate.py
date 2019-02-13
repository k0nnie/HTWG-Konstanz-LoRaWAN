import requests

req_header = {
"authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI1YmU5N2Q1MDVkMzU2ODAwM2IwMjNkM2QiLCJpc3MiOiJ0dG4tYWNjb3VudC12MiIsImlhdCI6MTU1MDA3MjU4MSwidHlwZSI6InVzZXIiLCJjbGllbnQiOiJ0dG4tY29uc29sZSIsInNjb3BlIjpbImFwcHMiLCJnYXRld2F5cyIsInByb2ZpbGUiLCJjbGllbnRzIl0sImludGVyY2hhbmdlYWJsZSI6dHJ1ZSwidXNlcm5hbWUiOiJIVFdHLUtvbnN0YW56LUxvUmFXQU4iLCJlbWFpbCI6Im1heHJvdGhAaHR3Zy1rb25zdGFuei5kZSIsImNyZWF0ZWQiOiIyMDE4LTExLTEyVDEzOjE3OjA0Ljk0MFoiLCJ2YWxpZCI6dHJ1ZSwiX2lkIjoiNWJlOTdkNTA1ZDM1NjgwMDNiMDIzZDNkIiwiZXhwIjoxNTUwMDc2MjQxfQ.TLD350322mKWaBfnmEN1hRJvvcZSJxiPdG9jU9yrY6spdELw2P7U5vZOLn_QK50jiKV4X_zx3bDg6NQujGq0tItfIM4EhS3tBP8obgLLkPZl0Z8b-pHOEvxQvYhL-nYD5V-6Nh89lV3JmklF7h7RNoBXeZvUIxjEFaUBmoVdFPS1EfMHgMfDBob1EJKZrSxZA4gVmPf2HkQ232LcQZnDEiQEueAXrGie6JKpYUUnCgpTgniAaMhx0lpoQZraC5d62wF0blsTpzSo6Qv7q8dnAJIXuquZL1J8jvxm2oUnfQ1zEq6YbU7Xizm6hw2631QcgkEbJcXMI3ZLPbIsyNDaZIsvBxxLtlWsykBE9Vm6mhHF5OZSgyaSIQB7A9rd9fZqv3jFOz-vGeXL3tUaw26eH_HtiogTnVP1lToqUnsNYnGTxVOEBHxBkYfUO3Gx8Oed2aioY3CH_fcAWsx80dDqGz2ZnGxbsyjndcVdFnnOvK7sFDEUofuGsmhSJ9bqZ9kTW4kzOq_8fRW_8wXHx-bLRlnnwlKqVbyn5qSNtFPmKsZbpntH7HC3VunLtH7f_FhSZjWaJzK5RdaddssATgEJ1IZFR0TBZXh3cKzIP2J_uAy4GcOPSkTVrV1lsWSymaVcmDdy0nTvRzjuAN5TFtTTFdqyR_BT0k7xxoTz_XFTH7k"
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

req_body = {"fport":1,"payload":"FFFF"}

req_body["payload"] = "FFFF"

payload_int_left = 255
payload_int_right = 255
for x in range(10):
    payload_int_left = payload_int_left - 20
    payload_int_right = payload_int_right - 20
    req_body["payload"] = str(hex(payload_int_left)[2:]) + str(hex(payload_int_right)[2:])
    print(req_body["payload"])
    for y in range(5):
        response = s.post(distance_addresses[y], json= req_body, headers=req_header)
        print(str(response))
        
response = s.post(mic_addresses[0], json= req_body, headers=req_header)
response = s.post(mic_addresses[1], json= req_body, headers=req_header)
print(str(response))
