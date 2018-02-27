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
#        print('sub id',id(self.data))
        print('sub right',self.data["right"],'left',self.data["left"])
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        with closing(sock):
            sock.bind((self.UDP_IP,self.UDP_PORT))
            while True:
                mes=sock.recv(self.bufsize)
                raw=mes.decode('utf-8')
                print('mes',mes,'raw',raw)
                if raw == 'q':
                    print('Sub process is terminated')
                    break
                elif raw is not '' : #and  self.is_json(raw) ==True:
                    tmp=json.loads(raw)
                    self.data['right']=tmp['right']
                    self.data['left']=tmp['left']
                else:
                    print('empty message or not json ')
                print('Udp right',self.data["right"],'left',self.data["left"])
                time.sleep(1)

#pins=(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27)
if __name__ == '__main__':
    motor=Motor([[14,15],[23,24],[8,7],[16,20]])
    while True:
#       motor.drive(0,250)
        for pwm in range(-254,254,20):
            print('pwm up :',pwm)
            motor.drive(0,pwm)
            motor.drive(1,pwm)
            time.sleep(0.5)
        for pwm in range(254,-254,-20):
            print('pwm down:',pwm)
            motor.drive(0,pwm)
            motor.drive(1,pwm)
            time.sleep(0.5)






