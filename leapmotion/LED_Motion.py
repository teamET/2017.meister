# -*- coding: cp932 -*-
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

def Led_Flash(pwm,n,m):
    #LEDが現在の状態を保ちながら周期nミリ秒でm秒点滅する.
    pwm_current=pwm
    n=n*0.001
    count=0
    print("h")
    while(1):
        print("A")
        pwm=[0 for i in range(9)]
        sleep(n)
        for i in range(9):
            pwm[i]=pwm_current[i]
        if count==30:
            break
        count+=1


            
def main():
    
    global led_status
    v=viewer.viewer()
    v.setDaemon(True)
    v.start()
    led_status=[150,0,0,150,0,0,150,0,0]
    sleep(3)
    Led_Flash(led_status,500,6)

    v=viewer.viewer()
    v.setDaemon(True)
    v.start()

    """
    print "Press Enter to Quit"
    try:
        sys.stdin.readline()
    except KeyboardInterpt:
        pass
    finally:
        controller.remove_listener(listener)
    """
if __name__=='__main__':
    main()
