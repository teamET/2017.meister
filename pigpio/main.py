import pigpio,time

class Motor:
    last=[0,0,0,0]
    pi=pigpio.pi()
    def __init__(self,pins):
        print('initialized pin is ',pins)
        for pin in pins:
            self.pi.set_mode(pin,pigpio.OUTPUT)

    def drive(self,port,rate):
        self.last[port]=rate
        if self.last[port] * rate < 0:
            time.sleep(0.0001)
        if port is 0:
            self.drive_pin(14,15,rate)
        elif port is 1:
#            drive_pin()
            pass
        else:
            pass
    def drive_pin(self,pin1,pin2,rate,BREAK=False):
        if rate > 0:
            self.pi.set_PWM_dutycycle(pin1,rate)
        elif rate <0:
            self.pi.ser_PWM_dutycycle(pin2.rate)
        elif BREAK is True:
            self. pi.set_PWM_dutycycle(pin1,100)
            self.pi.set_PWM_dutycycle(pin2,100)

if __name__ == '__main__':
    motor=Motor([14,15])
    motor.drive(0,50)
