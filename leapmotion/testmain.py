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
        #print "Frame available"
        frame=controller.frame()
        hand = frame.hands.rightmost
        #Wait()

        

        #hands
            
        for hand in frame.hands:

            pitch = hand.direction.pitch
            yaw = hand.direction.yaw
            roll = hand.palm_normal.roll
            strength = hand.grab_strength

            hand_name = "Left hand" if hand.is_left else "Right hand"
            if hand_name == "Left hand" :
                speed=back(pitch)
            else:
                speed=forward(pitch)
            print "right:{0},left:{1}".format(speed,speed)
#            send('{"right":%d,"left":%d}'.format(speed,speed))
            send('{"right":'+str(speed)+',"left":'+str(speed)+'}')
            
def ConvertSP(speed):
        speed=-62.5*(speed-0.8)
        return speed
        

def Wait():
    #無限ループの表示感覚を遅くする
    for num, i in enumerate(range(100)):
            sys.stdout.flush()
            time.sleep(0.01)
            

"""
forward back

max: -0.8,Min:0.8

right : 前進　left :　後進

        
"""

def forward(pitch):
    #前進
    
    if pitch > 0.8 :
        print "STOP"
        speed = 0

    elif pitch > -0.8:
        speed=ConvertSP(pitch)
        print "speed: {}".format(speed)
    else:
        print "MAX"
        speed=100
    return speed
    #send('{"right":{0},"left":{1}}'.format(speed,speed))


def back(pitch):
    #後進
    if pitch > 0.8 :
        print "STOP"
        speed=-100

    elif pitch > -0.8:
        speed=ConvertSP(pitch)
        speed=-1*speed
        print "speed: {}".format(speed)
    else:
        print "MAX"
        speed=0

    return speed
    #send('{"right":{0},"left":{1}}'.format(speed,speed))


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

