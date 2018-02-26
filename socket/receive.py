import socket,requests,datetime

UDP_IP=""
UDP_PORT=5005



sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))
while True:
	data,addr=sock.recvfrom(1024)
	print("received",data)
if __name__ == '__main__':
    main()


