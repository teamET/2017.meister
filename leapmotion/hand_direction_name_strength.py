import os, sys, inspect,time


src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, 'lib'))
sys.path.insert(0, lib_dir)

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

            #hand_direction 手の方向ベクトル
            hand_direction =hand.direction
            print "vector = {}".format(hand_direction)
            
            #grab_strength 拳の判定
            #1.0に近づくほど拳に近い
            strength = hand.grab_strength
            print "grab_strength = {}".format(strength)
            
            #右手と左手の判定
            hand_identifier = hand.id
            #左手の判定文,
            #left=>1 right=>0

            hand_name = "Left hand" if hand.is_left else "Right hand"
            if hand_name == "Left hand" :
                print "left"
            else:
                print "right"

        

def Wait():
    #無限ループの表示感覚を遅くする
    for num, i in enumerate(range(100)):
            sys.stdout.flush()
            time.sleep(0.01)
    
    
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

"""
左手パー
vector = (0.496395, 0.805313, -0.324135)
grab_strength = 0.0
left

右手グー
vector = (-0.598858, 0.033626, -0.800149)
grab_strength = 1.0
right

"""
