import time
import board
from busio import I2C
import adafruit_bme680
# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
bme6801 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
#bme6802 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x76, debug=False)
# change this to match the location's pressure (hPa) at sea level
bme6801.sea_level_pressure = 1013.25
#bme6802.sea_level_pressure = 1013.25
while True:
    print("\nTemperature BME1: %0.1f C" % bme6801.temperature)
   # print("Temperature BME2: %0.1f C" % bme6802.temperature)
    print("Gas BME1: %d ohm" % bme6801.gas)
   # print("Gas BME2: %d ohm" % bme6802.gas)
    print("Humidity BME1: %0.1f %%" % bme6801.humidity)
   # print("Humidity BME2: %0.1f %%" % bme6802.humidity)
    print("Pressure: %0.3f hPa" % bme6801.pressure)
    print("Altitude = %0.2f meters" % bme6801.altitude)
    time.sleep(2)