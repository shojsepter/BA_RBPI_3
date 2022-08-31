import csv
import time
import board
from busio import I2C
import adafruit_bme680
from smbus2 import SMBus, i2c_msg
import struct
from typing import List

# Declare Filename
EXPERIMENT_NOMENCLATURE = 'test6'
# Declare CSV Header
CSV_HEADER = ['TIME', 'TEMPERATURE_IN_BME', 'TEMPERATURE_OUT_BME', 'PRESSURE_IN_BME ', 'PRESSURE_OUT_BME', 'HUMIDITY_IN_BME', 'HUMIDITY_OUT_BME', 'AIRFLOW_OUT_SFM', 'CO2_OUT_SCD']

def SCD30_conversion(data: List[int]) -> tuple[int, int, float] :

    """takes in relevant bits and casts a float like described in the datasheet. Other than the SFM, the conversions for the SCD are all the same, so the funciton is called 3 times"""

    byte_1 = hex(data[0])[2:].zfill(2)
    byte_2 = hex(data[1])[2:].zfill(2)
    byte_3 = hex(data[2])[2:].zfill(2)
    byte_4 = hex(data[3])[2:].zfill(2)

    bytes_merged = byte_1+byte_2+byte_3+byte_4
    float_value = struct.unpack('!f', bytes.fromhex(bytes_merged))[0]

    return float_value

def SFM3003300CL_conversion(data: List[int]) -> tuple[float, float]:

    """takes in relevant bits and casts a float like described in the datasheet"""

    OFFSET_FLOW = -24576 # [-]
    SCALEFACTOR_FLOW = 170 # [slm^-1]
    OFFSET_TEMP = 0 # [-]
    SCALEFACTOR_TEMP = 200 # [°C^-1]
    
    flow_bytes_converted = bytes(data[0:2])
    flow_raw = int.from_bytes(flow_bytes_converted, byteorder='big', signed=True)
    flow = float((flow_raw-OFFSET_FLOW)/SCALEFACTOR_FLOW)

    temp_bytes_converted = bytes(data[2:4])
    temp_raw = int.from_bytes(temp_bytes_converted, byteorder='big', signed=True)
    temp = float((temp_raw-OFFSET_TEMP)/SCALEFACTOR_TEMP)

    return flow, temp


# Data is only written in mode 'a', so that file cannot be overwritten
with open('/home/shojsepter/dev/log/%s.csv' %EXPERIMENT_NOMENCLATURE , 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(CSV_HEADER)

########                                                 ########
########--------------- SENSOR SETUP --------------------########
########                                                 ########


########                     BME680                      ########
# Create object using adadfruit library and I2C port
i2c = I2C(board.SCL, board.SDA)
bme680_IN = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x76, debug=False)
bme680_OUT = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x77, debug=False)
# change this to match the location's pressure (hPa) at sea level
bme680_IN.sea_level_pressure = 1013.25
bme680_OUT.sea_level_pressure = 1013.25

########                     SCD30                       ########
SCD30_START_MEASUREMENT = i2c_msg.write(0x61, [0x00, 0x10, 0x00, 0x00, 0x81])
SCD30_START_READ_MEASUREMENT = i2c_msg.write(0x61, [0x03, 0x00])
SCD30_READ_MEASUREMENT = i2c_msg.read(0x61, 18)
SCD30_STOP_MEASUREMENT = i2c_msg.write(0x28, [0x3F, 0xF9])

bus = SMBus(1)
bus.i2c_rdwr(SCD30_START_MEASUREMENT) # measurement Interval is 2s!!!

########                 SFM3003300CL                    ########
#SFM3003300CL_START_MEASUREMENT = i2c_msg.write(0x28, [0x36, 0x08])
#SFM3003300CL_READ_MEASUREMENT = i2c_msg.read(0x28, 9)
#SFM3003300CL_STOP_MEASUREMENT = i2c_msg.write(0x28, [0x3F, 0xF9])

# prevent Error in case sensor is already started -> stop and start
#bus.i2c_rdwr(SFM3003300CL_STOP_MEASUREMENT)
#time.sleep(0.5)
#bus.i2c_rdwr(SFM3003300CL_START_MEASUREMENT)

# wait for sensors to wake up
time.sleep(2)

while True:

    # Get data from SCD30 and do calculations later for less latency between measurements
    bus.i2c_rdwr(SCD30_START_READ_MEASUREMENT)
    time.sleep(0.01)
    bus.i2c_rdwr(SCD30_READ_MEASUREMENT)
    SCD30_data = list(SCD30_READ_MEASUREMENT)

    #bus.i2c_rdwr(SFM3003300CL_READ_MEASUREMENT)
    #SFM3003300CL_data = list(SFM3003300CL_READ_MEASUREMENT)

    SCD30_CO2_bytes = list(SCD30_data[i] for i in [0, 1, 3, 4])
    SCD30_CO2 = SCD30_conversion(SCD30_CO2_bytes)
    SCD30_Temp_bytes = list(SCD30_data[i] for i in [6, 7, 9, 10])
    SCD30_Temp = SCD30_conversion(SCD30_Temp_bytes)
    SCD30_Hum_bytes = list(SCD30_data[i] for i in [12, 13, 15, 16])
    SCD30_Hum = SCD30_conversion(SCD30_Hum_bytes)

    #SFM3003300CL_bytes = list(SFM3003300CL_data[i] for i in [0, 1, 3, 4])
    #SFM3003300CL_flow, SFM3003300CL_temp = SFM3003300CL_conversion(SFM3003300CL_bytes)


    with open('/home/shojsepter/dev/log/%s.csv' %EXPERIMENT_NOMENCLATURE , 'a') as csvfile:
        # create the csv writer
        writer = csv.writer(csvfile, delimiter=',')
        # write a row to the csv file
        # Compare with header: CSV_HEADER = ['TIME', 'TEMPERATURE_IN_BME', 'TEMPERATURE_OUT_BME', 'PRESSURE_IN_BME ', 'PRESSURE_OUT_BME', 'HUMIDITY_IN_BME', 'HUMIDITY_OUT_BME','HUMIDITY_OUT_SCD', 'AIRFLOW_OUT_SFM', 'CO2_OUT_SCD']
        writer.writerow([time.ctime(), "%0.1f"%bme680_IN.temperature, "%0.1f"%bme680_OUT.temperature,  "%0.3f"%bme680_IN.pressure, "%0.3f"%bme680_OUT.pressure, "%0.1f %%"%bme680_IN.humidity, "%0.1f %%"%bme680_OUT.humidity, SCD30_Hum, "SFM3003300CL_flow", SCD30_CO2])
        print("wrote to file...")
        time.sleep(5)


