import threading,time
import Tkinter
#when you want to update color of led ,you should change this list like main()
led_status=[i for i in range(25)]


#koki start
#B:button
#M:menu

#show menu
def menu():
    menu = Tkinter.Tk()
    menu.title(u"menu")
    menu.geometry("400x300")

    led =Tkinter.Button(menu,text=u'LED')
    led.bind("<Button-1>",ledM)
    led.place(x=150,y=60)


#show ledmenu
def ledM(event):
    menu=Tkinter.Tk()
    menu.title(u"led menu")
    menu.geometry("400x300")
    
    patternB=Tkinter.Button(menu,text=u'Set Pattern')
    patternB.bind("<Button-1>",patternM)
    patternB.place(x=150,y=60)

    gestureB=Tkinter.Button(menu,text=u'Set')
    gestureB.bind("<Button-1>",gestureM)
    gestureB.place(x=150,y=90)

    goB=Tkinter.Button(menu,text=u'GO!')
    #goB.bind("<Button-1>",)
    goB.place(x=150,y=120)  

def patternM(event):
    menu=Tkinter.Tk()
    menu.title(u"pattern menu")
    menu.geometry("400x300")

def gestureM(event):
    menu=Tkinter.Tk()
    menu.title(u"gesture menu")
    menu.geometry("400x300")


#koki end  

class viewer(threading.Thread):
#    import Tkinter
    def __init__(self):
        import Tkinter
        print("====== ",__name__," ====== ")
        print("====== init viewer thread ====== ")
        super(viewer,self).__init__()
        self.aaa=3
        self.w=50
        self.h=50
        self.root=Tkinter.Tk()
        self.root.title(u"LEDmap")
        self.root.geometry('250x250')
        self.c=Tkinter.Canvas(self.root,width=self.w*10,height=self.h*10)
        self.led_id=[]
        global led_id
        global led_Status
        self.init_led(self.h,self.w)
        menu()
 
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
        for i in range(1,4):
            for j in range(1,4):
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
            print("sub thread run()",id(led_status))
            for i in range(9):
                self.c.itemconfig(self.led_id[i],fill=self.color2hex([led_status[i]*10,0,0]))
                time.sleep(0.01)
            self.root.update()
        

def main():
        
    v=viewer()
    v.setDaemon(True)
    v.start()
    cnt=0
    global led_status
    while True:
        led_status=[i*cnt for i in range(25)]
        cnt+=1
        if cnt>9:
            cnt=0
        print("main thread")
        time.sleep(0.01)
if __name__  == '__main__':
    main()


