import socket,flask

UDP_IP=""
UDP_PORT=5005

app=flask.Flask(__name__)

@app.route('/')
def hello():
    return "hello flask"

def main():
    app.run(host='0.0.0.0')

    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((UDP_IP,UDP_PORT))
    while True:
            data,addr=sock.recvfrom(1024)
            print("received",data)

if __name__ == '__main__':
    main()
