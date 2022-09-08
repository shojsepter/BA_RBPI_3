import time
import csv
import board
from busio import I2C
import adafruit_bme680
import TCA9548A

def get_bme680_values(BME):
        
    if BME == "BME_IN":
        TCA9548A.I2C_setup(0x70, 1)
        time.sleep(0.01)
        i2c = I2C(board.SCL, board.SDA)
        bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x77, debug=False)
        time.sleep(2)

    elif BME == "BME_OUT":
        TCA9548A.I2C_setup(0x70, 0)
        time.sleep(0.01)
        i2c = I2C(board.SCL, board.SDA)
        bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x77, debug=False)
        time.sleep(2)

    elif BME == "BME_CHAMBER":
        i2c = I2C(board.SCL, board.SDA)
        bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x76, debug=False)
        time.sleep(2)

    return "%0.1f"%bme680.temperature, "%0.3f"%bme680.pressure, "%0.1f %%"%bme680.humidity,  "%d ohm"%bme680.gas
