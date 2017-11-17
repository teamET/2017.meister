
import socket

#raspberry pi ip address
UDP_IP="192.168.137.93"
UDP_PORT=5005
MESSAGE=b"Hello World"

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.sendto(MESSAGE,(UDP_IP,UDP_PORT))
