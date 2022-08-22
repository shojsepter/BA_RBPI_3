import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32,GPIO.OUT)


while True:
    GPIO.output(32,False)
    time.sleep(0.0003)#1
    GPIO.output(32,True)
    time.sleep(0.0003)#2
#This is how PWM works