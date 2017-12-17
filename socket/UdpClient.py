
import socket,json,sys
#  UDP communication

#raspberry pi ip address
UDP_IP="127.0.1.1"
UDP_PORT=5005

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True
def send(message):

    """
    if is_json(data) is True:
        MESSAGE=json.dumps(data)
    else:
        MESSAGE=data
    print("message",message)
    sock=socket.socket(socket.af_inet,socket.sock_dgram)
    sock.sendto(message.encode('utf-8'),(udp_ip,udp_port))
    """

    print("message",message)
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(message.encode('utf-8'),(UDP_IP,UDP_PORT))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        send(sys.argv[1])
    else:
        while True:
            msg=input('input message >> ')
            send(msg)
