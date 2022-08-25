import time
import board
from busio import I2C
import adafruit_bme680
# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
bme680_1 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x76, debug=False)
bme680_2 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x77, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680_1.sea_level_pressure = 1013.25
bme680_2.sea_level_pressure = 1013.25
while True:
    print(time.ctime())
    print("\nTemperature BME1: %0.1f C" % bme680_1.temperature)
    print("Temperature BME2: %0.1f C" % bme680_2.temperature)
    print("Gas BME1: %d ohm" % bme680_1.gas)
    print("Gas BME2: %d ohm" % bme680_2.gas)
    print("Humidity BME1: %0.1f %%" % bme680_1.humidity)
    print("Humidity BME2: %0.1f %%" % bme680_2.humidity)
    print("Pressure: %0.3f hPa" % bme680_1.pressure)
    print("Altitude = %0.2f meters" % bme680_1.altitude)
    time.sleep(2)
