
import socket,json

#raspberry pi ip address
UDP_IP="127.0.1.1"
UDP_PORT=5005

data={
	'foo':1,
	'aaa':2
}

def send():
	print("send",MESSAGE)
	sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.sendto(MESSAGE.encode('utf-8'),(UDP_IP,UDP_PORT))

MESSAGE=json.dumps(data)

send()
