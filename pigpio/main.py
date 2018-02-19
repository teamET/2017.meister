import time,socket,asyncore,requests,datetime,json,threading,
import subprocess,logging
from contextlib import closing

<<<<<<< HEAD
pins=(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27)
class LED:
    pi=pigpio.pi()
    def __init__(self):
        print('initialize led pin')
        for i in pins:
            self.pi.set_mode(i,pigpio.OUTPUT)
    def up(self,pwm):
        for pin in pins:
#            print('pin',pin,'pwm',pwm[pin])
            self.pi.set_PWM_dutycycle(pin,pwm[pin])

#pulse width  modulation data
#data={ 'right':0, 'left':0 }
=======
pins=[14,15,23,24]
>>>>>>> e25c69b92efb5d33c65f8284a235433d8fa3ab12
class Motor:
    import pigpio
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
    def run(self):
        print('===  Sub Thread Starts===')
<<<<<<< HEAD
        print("PORT",self.UDP_PORT)
#        print('sub id',id(self.data))
#        print('sub right',self.data["right"],'left',self.data["left"])
=======
>>>>>>> e25c69b92efb5d33c65f8284a235433d8fa3ab12
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        with closing(sock):
            sock.bind((self.UDP_IP,self.UDP_PORT))
            while True:
                mes=sock.recv(self.bufsize)
                raw=mes.decode('utf-8')
                print('mes',mes,'raw',raw)
<<<<<<< HEAD
                if raw == 'q':
                    print('Sub process is terminated')
                    break
                elif raw is not '' : #and  self.is_json(raw) ==True:
                    #led
                    pwm_str=raw.split(',')
                    for i,j in range(26),map(int,pwm_str):
                        self.data[i]=j
                    print(self.data)
                    #motor
                    """
                    tmp=json.loads(raw)
                    self.data['right']=tmp['right']
                    self.data['left']=tmp['left']
                    """
                else:
                    print('empty message or not json ')
#                print('Udp right',self.data["right"],'left',self.data["left"])
                time.sleep(1)

if __name__ == '__main__':
#    motor=Motor([14,15,23,24])
#    data={ 'right':0, 'left':0 }
#    print("max pin number:",pins[:-1:])
    led_pwm=[0 for i in range(28)]
#    for i in pins:
#        led_pwm[i]=0
    led=LED()
=======
                try:
                    tmp=json.loads(raw)
                except:
                    print("not json")
                else:
					for key,value in tmp.iteritems():
						seld.data[key]=value
#					self.data["right"]=tmp.get("right",0)
#					self.data["left"]=tmp.get("left",0)
                    print('Udp right',self.data["right"],'left',self.data["left"])

if __name__ == '__main__':
	logging.basicConfig(filename=time.time()+'.log',level=logging.DEBUG)
    motor=Motor([14,15])
    data={ 'right':0, 'left':0 }
>>>>>>> e25c69b92efb5d33c65f8284a235433d8fa3ab12

    #Udp Server setup
#    server=SubUdpServer(data)
    server=SubUdpServer(led_pwm)
    server.setDaemon(True)
    server.start()
#    time.sleep(1)
    print('=== Main Thread  Starts ===')


    while True:
<<<<<<< HEAD
        print('led_pwm',led_pwm)
        led.up(led_pwm);
        """
        for i in range(26):
            led.up(i,led_pwm[i]);
            """
#        time.sleep(1)
#        print('motor.drive right',data["right"],'left',data["left"])
#        motor.drive(0,data['right'])
#        motor.drive(1,data['left'])
=======
        time.sleep(1)
        print('motor.drive right',data["right"],'left',data["left"])
        motor.drive(0,data['right'])
        motor.drive(1,data['left'])
		logging.info("subp -> "+subprocess.run(data.get("command",":") ))


		
>>>>>>> e25c69b92efb5d33c65f8284a235433d8fa3ab12




