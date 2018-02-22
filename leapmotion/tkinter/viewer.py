import threading,time

"""
http://momijiame.tumblr.com/post/38149309923/python-%E3%81%AE-threadingthread-%E3%82%92%E8%A9%A6%E3%81%97%E3%81%A6%E3%81%BF%E3%82%8B


"""

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

v=viewer()
v.setDaemon(True)
v.start()


cnt=0
while True:
    led_status=[i*cnt for i in range(25)]
    cnt+=1
    if cnt>9:
        cnt=0
    print("main thread")
    time.sleep(0.01)





