import pigpio,time
import socket,requests,datetime,json

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
        print('current',current_rate)
        if self.last[port] * target_rate < 0:
            time.sleep(0.0001)
        if port is 0:
            print('current',current_rate)
            self.drive_pin(14,15,current_rate)
        elif port is 1:
#            drive_pin()
            pass
        else:
            pass
        self.last[port]=target_rate
    def drive_pin(self,pin1,pin2,rate,BREAK=False):
        if rate > 0:
            self.pi.set_PWM_dutycycle(pin1,rate)
        elif rate <0:
            self.pi.ser_PWM_dutycycle(pin2.rate)
        elif BREAK is True:
            self. pi.set_PWM_dutycycle(pin1,100)
            self.pi.set_PWM_dutycycle(pin2,100)

class Server:
    UDP_IP=""
    UDP_PORT=5005
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def __init__(self):
        self.sock.bind((self.UDP_IP,self.UDP_PORT))

    def read():
        return val1,val2

if __name__ == '__main__':
    motor=Motor([14,15])
    server=Server()
    while True:
            raw_data,addr=server.sock.recvfrom(1024)
            print("received",raw_data)
            data=json.loads(raw_data.decode('utf-8'))
            print('right %d left %d'%(data['right'],data['left']))
            motor.drive(0,data['right'])
            motor.drive(1,data['left'])




