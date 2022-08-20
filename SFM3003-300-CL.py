from smbus2 import SMBus, i2c_msg
import time

OFFSET_FLOW = -24576 # [-]
SCALEFACTOR_FLOW = 170 # [slm^-1]

OFFSET_TEMP = 0 # [-]
SCALEFACTOR_TEMP = 200 # [°C^-1]

# Single transaction writing two bytes then read two at address 80
# write = i2c_msg.write(0x28, [40, 50])
msg = i2c_msg.read(0x28, 9)

bus = SMBus(1)


while True:
    bus.i2c_rdwr(msg)
    data = list(msg)
    flow_bytes = data[0:2]
    flow_bytes_converted = bytes(flow_bytes)
    flow_raw = int.from_bytes(flow_bytes_converted, byteorder='big', signed=True)
    print("flow_raw: ", flow_raw)
    flow = (flow_raw-OFFSET_FLOW)/SCALEFACTOR_FLOW
    print("flow: ", flow)
    temp_bytes = data[3:5]
    temp_bytes_converted = bytes(temp_bytes)
    temp_raw = int.from_bytes(temp_bytes_converted, byteorder='big', signed=True)
    print("temp_raw: ", temp_raw)
    temp = (temp_raw-OFFSET_TEMP)/SCALEFACTOR_TEMP
    print("temp: ", temp)
    time.sleep(0.1)



# # 1: Convert message content to list
# msg = i2c_msg.write(60, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# data = list(msg)  # data = [1, 2, 3, ...]
# print(len(data))  # => 10

# # 2: i2c_msg is iterable
# for value in msg:
#     print(value)

# # 3: Through i2c_msg properties
# for k in range(msg.len):
#     print(msg.buf[k])

# while True:
#     value = bus.read_byte_data(new_address, COMMAND_GET_VALUE)
#     print(value)
#     time.sleep(0.5)

# bus = SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
# bus.write_byte_data(address, COMMAND_GET_VALUE)
# bus.write_byte_data(address, COMMAND_CHANGE_ADDRESS, new_address)


# while True:
#     value = bus.read_byte_data(new_address, COMMAND_GET_VALUE)
#     print(value)
#     time.sleep(0.5)


#   # Gets the specified variable as an unsigned value.
#   def get_variable(self, id):
#     write = i2c_msg.write(self.address, [0xA1, id])
#     read = i2c_msg.read(self.address, 2)
#     self.bus.i2c_rdwr(write, read)
#     b = list(read)
#     return b[0] + 256 * b[1]
