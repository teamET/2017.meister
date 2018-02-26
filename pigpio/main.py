import pigpio,time,socket,asyncore,requests,datetime,json,threading
from contextlib import closing

pins=(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27)
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
            self.pi.set_PWM_dutycycle(pin2.rate)
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


mode='__LED__'
print("mode : ",mode)


if __name__ == '__main__' :
#Udp Server setup
#server=SubUdpServer(data)

    if mode == '__LED__':
        led_pwm=[0 for i in range(28)]
        led=LED()
        server=SubUdpServer(led_pwm)
        server.setDaemon(True)
        server.start()
        print('=== Main Thread  Starts ===')
        while True:
            pass
            """
            for i in range(26):
                led.up(i,led_pwm[i]);
                """
    elif mode =='__MOTOR__':
        motor=Motor([14,15,23,24])
        while True:
            print('motor.drive right')
            motor.drive(0,100)
            motor.drive(1,100)





