# -*- coding : utf-8 -*-
import os, sys, inspect,time
from time import sleep

import viewer
from viewer import led_status

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, 'lib'))
sys.path.insert(0, lib_dir)


import socket,json
#  UDP communication
#raspberry pi ip address
UDP_IP="192.168.0.100"
UDP_PORT=5005

"""""""""""""""
定数定義
Y_MAX:最大の高さ
Y_MIN:最小の高さ

LEDの送信デューティー比の最大：254
LEDの送信デューティー比の最小：0

"""""""""""""""
Y_MAX=430
Y_MIN=40

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
        frame=controller.frame()
        hand = frame.hands.rightmost
        finger=frame.finger
        global led_status
        #hands
        for hand in frame.hands:
            pointable = frame.pointables.frontmost
            position = pointable.tip_position
            y=position.y #variable=vector.(x,y,z)
            #print(y)
            #position.y.range = 40 to 430
            #LED: 0 to 254 
            p=Led_Brightness(y)
            #print(p)
            pwm=Led_All(int(p))
            Led_Send(pwm)
            for i in range(9):
                led_status[i]=pwm[i]
            

def Led_All(p):
    pwm=[p for i in range(9)]
    return pwm

def Led_Brightness(y):
    p=(254.0/(Y_MAX - Y_MIN))*(y-Y_MIN)
    #一般式
    #a-b の範囲の時 x=254/(b-a)*(y-a))
    if p>254:
        p=254
    elif p<0:
        p=0
    return p

def Led_Send(pwm):
    print "pwm={}".format(pwm)
    #LED SEND BEGIN
    pwm_str=map(str,pwm)
    mes=','.join(pwm_str)
    send(mes)
    #LED SEND END
            
def main():
    global led_status
    
    
    listener=SampleListener()
    controller=Leap.Controller()
    controller.add_listener(listener)
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    controller.set_policy(controller.POLICY_IMAGES)
    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    #Controller.set_policy
    
    v=viewer.viewer()
    v.setDaemon(True)
    v.start()

    pointable = frame.pointables.frontmost
    direction = pointable.direction
    length = pointable.length
    width = pointable.width
    stabilizedPosition = pointable.stabilized_tip_position
    position = pointable.tip_position
    speed = pointable.tip_velocity
    touchDistance = pointable.touch_distance
    zone = pointable.touch_zone

    
    print "Press Enter to Quit"
    try:
        sys.stdin.readline()
    except KeyboardInterpt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__=='__main__':
    main()
