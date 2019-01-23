import machine
from time import sleep
trigger = machine.Pin('P16', mode=machine.Pin.OUT)
echo = machine.Pin('P15', mode=machine.Pin.IN)


def measureDistance():
    trigger.value(0)
    sleep(2 / 1e-5)
    trigger.value(1)
    sleep(1 / 1e-5)
    trigger.value(0)
    delay = machine.time_pulse_us(echo, 1, 200000)  # 200ms timeout
    return int(delay / 58.2)

