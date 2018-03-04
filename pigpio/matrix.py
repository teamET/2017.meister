import pigpio,time,socket,asyncore,requests,datetime,json,threading
from contextlib import closing

#pins=(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27)
pins=(2, 3, 4, 5, 6, 9, 10, 11, 12)
class LED:
    pi=pigpio.pi()
    def __init__(self):
        print('initialize led pin')
        for i in pins:
            self.pi.set_mode(i,pigpio.OUTPUT)
    def upall(self,pwm):
        print('led upall pwm: ',pwm,'pins : ',pins)
        c=0
        for p in pwm:
            self.pi.set_PWM_dutycycle(pins[c],p)
            c+=1
    def up(self,pin,pwm):
        self.pi.set_PWM_dutycycle(pin,pwm)


if __name__ == '__main__' :
    led_pwm=[254 for i in range(28)]
    led=LED()
    print('=== Main Thread  Starts ===')
    while True:
        for pin in pins:
            led.up(pin,254)
            time.sleep(0.5)
            led.up(pin,0)


