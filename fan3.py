import sys
import time

import navio.pwm
import navio.util

navio.util.check_apm()

with navio.pwm.PWM(1) as pwm:
    time.sleep(0.1)
    pwm.set_period(50)
    time.sleep(0.1)
    pwm.enable()
    time.sleep(0.1)

    while True:
        pwm.set_duty_cycle(float(sys.argv[1]))
        time.sleep(0.1)