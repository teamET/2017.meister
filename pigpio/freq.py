import pigpio,time,socket,asyncore,requests,datetime,json,threading
from time import sleep
from contextlib import closing

pi=pigpio.pi()
class Motor:
    global pi
    last=[0 for i in range(2)]
    current_rate=[0 for i in range(2)]
    step=10
    pins=[]
    def __init__(self,pins):
        self.pi=pi
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
#    scales=[220,233.0818808,246.9416506,261.6255653,277.182631,293.6647679,311.1269837,329.6275569,349.2282314,369.9944227,391.995436,415.3046976,440,466.1637615,493.8833013,523.2511306,554.365262,587.3295358,622.2539674,659.2551138,698.4564629,739.9888454,783.990872,830.6093952,880,932.327523,987.7666025,1046.502261,1108.730524,1174.659072,1244.507935,1318.510228,1396.912926,1479.977691,1567.981744,1661.21879,1760,1864.655046,1975.533205,2093.004522,2217.461048,2349.318143,2489.01587,2637.020455,2793.825851,2959.955382,3135.963488,3322.437581,3520]

#    score=[0,1,2,2,1,0,0,1,2,1,0,1]
    #charumera
    score=[0,1,2,1,0,None,0,1,2,1,0,1,None]
    beats=[1,1,2,1,3,1,   1,1,1,1,1,1,5]
    '''mario
    score=[2,4,2,0,2,4,None]
    beats=[0.1,0.1,0.1,0.1,0.1,0.1,5]
    '''
    while True:
        for note ,beat in zip(score,beats):
            if note is None:
                print('None')
                motor.drive(0,0)
            else:
                print(note,scales[note])
                pi.set_PWM_frequency(14,scales[note])
                pi.set_PWM_frequency(15,scales[note])
                motor.drive(0,20)
            sleep(0.5*beat)





