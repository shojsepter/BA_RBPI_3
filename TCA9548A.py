from smbus2 import SMBus, i2c_msg
import time
import sys

channel_array=[0b00000001, 0b00000010, 0b00000100, 0b00001000, 0b00010000, 0b00100000, 0b01000000, 0b10000000]

def I2C_setup(multiplexer, i2c_chanel_setup):
    bus = SMBus(1)
    bus.write_byte(multiplexer, channel_array[i2c_chanel_setup])
    time.sleep(0.01)