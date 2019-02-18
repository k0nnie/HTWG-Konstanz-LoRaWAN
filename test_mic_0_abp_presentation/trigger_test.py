from machine import Pin
from time import sleep

trigger = Pin('P16', mode=Pin.OUT)

def test():
    while True:
        trigger.value(0)
        sleep(2)
        trigger.value(1)
        sleep(2)


if __name__ == "__main__":
    test()