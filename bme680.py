import time
import csv
import board
from busio import I2C
import adafruit_bme680

EXPERIMENT_NOMENCLATURE = 'pressuretest'
# Declare CSV Header
CSV_HEADER = ['TEMPERATURE_BME', 'PRESSURE_BME ', 'HUMIDITY_BME']

# Data is only written in mode 'a', so that file cannot be overwritten
with open('/home/shojsepter/dev/log/%s.csv' %EXPERIMENT_NOMENCLATURE , 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(CSV_HEADER)

# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
#bme680_1 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x76, debug=False)
bme680_2 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x77, debug=False)

# change this to match the location's pressure (hPa) at sea level
#bme680_1.sea_level_pressure = 1013.25
bme680_2.sea_level_pressure = 1013.25
while True:


    with open('/home/shojsepter/dev/log/%s.csv' %EXPERIMENT_NOMENCLATURE , 'a') as csvfile:
        # create the csv writer
        writer = csv.writer(csvfile, delimiter=',')
        # write a row to the csv file
        # Compare with header: CSV_HEADER = ['TEMPERATURE_BME', 'PRESSURE_BME ', 'HUMIDITY_BME']
        writer.writerow([time.ctime(), "%0.1f"%bme680_2.temperature, "%0.3f"%bme680_2.pressure, "%0.1f %%"%bme680_2.humidity])
        print("wrote to file...")
        time.sleep(1)


    print(time.ctime())
    #print("\nTemperature BME1: %0.1f C" % bme680_1.temperature)
    print("Temperature BME2: %0.1f C" % bme680_2.temperature)
    #print("Gas BME1: %d ohm" % bme680_1.gas)
    print("Gas BME2: %d ohm" % bme680_2.gas)
    #print("Humidity BME1: %0.1f %%" % bme680_1.humidity)
    print("Humidity BME2: %0.1f %%" % bme680_2.humidity)
    #print("Pressure: %0.3f hPa" % bme680_1.pressure)
    print("Pressure: %0.3f hPa" % bme680_2.pressure)
    #print("Altitude = %0.2f meters" % bme680_1.altitude)
    time.sleep(2)
