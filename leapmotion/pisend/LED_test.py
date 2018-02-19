
import socket,json,time
#  UDP communication
#raspberry pi ip address
UDP_IP="127.0.1.1"
UDP_IP="192.168.137.113"
UDP_PORT=5005
cnt=0

def send(message):
    print("message",message)
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(message.encode('utf-8'),(UDP_IP,UDP_PORT))


pwm=[i for i in range(26)]
pwm=[100,100,100,100,100,100,100,100,100,100,
     100,100,100,100,100,100,100,100,100,100,
     100,100,100,100,100,100]
while True:
    pwm[0]=cnt
    cnt=cnt+1
    pwm_str=map(str,pwm)
    mes=','.join(pwm_str)
    send(mes)
    print(mes)
    time.sleep(0.01)
