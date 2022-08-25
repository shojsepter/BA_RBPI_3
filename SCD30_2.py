from smbus2 import SMBus, i2c_msg
import time
import struct
from typing import List

# SETUP
msg_start = i2c_msg.write(0x61, [0x00, 0x10, 0x00, 0x00, 0x81])
msg_read = i2c_msg.write(0x61, [0x03, 0x00])
msg = i2c_msg.read(0x61, 18)
msg_stop = i2c_msg.write(0x28, [0x3F, 0xF9])

bus = SMBus(1)
bus.i2c_rdwr(msg_start)
time.sleep(0.1)


# data = [68, 65, 135, 156, 190, 216, 65, 228, 249, 193, 12, 162, 66, 30, 141, 175, 112, 31]


def SCD30_cast_float(data: List[int]) -> float :
    """takes in 4 bits and casts a float like described in the datasheet"""
    byte_1 = hex(data[0])[2:].zfill(2)
    byte_2 = hex(data[1])[2:].zfill(2)
    byte_3 = hex(data[2])[2:].zfill(2)
    byte_4 = hex(data[3])[2:].zfill(2)
    bytes_merged = byte_1+byte_2+byte_3+byte_4
    float_value = struct.unpack('!f', bytes.fromhex(bytes_merged))[0]
    return float_value
 
while True:
    bus.i2c_rdwr(msg_read)
    time.sleep(0.1)
    bus.i2c_rdwr(msg)
    data = list(msg)
    print(data)
    CO2_bytes = list(data[i] for i in [0, 1, 3, 4])
    print(CO2_bytes)
    CO2_float = SCD30_cast_float(CO2_bytes)
    print(CO2_float)

    Temp_bytes = list(data[i] for i in [6, 7, 9, 10])
    print(CO2_bytes)
    Temp_float = SCD30_cast_float(Temp_bytes)
    print(Temp_float)

    Hum_bytes = list(data[i] for i in [12, 13, 15, 16])
    print(CO2_bytes)
    Hum_float = SCD30_cast_float(Hum_bytes)
    print(Hum_float)
    time.sleep(2)


