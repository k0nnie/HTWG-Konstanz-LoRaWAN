import pycom
from time import sleep_ms
from machine import Pin, Timer
trigger = Pin('P22', mode=Pin.OUT, pull=Pin.PULL_DOWN)
echo = Pin('P21', mode=Pin.IN, pull=Pin.PULL_DOWN)


def measureDistance():
    micros = Timer.Chrono()
    start = 0
    end = 0
    micros.reset()
    print("trigger up")
    trigger.value(1)
    Timer.sleep_us(10)
    trigger.value(0)
    print("trigger down")
    while echo.value() == 0:
        start = micros.read_ms()
    # Wait 'till the pulse is gone.
    while echo.value() == 1:
        end = micros.read_ms()
    micros.stop()
    delay = end - start
    print("received echo.")
    print(delay)
    delay = int(delay / 58.2)
    print(delay)
    if delay > 255:
        delay = 255
    return delay

if __name__ == "__main__":
    pass
