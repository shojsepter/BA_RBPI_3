from smbus2 import SMBus, i2c_msg
import time

# SETUP
msg_start = i2c_msg.write(0x61, [0x00, 0x10, 0x00, 0x00, 0x81])
msg_read = i2c_msg.write(0x61, [0x03, 0x00])
msg = i2c_msg.read(0x61, 18)
msg_stop = i2c_msg.write(0x28, [0x3F, 0xF9])

bus = SMBus(1)
bus.i2c_rdwr(msg_start)
time.sleep(0.1)
bus.i2c_rdwr(msg_read)
time.sleep(0.01)
bus.i2c_rdwr(msg)
data = list(msg)
print(data)