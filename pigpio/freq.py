import pigpio,time,socket,asyncore,requests,datetime,json,threading
from contextlib import closing

class Motor:
    last=[0 for i in range(2)]
    current_rate=[0 for i in range(2)]
    pi=pigpio.pi()
    step=10
    pins=[]
    def __init__(self,pins):
        print('initialized pin is ',pins)
        self.pins=pins
        for pins in self.pins:
            for pin in pins:
                self.pi.set_mode(pin,pigpio.OUTPUT)
    def drive(self,port,target_rate):
#        self.current_rate[port]=self.acceleration(port,target_rate)
        self.current_rate[port]=target_rate
        print('port',port,'target',target_rate,'current',self.current_rate[port])
        if self.last[port] * target_rate < 0:
            time.sleep(0.0001)
        self.drive_pin(port,self.current_rate[port])
        self.last[port]=self.current_rate[port]
    def drive_pin(self,port,rate,BREAK=False):
        print('port:',port,'pin0,1:',self.pins[port],self.pins[0][0],self.pins[0][1],rate)
        if rate > 0:
            self.pi.set_PWM_dutycycle(self.pins[port][0],rate)
            self.pi.set_PWM_dutycycle(self.pins[port][1],0)
        elif rate <0:
            self.pi.set_PWM_dutycycle(self.pins[port][0],0)
            self.pi.set_PWM_dutycycle(self.pins[port][1],-rate)
        elif BREAK is True:
            self.pi.set_PWM_dutycycle(self.pins[port][0],254)
            self.pi.set_PWM_dutycycle(self.pins[port][1],254)

if __name__ == '__main__':
    motor=Motor([[14,15],[23,24],[8,7],[16,20]])
    scales=[261,293,329,349,391,440,494,523]
    while True:
        for scale in scales:
            print(scale)
            pi.set_PWM_frequency(14,scale)
            pi.set_PWM_frequency(15,scale)
            motor.drive(1,100)
            sleep(0.5)






