import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)	
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(32,GPIO.OUT)
pi_pwm = GPIO.PWM(32,8000)		#create PWM instance with frequency
pi_pwm.start(90)				#start PWM of required Duty Cycle 
time.sleep(50)
GPIO.cleanup()

