import csv
import time
import board
from busio import I2C
import adafruit_bme680
from smbus2 import SMBus, i2c_msg
import struct
from typing import List
import mybme680
import TCA9548A
import DS18B20

# Declare Filename
EXPERIMENT_NOMENCLATURE = 'larvae_experiment'
# Declare CSV Header
CSV_HEADER = ['TIME', 'TEMPERATURE_IN_BME', 'TEMPERATURE_IN_SCD', 'TEMPERATURE_IN_DS', 'TEMPERATURE_OUT_BME', 'TEMPERATURE_OUT_SCD', 'TEMPERATURE_OUT_DS', 'TEMPERATURE_OUT_SFM', 'TEMPERATURE_C_BME', 'TEMPERATURE_C1_DS', 'TEMPERATURE_C2_DS', 'TEMPERATURE_C3_DS', 'HUMIDITY_IN_BME', 'HUMIDITY_IN_SCD', 'HUMIDITY_OUT_BME', 'HUMIDITY_OUT_SCD', 'CO2_IN_SCD', 'CO2_OUT_SCD', 'PRESSURE_IN_BME ', 'PRESSURE_OUT_BME', 'PRESSURE_C_BME', 'AIRFLOW_OUT_SFM', 'GAS_IN', 'GAS_OUT']

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


########                     SCD30                       ########
SCD30_START_MEASUREMENT = i2c_msg.write(0x61, [0x00, 0x10, 0x00, 0x00, 0x81])
SCD30_START_READ_MEASUREMENT = i2c_msg.write(0x61, [0x03, 0x00])
SCD30_READ_MEASUREMENT = i2c_msg.read(0x61, 18)
SCD30_STOP_MEASUREMENT = i2c_msg.write(0x28, [0x3F, 0xF9])

bus = SMBus(1)
bus.i2c_rdwr(SCD30_START_MEASUREMENT) # measurement Interval is 2s!!!
time.sleep(1)


# wait for sensors to wake up
time.sleep(2)

while True:
    try:
        # Get data from SCD30 and do calculations later for less latency between measurements
        bus.i2c_rdwr(SCD30_START_READ_MEASUREMENT)
        time.sleep(0.01)
        bus.i2c_rdwr(SCD30_READ_MEASUREMENT)
        SCD30_OUT_data = list(SCD30_READ_MEASUREMENT)
    except:
        pass

    try:
        SCD30_CO2_bytes = list(SCD30_OUT_data[i] for i in [0, 1, 3, 4])
        SCD30_OUT_CO2 = SCD30_conversion(SCD30_CO2_bytes)
        SCD30_Temp_bytes = list(SCD30_OUT_data[i] for i in [6, 7, 9, 10])
        SCD30_OUT_Temp = SCD30_conversion(SCD30_Temp_bytes)
        SCD30_Hum_bytes = list(SCD30_OUT_data[i] for i in [12, 13, 15, 16])
        SCD30_OUT_Hum = SCD30_conversion(SCD30_Hum_bytes)
    except:
        pass
    
    try:
        bme680_IN_t, bme680_IN_p, bme680_IN_h, bme680_IN_g = mybme680.get_bme680_values("BME_IN")
    except:
        pass

    bme680_OUT_t, bme680_OUT_p, bme680_OUT_h = [0,0,0] #mybme680.get_bme680_values("BME_OUT")
    try:
        bme680_C_t, bme680_C_p, bme680_C_h, bme680_C_g = mybme680.get_bme680_values("BME_CHAMBER")
    except:
        pass

    TEMPERATURE_IN_DS = DS18B20.read_sensor("28-00000de73a3c")
    TEMPERATURE_OUT_DS = DS18B20.read_sensor("28-00000de72894")
    TEMPERATURE_C1_DS = DS18B20.read_sensor("28-00000de7c112")
    TEMPERATURE_C2_DS = DS18B20.read_sensor("28-00000de78429")
    TEMPERATURE_C3_DS = DS18B20.read_sensor("28-00000de720d4")


    with open('/home/shojsepter/dev/log/%s.csv' %EXPERIMENT_NOMENCLATURE , 'a') as csvfile:
        # create the csv writer
        writer = csv.writer(csvfile, delimiter=',')
        # write a row to the csv file
        # CSV_HEADER = ['TIME', 'TEMPERATURE_IN_BME', 'TEMPERATURE_IN_SCD', 'TEMPERATURE_IN_DS', 'TEMPERATURE_OUT_BME', 'TEMPERATURE_OUT_SCD', 'TEMPERATURE_OUT_DS', 'TEMPERATURE_OUT_SFM', 'TEMPERATURE_C_BME', 'TEMPERATURE_C1_DS', 'TEMPERATURE_C2_DS', 'TEMPERATURE_C3_DS', 'HUMIDITY_IN_BME', 'HUMIDITY_IN_SCD', 'HUMIDITY_OUT_BME', 'HUMIDITY_OUT_SCD', 'CO2_IN_SCD', 'CO2_OUT_SCD', 'PRESSURE_IN_BME ', 'PRESSURE_OUT_BME', 'PRESSURE_C_BME', 'AIRFLOW_OUT_SFM', 'GAS_IN', 'GAS_OUT', 'HUMIDITY_C_BME']
        writer.writerow([time.ctime(), bme680_IN_t, 'SCD30_IN_Temp', TEMPERATURE_IN_DS, 'bme680_OUT_t', SCD30_OUT_Temp, TEMPERATURE_OUT_DS, 'SFM3003300CL_temp', bme680_C_t, TEMPERATURE_C1_DS, TEMPERATURE_C2_DS, TEMPERATURE_C3_DS, bme680_IN_h, 'SCD30_IN_Hum', 'bme680_OUT_h', SCD30_OUT_Hum, 'SCD30_IN_CO2', SCD30_OUT_CO2, bme680_IN_p, 'bme680_OUT_p', bme680_C_p, 'SFM3003300CL_flow', bme680_IN_g, bme680_C_g, bme680_C_h])
        print("wrote to file...")
    
    time.sleep(51)


