import pigpio
import time

pi=pigpio.pi()
pi.set_mode(2,pigpio.OUTPUT)

for i in range(5):
    for j in range(256):
        pi.set_PWM_dutycycle(2,j)
        time.sleep(0.1)
