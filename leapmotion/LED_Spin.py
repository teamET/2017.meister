# -*- coding : utf-8 -*-
#viewer側のLEDの受け取り順が間違えている可能性アリ
#tailは実装前

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
        pwm=init_pwm()
        p=254
        spin_period=200 #ms
        tail=50 #%
        #tail:回転させたときに生じる尾の割合（前のLEDの明るさに対してtail％）
        #hands
        for hand in frame.hands:
            strength = hand.grab_strength
            hand_identifier = hand.id
            hand_name = "Left hand" if hand.is_left else "Right hand"
            if hand_name=="Right hand" and strength == 1.0:
                print"Right hand"
                Led_Spin_Right(pwm,spin_period,p,tail)
            if hand_name=="Left hand" and strength == 1.0:
                print "Left Hand"
                Led_Spin_Left(pwm,spin_period,p,tail)
        
def init_pwm():
    pwm=[0 for i in range(9)]
    return pwm

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

def Led_Flash(pwm,n,m):
    #LEDがmainで取得した状態を保ちながら周期nミリ秒でm秒点滅する.
    #global led_status
    pwm_current=pwm
    print(pwm_current)
    n=n*0.0005
    m/=2
    count=0
    while(True):
        pwm=[0 for i in range(9)]
        L_status_update(pwm)
    
        sleep(n)
        pwm=[pwm_current[i] for i in range(9)]
        L_status_update(pwm)
        if count==(m/n):
            break
        count+=1
        sleep(n)
    pwm=pwm_current
    L_status_update(pwm)

def Led_Flash_update(pwm,n,m,y):
    #LEDが現在(取得した状態）の状態を"""更新し続けながら"""周期nミリ秒でm秒点滅する.
    pwm_current=pwm
    print(pwm_current)
    n=n*0.0005
    pwm=[0 for i in range(9)]
    L_status_update(pwm)
    sleep(n)
    pwm=[pwm_current[i] for i in range(9)]
    L_status_update(pwm)
    sleep(n)
    if count==(m/2) : ck=0
    else : ck=1
    return ck

def L_status_update(pwm):
    for i in range(9):
        led_status[i]=pwm[i]
        Led_Send(pwm)

def Led_Spin_Right(pwm,n,p,tail):
    #Nミリ秒で1回転する(時計回り)
    #pは光の明るさ
    #tailは尾の長さ
    #atode
    n*=0.000125
    round_order=[1,2,5,8,7,6,3,0]
    pwm=init_pwm()
    for i in range(8):
        pwm=init_pwm()
        pwm[round_order[i]]=p
        L_status_update(pwm)
        sleep(n)

def Led_Spin_Left(pwm,n,p,tail):
    #Nミリ秒で1回転する(半時計回り)
    #pは光の明るさ
    #tailは尾の長さ
    #atode
    n*=0.000125
    round_order=[1,0,3,6,7,8,5,2]
    pwm=init_pwm()
    for i in range(8):
        pwm=init_pwm()
        pwm[round_order[i]]=p
        L_status_update(pwm)
        sleep(n)

def main():
    global led_status

    listener=SampleListener()
    controller=Leap.Controller()
    controller.add_listener(listener)
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    controller.set_policy(controller.POLICY_IMAGES)
    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    #Controller.set_policy
    

    #Tkinter
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

