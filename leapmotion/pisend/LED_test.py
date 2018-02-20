#LEDデータ送信テスト
#26のデータをリスト化：送信
import os, sys, inspect,time


src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, 'lib'))
sys.path.insert(0, lib_dir)

import socket,json
#  UDP communication
#raspberry pi ip address
UDP_IP="127.0.1.1"
UDP_IP="192.168.137.132"
UDP_PORT=5005

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True
def send(message):


    print("message",message)
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(message.encode('utf-8'),(UDP_IP,UDP_PORT))

import Leap
class SampleListener(Leap.Listener):

    def on_connect(self,controller):
        print "connected"
        
    def on_frame(self,controller):
        #LED data送信テスト
        #LED SEND BEGIN
        pwm=[i for i in range(26)]
        pwm=[100,100,100,100,100,100,100,100,100,100,
             100,100,100,100,100,100,100,100,100,100,
             100,100,100,100,100,100]
        pwm_str=map(str,pwm)
        mes=','.join(pwm_str)
        #LED SEND END
if __name__=='__main__':
    main()

