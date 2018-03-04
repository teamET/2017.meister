import pigpio,time,socket,asyncore,requests,datetime,json,threading
from contextlib import closing

import matrix,motor

""" 
led,motor pin defination

Motor : ([[14,15],[23,24],[8,7],[16,20]])
LED   : (2, 3, 4, 5, 6, 9, 10, 11, 12)

"""
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
                    pwm_str=raw.split(',')
                    for pwm in map(int,pwm_str):
                        self.data[cnt]=pwm
                        cnt+=1
                    print(self.data)
                else:
                    print('empty message or not json ')
#                time.sleep(1)

if __name__ == '__main__' :
    motor=motor.Motor([[14,15],[23,24],[8,7],[16,20]])
    pwms=[0 for i in range(28)]
#    print(pwms,pwms[4::])
    led=matrix.LED()
    server=SubUdpServer(pwms)
    server.setDaemon(True)
    server.start()
    print('=== Main Thread  Starts ===')
    while True:
        print('motor',pwms[0:4:],'led',pwms[4:13:])
        for i in range(4):
            motor.drive(i,pwms[i]);
        led.upall(pwms[4:13:]);
        
