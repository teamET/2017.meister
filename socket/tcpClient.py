
import socket,json,sys
#  TCP communication

#raspberry pi ip address
TCP_IP="127.0.1.1"
TCP_PORT=5005
BUFFER_SIZE=1024

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError  as e:
        return False
    return True
def send(data):
    print('data',data,'dumps',json.dumps(json.loads(data),indent=4))
    if is_json(data) is True:
        MESSAGE=json.dumps(json.loads(data))
    else:
        MESSAGE=data
    print("send",MESSAGE)
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((TCP_IP,TCP_PORT))
    sock.send(MESSAGE.encode('utf-8'))
    data=sock.recv(BUFFER_SIZE)
    sock.close()
    print('received data',data)


if __name__ == '__main__':
    if  len(sys.argv) > 1:
        send(sys.argv[1])
    else:
        while True:
            mes=input('>>input message   ')
            send(mes)
    
