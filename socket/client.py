import socket

host="JET39"
port=80

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
client.connect((host,port))
client.send("from raspberry pi")
while True:
    print(client.recv(4096))
