#!/usr/bin/python
import smbus2
import math
import time
 
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
 
bus = smbus2.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
 
# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)

while True:
    print ("Gyroskop")
    print ("--------")
    
    gyroskop_xout = read_word_2c(0x43)
    gyroskop_yout = read_word_2c(0x45)
    gyroskop_zout = read_word_2c(0x47)
    
    print ("gyroskop_xout: ", ("%5d" % gyroskop_xout), " skaliert: ", (gyroskop_xout / 131))
    print ("gyroskop_yout: ", ("%5d" % gyroskop_yout), " skaliert: ", (gyroskop_yout / 131))
    print ("gyroskop_zout: ", ("%5d" % gyroskop_zout), " skaliert: ", (gyroskop_zout / 131))
    
    print ("Beschleunigungssensor")
    print ("---------------------")
    
    beschleunigung_xout = read_word_2c(0x3b)
    beschleunigung_yout = read_word_2c(0x3d)
    beschleunigung_zout = read_word_2c(0x3f)
    
    beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
    beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0
    beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0
    
    print ("beschleunigung_xout: ", ("%6d" % beschleunigung_xout), " skaliert: ", beschleunigung_xout_skaliert)
    print ("beschleunigung_yout: ", ("%6d" % beschleunigung_yout), " skaliert: ", beschleunigung_yout_skaliert)
    print ("beschleunigung_zout: ", ("%6d" % beschleunigung_zout), " skaliert: ", beschleunigung_zout_skaliert)
    
    print ("X Rotation: " , get_x_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert))
    print ("Y Rotation: " , get_y_rotation(beschleunigung_xout_skaliert, beschleunigung_yout_skaliert, beschleunigung_zout_skaliert))
    time.sleep(0.5)

# #include "Wire.h" // This library allows you to communicate with I2C devices.

# const int MPU_ADDR = 0x68; // I2C address of the MPU-6050. If AD0 pin is set to HIGH, the I2C address will be 0x69.

# int16_t accelerometer_x, accelerometer_y, accelerometer_z; // variables for accelerometer raw data
# int16_t gyro_x, gyro_y, gyro_z; // variables for gyro raw data
# int16_t temperature; // variables for temperature data

# char tmp_str[7]; // temporary variable used in convert function

# char* convert_int16_to_str(int16_t i) { // converts int16 to string. Moreover, resulting strings will have the same length in the debug monitor.
#   sprintf(tmp_str, "%6d", i);
#   return tmp_str;
# }

# void setup() {
#   Serial.begin(9600);
#   Wire.begin();
#   Wire.beginTransmission(MPU_ADDR); // Begins a transmission to the I2C slave (GY-521 board)
#   Wire.write(0x6B); // PWR_MGMT_1 register
#   Wire.write(0); // set to zero (wakes up the MPU-6050)
#   Wire.endTransmission(true);
# }
# void loop() {
#   Wire.beginTransmission(MPU_ADDR);
#   Wire.write(0x3B); // starting with register 0x3B (ACCEL_XOUT_H) [MPU-6000 and MPU-6050 Register Map and Descriptions Revision 4.2, p.40]
#   Wire.endTransmission(false); // the parameter indicates that the Arduino will send a restart. As a result, the connection is kept active.
#   Wire.requestFrom(MPU_ADDR, 7*2, true); // request a total of 7*2=14 registers
  
#   // "Wire.read()<<8 | Wire.read();" means two registers are read and stored in the same variable
#   accelerometer_x = Wire.read()<<8 | Wire.read(); // reading registers: 0x3B (ACCEL_XOUT_H) and 0x3C (ACCEL_XOUT_L)
#   accelerometer_y = Wire.read()<<8 | Wire.read(); // reading registers: 0x3D (ACCEL_YOUT_H) and 0x3E (ACCEL_YOUT_L)
#   accelerometer_z = Wire.read()<<8 | Wire.read(); // reading registers: 0x3F (ACCEL_ZOUT_H) and 0x40 (ACCEL_ZOUT_L)
#   temperature = Wire.read()<<8 | Wire.read(); // reading registers: 0x41 (TEMP_OUT_H) and 0x42 (TEMP_OUT_L)
#   gyro_x = Wire.read()<<8 | Wire.read(); // reading registers: 0x43 (GYRO_XOUT_H) and 0x44 (GYRO_XOUT_L)
#   gyro_y = Wire.read()<<8 | Wire.read(); // reading registers: 0x45 (GYRO_YOUT_H) and 0x46 (GYRO_YOUT_L)
#   gyro_z = Wire.read()<<8 | Wire.read(); // reading registers: 0x47 (GYRO_ZOUT_H) and 0x48 (GYRO_ZOUT_L)
  
#   // print out data
#   Serial.print("aX = "); Serial.print(convert_int16_to_str(accelerometer_x));
#   Serial.print(" | aY = "); Serial.print(convert_int16_to_str(accelerometer_y));
#   Serial.print(" | aZ = "); Serial.print(convert_int16_to_str(accelerometer_z));
#   // the following equation was taken from the documentation [MPU-6000/MPU-6050 Register Map and Description, p.30]
#   Serial.print(" | tmp = "); Serial.print(temperature/340.00+36.53);
#   Serial.print(" | gX = "); Serial.print(convert_int16_to_str(gyro_x));
#   Serial.print(" | gY = "); Serial.print(convert_int16_to_str(gyro_y));
#   Serial.print(" | gZ = "); Serial.print(convert_int16_to_str(gyro_z));
#   Serial.println();
  
#   // delay
#   delay(1000);
# }