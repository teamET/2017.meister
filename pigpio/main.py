import pigpio,time,socket,asyncore,requests,datetime,json,threading
from contextlib import closing


#pulse width  modulation data
#data={ 'right':0, 'left':0 }
class Motor:
    last=[0,0,0,0]
    pi=pigpio.pi()
    def __init__(self,pins):
        print('initialized pin is ',pins)
        for pin in pins:
            self.pi.set_mode(pin,pigpio.OUTPUT)
    def acceleration(self,port,target):
        if target > self.last[port]:
            return  self.last[port]+2
        elif target < self.last[port]:
            return self.last[port]-2
        else :
            return self.last[port]

    def drive(self,port,target_rate):
        current_rate=self.acceleration(port,target_rate)
        print('port',port,'target',target_rate,'current',current_rate)
        if self.last[port] * target_rate < 0:
            time.sleep(0.0001)
        if port is 0:
            self.drive_pin(14,15,current_rate)
        elif port is 1:
            self.drive_pin(23,24,current_rate)
        else:
            print('unknown port')
        self.last[port]=current_rate
    def drive_pin(self,pin1,pin2,rate,BREAK=False):
        if rate > 0:
            self.pi.set_PWM_dutycycle(pin1,rate)
        elif rate <0:
            self.pi.ser_PWM_dutycycle(pin2.rate)
        elif BREAK is True:
            self.pi.set_PWM_dutycycle(pin1,100)
            self.pi.set_PWM_dutycycle(pin2,100)

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

if __name__ == '__main__':
    motor=Motor([14,15,23,24])
    data={ 'right':0, 'left':0 }

    #Udp Server setup
    server=SubUdpServer(data)
    server.setDaemon(True)
    server.start()
#    time.sleep(1)
    print('=== Main Thread  Starts ===')
#    print('main id ',id(data))
    
    while True:
#        time.sleep(1)
        print('motor.drive right',data["right"],'left',data["left"])
        motor.drive(0,data['right'])
        motor.drive(1,data['left'])




