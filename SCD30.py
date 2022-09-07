from smbus2 import SMBus, i2c_msg
import time
import struct

# SETUP
msg_start = i2c_msg.write(0x61, [0x00, 0x10, 0x00, 0x00, 0x81])
msg_read = i2c_msg.write(0x61, [0x03, 0x00])
msg = i2c_msg.read(0x61, 18)
msg_stop = i2c_msg.write(0x28, [0x3F, 0xF9])

bus = SMBus(1)
bus.i2c_rdwr(msg_start)
time.sleep(0.1)

while True:
    bus.i2c_rdwr(msg_read)
    time.sleep(0.01)
    bus.i2c_rdwr(msg)
    data = list(msg)
    print(data)

    byte_1 = hex(data[0])[2:].zfill(2)
    byte_2 = hex(data[1])[2:].zfill(2)
    byte_3 = hex(data[2])[2:].zfill(2)
    byte_4 = hex(data[3])[2:].zfill(2)

    bytes_merged = byte_1+byte_2+byte_3+byte_4

    float_co2 = struct.unpack('!f', bytes.fromhex(bytes_merged))[0]

    byte_1 = hex(data[6])[2:].zfill(2)
    byte_2 = hex(data[7])[2:].zfill(2)
    byte_3 = hex(data[9])[2:].zfill(2)
    byte_4 = hex(data[10])[2:].zfill(2)


    bytes_merged = byte_1+byte_2+byte_3+byte_4

    float_t = struct.unpack('!f', bytes.fromhex(bytes_merged))[0]

    byte_1 = hex(data[12])[2:].zfill(2)
    byte_2 = hex(data[13])[2:].zfill(2)
    byte_3 = hex(data[15])[2:].zfill(2)
    byte_4 = hex(data[16])[2:].zfill(2)


    bytes_merged = byte_1+byte_2+byte_3+byte_4

    float_h = struct.unpack('!f', bytes.fromhex(bytes_merged))[0]

    print("float_co2:", float_co2, "float_t:", float_t, "float_h:", float_h)
    time.sleep(2)