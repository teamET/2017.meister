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
        print ""
        #print "Frame available"
        frame=controller.frame()
        hand = frame.hands.rightmost
        Wait()
        

        #hands
            
        for hand in frame.hands:
            hand_x_basis = hand.basis.x_basis
            hand_y_basis = hand.basis.y_basis
            hand_z_basis = hand.basis.z_basis
            hand_origin = hand.palm_position
            
            hand_transform = Leap.Matrix(hand_x_basis, hand_y_basis, hand_z_basis, hand_origin)
            hand_transform = hand_transform.rigid_inverse()
            
            Cordinate_Print(hand_x_basis,hand_y_basis,hand_z_basis,hand_origin)
            
            pitch = hand.direction.pitch
            yaw = hand.direction.yaw
            roll = hand.palm_normal.roll
            
            Angle_Print(pitch,yaw,roll)
            
        for finger in hand.fingers:
            transformed_position = hand_transform.transform_point(finger.tip_position)
            transformed_direction = hand_transform.transform_direction(finger.direction)
            # Do something with the transformed fingers
            
        position = hand.palm_position
        velocity = hand.palm_velocity
        direction = hand.direction

        #fingers
        for hand in frame.hands:
            pointable = frame.pointables.frontmost
            direction = pointable.direction
            length = pointable.length
            width = pointable.width
            stabilizedPosition = pointable.stabilized_tip_position
            position = pointable.tip_position
            speed = pointable.tip_velocity
            touchDistance = pointable.touch_distance
            zone = pointable.touch_zone

            Finger_Print(direction,width,length,stabilizedPosition,speed)
        

        

def Wait():
    #無限ループの表示感覚を遅くする
    for num, i in enumerate(range(100)):
            sys.stdout.flush()
            time.sleep(0.01)
    

def Cordinate_Print(x,y,z,p):
    #Leapの視野内の相対位置座標(x,y,z)
    #palm:手の中心

    print "x                  = {}".format(x)
    print "y                  = {}".format(y)
    print "z                  = {}".format(z)
    print "palm               = {}".format(p)


def Angle_Print(pitch,yaw,rool):
    """
    pitch : x軸回りの角度
    yaw   : y軸回りの角度
    rool  : z軸回りの角度
    
    """
    print "pitch              = {}".format(pitch)
    print "yaw                = {}".format(yaw)
    print "rool               = {}".format(rool)

def Finger_Print(d,w,l,sp,speed):
    """
    Direction          : 現在のポインティング方向ベクトル
    width              : 平均幅
    Length             : 指の見かけの長さ
    StabilizedPosition : 速度および過去の位置を使用してフィルタリングされ安定化された位置
    Speed              : 瞬時先端速度（mm / s）
    
    """
    print "Direction          : {}".format(d)
    print "Width              : {}" .format(w)
    print "Length             : {}" .format(l)
    print "StabilizedPosition : {}".format(sp)
    print "Speed              : {}".format(speed)
    
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
x                  = (-0.967808, -0.127089, -0.217246)
y                  = (-0.186013, 0.942624, 0.277235)
z                  = (-0.169548, -0.308721, 0.935919)
palm               = (-15.6249, 112.948, 70.93)
pitch              = 0.318620473146
yaw                = 0.179212942719
rool               = 0.194832608104
Direction          : (0.103924, -0.0694023, -0.992161)
Width              : 18.0547561646
Length             : 63.6822738647
StabilizedPosition : (1.05555, 117.219, -37.2291)
Speed              : (-4.50292, 3.27976, 2.00732)
"""
