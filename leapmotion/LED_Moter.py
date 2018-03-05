# -*- coding: utf-8 -*-

"""
MEMO

Send Data

send = [MoterFrontRight,MoterFrontLeft,MoterBackRight,MoterBackLeft,
        LED0,LED1,LED2,LED3,LED4,LED5,LED6,LED7,LED8]


                    Moter

        FrontLeft           FrontRight

        Back Left           Back Right


            LED
            
    LED0    LED1    LED2

    LED3    LED4    LED5

    LED6    LED7    LED8



"""
import os, sys, inspect,time
from time import sleep

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

"""""""""""""""
定数定義
PITCH_MAX:x軸方向の最大角度
PITCH_MIN:x軸方向の最小角度
ROLL_RIGHT:右に倒した時の最大角度(負の値）
ROLL_LEFT:左に倒した時の最小角度(正の値）

"""""""""""""""
PITCH_MAX=0.8
PITCH_MIN=-0.8
ROLL_RIGHT=-1.2
ROLL_LEFT=1.2

#LED Global
current=0
before =0
p=0
#pwm Global
pwm=[0 for i in range(14)]

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
        #print "Frame available"
        frame=controller.frame()
        hand = frame.hands.rightmost
        global pwm
        #Wait()
        pitch = hand.direction.pitch
        #hands 
        for hand in frame.hands:
            
            pitch = hand.direction.pitch
            roll = hand.palm_normal.roll
            #morter control
            #hand_name = "Left hand" if hand.is_left else "Right hand"
            pwm=MoterControl(pitch,roll,pwm)
        #fingers
        swipeck=0
        global current
        global before
        global p
        for finger in hand.fingers:
            pointable = frame.pointables.frontmost
            direction = pointable.direction
            id = pointable.id

            
            length = pointable.length
            width = pointable.width
            stabilizedPosition = pointable.stabilized_tip_position
            position = pointable.tip_position
            speed = pointable.tip_velocity
            touchDistance = pointable.touch_distance
            zone = pointable.touch_zone
            
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
        controller.config.set("Gesture.Swipe.MinLength", 100.0)
        controller.config.set("Gesture.Swipe.MinVelocity", 1000.0)
        controller.config.save()
        #gesture/swipe
        #https://developer.leapmotion.com/documentation/python/api/Leap.SwipeGesture.html
        for gesture in frame.gestures():
            if gesture.type is Leap.Gesture.TYPE_SWIPE:
                swipe = Leap.SwipeGesture(gesture)
                current = swipe.position
                velocity = swipe.speed
                swipeck=1
                swipper = swipe.pointable
        pwm=LED(swipeck,current,before,p,pwm)
        Send(pwm)


        

def Wait():
    #無限ループの表示感覚を遅くする
    for num, i in enumerate(range(100)):
            sys.stdout.flush()
            time.sleep(0.01)

#================================モーター制御====================================#
def MoterControl(pitch,roll,pwm):
    #print "hand:x:{}".format(pitch)
    speed=forward(pitch)
    #print "{}".format(roll)
    duty_right=duty(roll)
    #print "右側のデューティー比は{}%".format(duty_right)
    duty_left=100-duty_right
    speed_right = speed * duty_right *0.01
    speed_left  = speed * duty_left  *0.01
    #print "right:{0},left:{1}".format(speed_right,speed_left)
    #speed : front=back

    for i in range(5):
    	if i%2==1:
    		pwm[i]=speed_left
    	else:
    		pwm[i]=speed_right

    return pwm

"""
forward   : 前進スピード制御　
left 　   : 後進スピード制御
ConvertSP : 角度→スピード変換関数
        
"""
#====================================前進制御====================================#
def forward(pitch):
    #前進
    
    if pitch > PITCH_MAX :
        #print "STOP"
        speed = 0

    elif pitch > PITCH_MIN:
        speed=ConvertSP(pitch)
        #print "speed: {}".format(speed)
    else:
        #print "MAX"
        speed=100
    return speed
    #send('{"right":{0},"left":{1}}'.format(speed,speed))

#====================================後進制御====================================#
def back(pitch):
    
    if pitch > PITCH_MAX :
        #print "STOP"
        speed=-100

    elif pitch > PITCH_MIN:
        speed=ConvertSP(pitch)
        speed=-1*speed
        #print "speed: {}".format(speed)
    else:
        #print "MAX"
        speed=0

    return speed
    #send('{"right":{0},"left":{1}}'.format(speed,speed))

#==================================角度/速度変換==================================#
def ConvertSP(speed):
    speed=-62.5*(speed-PITCH_MAX)
    return speed

#==================================左右方向制御==================================#
#右モーター回転率を算出する関数回転率[duty]%
#左の回転率=100-右の回転率
def duty(roll):
    if roll > ROLL_LEFT:
        #print "これ以上左に倒しても意味ないよ"
        duty = 0
    elif roll > ROLL_RIGHT:
        #print "中間"
        duty = ConvertDuty(roll)
    else :
        #print "これ以上右に倒しても意味ないよ"
        duty = 100
    return duty
        
#===========================左右方向角度/デューティー比変換==========================#    
def ConvertDuty(roll):
    x = roll+ROLL_LEFT
    y = (100*x)/(ROLL_LEFT-ROLL_RIGHT)
    return y

#===========================LED制御==========================#
def LED(swipeck,current,before,p,pwm):
    if (swipeck is 1):              
        #print "swipe"
        current=1    
        sleep(0.2) #chattering eliminat
    else:
        current=0

    if current is 1 and before is 0:
        if p is 0:
            p=100
        elif p is 100:
            p=0
    pwm=Led_All(p,pwm)

    return pwm
#===========================LED　全点灯==========================#
def Led_All(p,pwm):
    for i in range(4,14):
    	pwm[i]=p
    return pwm
#===========================DataSend==========================#
def Send(pwm):
    print "pwm={}".format(pwm)
    #LED SEND BEGIN
    pwm_str=map(str,pwm)
    mes=','.join(pwm_str)
    #LED SEND END
def main():
    listener=SampleListener()
    controller=Leap.Controller()
    controller.add_listener(listener)
    controller.set_policy(Controller.POLICY_BACKGROUND_FRAMES)
    controller.set_policy(controller.POLICY_IMAGES)
    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
    

    #Controller.set_policy

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
