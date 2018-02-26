import threading,os, sys, inspect,time
from time import sleep

import socket,json
#  UDP communication

UDP_IP="127.0.1.1"
UDP_IP="192.168.137.132" #raspberry pi ip address
UDP_PORT=5005

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, 'lib'))
sys.path.insert(0, lib_dir)
#import Leap

#when you want to update color of led ,you should change this list like main()
led_status=[i for i in range(25)]

class viewer(threading.Thread):
    def __init__(self):
        import Tkinter
        print("====== init viewer thread ====== ")
        super(viewer,self).__init__()
        self.w=50
        self.h=50
        self.root=Tkinter.Tk()
        self.root.geometry('500x500')
        self.c=Tkinter.Canvas(self.root,width=self.w*10,height=self.h*10)
        self.led_id=[]
        global led_id
        global led_Status
        self.init_led(self.h,self.w)
 
    def color2hex(self,rgb):
        '''
        get list of color value ,then return string of it
        color2hex([0xf,0xff,0]) -> '#0fff00'
        '''
        ih=list('0123456789abcdef')
        color='#'
        for c in rgb:
            if c/256 :c=c/256 
            if c<16:
                color+='0'+ih[c]
            else:
                color+=ih[c/16]+ih[c%16]
        return color

    #draw circle
    def init_led(self,h,w):
        for i in range(1,6):
            for j in range(1,6):
                self.led_id.append(self.c.create_oval(w*i  ,h*j,w*(i+1), h*(j+1),
                                        fill=self.color2hex([i*16,i*16,i*16])))
        self.c.pack()
        print("finish init led")

    #draw line
    def init_line():
        for i in range(1,7):
            c.create_line(w*i,h,  w*i,300)
            c.create_line(h  ,h*i,300, h*i)

    #change color of circle by id based on led_status frequentry
    def run(self):
        while True:
            #root.mainloop() is a substitute for update_idletasks() and update()
            self.root.update_idletasks()
            print("sub thread run()")
            for i in range(25):
                self.c.itemconfig(self.led_id[i],fill=self.color2hex([led_status[i]*10,0,0]))
                time.sleep(0.01)
            self.root.update()

#class SampleListener(Leap.Listener):
class SimpleListener():
    def __init__(self):
#        super(SimpleListener).__init__()
        global led_status
        self.cnt=0

    def on_connect(self,controller):
        print "connected"

    def mainloop(self):
        print("main loop")
        if self.cnt>9: self.cnt=0
        led_status=[i*self.cnt for i in range(25)]
        self.send_led(led_status)

    def on_frame(self,controller):
        print("on_frame")
        print(controller.frame())
        if self.cnt>9: self.cnt=0
        led_status=[i*self.cnt for i in range(25)]
        self.send_led(led_status)

    def send(self,message):
        print("message",message)
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock.sendto(message.encode('utf-8'),(UDP_IP,UDP_PORT))
        
    def send_led(self,pwm):
        print "pwm={}".format(pwm)
        pwm_str=map(str,pwm)
        mes=','.join(pwm_str)
        self.send(mes)

def buildThread():
    v=viewer()
    v.setDaemon(True)
    v.start()
    
def main():
    buildThread()
    
    listener=SimpleListener()
    while True:
        listener.mainloop()
        
if __name__  == '__main__':
    main()

