from smbus2 import SMBus, i2c_msg

msg1 = i2c_msg.read(0x61, 18)
read_measurement = i2c_msg.write(0x61, [0x03, 0x00])
bus = SMBus(1)
bus.i2c_rdwr(read_measurement, msg1)
data1 = list(msg1)
print(data1)