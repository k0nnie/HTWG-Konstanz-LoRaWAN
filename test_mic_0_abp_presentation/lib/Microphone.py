from machine import ADC
import time
adc = ADC(0)
adc.vref(1127)
pin = adc.channel(pin='P16', attn=ADC.ATTN_11DB)
SAMPLE_WIDTH = 0.05

def senseLevel() -> int:
    signal_min = 4096
    signal_max = 0
    start_time = time.time()

    while time.time() - start_time < SAMPLE_WIDTH:
        sample = pin()
        if sample < 4096:
            if sample > signal_max:
                signal_max = sample
            if sample < signal_min:
                signal_min = sample
    return pin.value_to_voltage(signal_max - signal_min)


if __name__ == "__main__":
    pass
