def read_sensor(sensor):
    tempfile = open("/sys/bus/w1/devices/{}/w1_slave".format(sensor))
    temptext = tempfile.read()
    tempfile.close()
    tempcelsius = temptext.split("\n")[1].split(" ")[9]
    temperature = float(tempcelsius[2:])
    temperature = temperature / 1000
    return temperature