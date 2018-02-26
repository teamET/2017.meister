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

FrameCount=0
FrameCheck=0
SwipeCount=0
StrC=0
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
        global FrameCount
        global FrameCheck
        global SwipeCount
        frame=controller.frame()
        hand = frame.hands.rightmost
        if(FrameCheck is 1 ):
            FrameCount+=1
        if(FrameCount > 50):
            FrameCount=0
            FrameCheck=0
        #print "t={}".format(FrameCount)
        #finger
        swipeck=0
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
        
        if (swipeck is 1):              
            print "swipe"
            swipeCheck=1
            sleep(1) #chattering eliminat

        if(swipeCheck is 1):
            Swipe()     

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

