import pigpio,time,socket,asyncore,requests,datetime,json,threading
from contextlib import closing

#motor=Motor([[14,15],[23,24],[8,7],[16,20]])
#pins=(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27)
pins=(2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 18, 19, 20, 21, 22, 25, 26, 27)

class LED:
    pi=pigpio.pi()
    def __init__(self):
        print('initialize led pin')
        for i in pins:
            self.pi.set_mode(i,pigpio.OUTPUT)
    def up(self,pwm):
        for pin in pins:
            self.pi.set_PWM_dutycycle(pin,pwm[pin])

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
    def acceleration(self,port,target):
        if target > self.last[port]:
            return  self.last[port]+self.step
        elif target < self.last[port]:
            return self.last[port]-self.step
        else :
            return self.last[port]

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


#sub  thread  UDP server
class  SubUdpServer(threading.Thread):
    def __init__(self,shared_data):
        super(SubUdpServer,self).__init__()
        self.UDP_IP=""
        self.UDP_PORT=5005
        self.backlog=10
        self.bufsize=1024
        self.data=shared_data
    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError as e:
            return False
        return True
    def run(self):
        print('===  Sub Thread Starts===')
        print("PORT",self.UDP_PORT)
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        with closing(sock):
            sock.bind((self.UDP_IP,self.UDP_PORT))
            while True:
                cnt=0
                mes=sock.recv(self.bufsize)
                raw=mes.decode('utf-8')
                print('mes',mes,'raw',raw)
                if raw == 'q':
                    print('Sub process is terminated')
                    break
                elif raw is not '' : #and  self.is_json(raw) ==True:
                    #led
                    pwm_str=raw.split(',')
                    for pwm in map(int,pwm_str):
                        self.data[cnt]=pwm
                        cnt+=1
                    print(self.data)
                else:
                    print('empty message or not json ')
#                time.sleep(1)

if __name__ == '__main__' :
    motor=Motor([[14,15],[23,24],[8,7],[16,20]])
    pwms=[254 for i in range(28)]
    led=LED()
    server=SubUdpServer(pwms)
    server.setDaemon(True)
    server.start()
    print('=== Main Thread  Starts ===')
    while True:
        for i in range(4):
            motor.drive(i,pwms[i]);
        led.up(pwms[4::]);
        print('motor',pwms[0:3:],'led',pwms[4::])
        
