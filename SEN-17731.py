
import smbus2
import time

COMMAND_GET_VALUE = 0x05
COMMAND_CHANGE_ADDRESS = 0x03
address = 0x10
new_address = 0x11


bus = smbus2.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
# bus.write_byte_data(address, COMMAND_GET_VALUE)
#bus.write_byte_data(address, COMMAND_CHANGE_ADDRESS, new_address)


while True:
#    value1 = bus.read_byte_data(new_address, COMMAND_GET_VALUE)
    value2 = bus.read_byte_data(address, COMMAND_GET_VALUE)
#    print("sensor1", value1)
    print("sensor2", value2)
    time.sleep(0.5)



# //When the master requests data from the slave, this
# //    ISR is triggered.

# void onI2CRequest() {
#    if (command == COMMAND_GET_VALUE) {
#     ADC_VALUE=analogRead(ADC_PIN);
#     ADC_VALUE_L=ADC_VALUE;
#     ADC_VALUE_H=ADC_VALUE>>8; 
#     TinyWire.send(ADC_VALUE_L);  
#     TinyWire.send(ADC_VALUE_H);
#     command = COMMAND_HAS_BEEN_CHECKED;
#   }
# }