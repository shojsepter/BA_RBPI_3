import mybme680
import time
import csv

# Declare Filename
EXPERIMENT_NOMENCLATURE = 'BME_calibration'
# Declare CSV Header
CSV_HEADER = ['TIME', 'TEMPERATURE_IN_BME', 'TEMPERATURE_OUT_BME', 'TEMPERATURE_C_BME', 'PRESSURE_IN_BME ', 'PRESSURE_OUT_BME', 'PRESSURE_C_BME', 'HUMIDITY_IN_BME', 'HUMIDITY_OUT_BME', 'HUMIDITY_C_BME']

# Data is only written in mode 'a', so that file cannot be overwritten
with open('/home/shojsepter/dev/log/%s.csv' %EXPERIMENT_NOMENCLATURE , 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(CSV_HEADER)

while True:
    
    bme680_IN_t, bme680_IN_p, bme680_IN_h = mybme680.get_bme680_values("BME_IN")
    bme680_OUT_t, bme680_OUT_p, bme680_OUT_h = mybme680.get_bme680_values("BME_OUT")
    bme680_C_t, bme680_C_p, bme680_C_h = mybme680.get_bme680_values("BME_CHAMBER")

    with open('/home/shojsepter/dev/log/%s.csv' %EXPERIMENT_NOMENCLATURE , 'a') as csvfile:
        # create the csv writer
        writer = csv.writer(csvfile, delimiter=',')
        # write a row to the csv file
        # Compare with header: CSV_HEADER = ['TIME', 'TEMPERATURE_IN_BME', 'TEMPERATURE_OUT_BME', 'PRESSURE_IN_BME ', 'PRESSURE_OUT_BME', 'HUMIDITY_IN_BME', 'HUMIDITY_OUT_BME','HUMIDITY_OUT_SCD', 'AIRFLOW_OUT_SFM', 'CO2_OUT_SCD']
        writer.writerow([time.ctime(), bme680_IN_t, bme680_OUT_t, bme680_C_t, bme680_IN_p, bme680_OUT_p, bme680_C_p, bme680_IN_h, bme680_OUT_h, bme680_C_h])
        print("wrote to file...")
        time.sleep(1)