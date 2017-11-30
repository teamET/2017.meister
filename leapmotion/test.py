import os, sys, inspect
import requests
ip='http://192.168.43.12:5000'

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, 'lib'))
sys.path.insert(0, lib_dir)
import Leap

def send(message):
    requests.get(ip+'/api/v1/pallot/'+message)
    

class SampleListener(Leap.Listener):
    def on_connect(self,controller):
        print "connected"
    def on_frame(self,controller):
        print "Frame available"
        frame=controller.frame()
        state= "Frame id: %d ,ts : %d ,hands :%d ,fingers : %d"%(
            frame.id,frame.timestamp,len(frame.hands),len(frame.fingers))
        print(state)
        send(state)

def main():
    listener=SampleListener()
    controller=Leap.Controller()
    controller.add_listener(listener)
    controller.set_policy(Controller.POLICY_BACKGROUND_FRAMES)
    controller.set_policy(controller.POLICY_IMAGES)
    #controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
    
    #Controller.set_policy

    
    print "Press Enter to Quit"
    try:
        sys.stdin.readline()
    except KeyboardInterpt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__=='__main__':
    main()
            

