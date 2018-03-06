import threading,time
import Tkinter
#when you want to update color of led ,you should change this list like main()
led_status=[0 for i in range(9)]
LED_GO=0
ebhandle=[]
Mode=0
pname=[0 for i in range(9)]
gname=[1 for i in range(4)]
#koki start
#B:button
#M:menu

#show menu
def menu():
    menu = Tkinter.Tk()
    menu.title(u"menu")
    menu.geometry("200x200")

    led =Tkinter.Button(menu,text=u'LED')
    led.bind("<Button-1>",ledM)
    led.pack()
    #led.place(x=10,y=10)

#show ledmenu
def ledM(event):
    menu=Tkinter.Tk()
    menu.title(u"led menu")
    menu.geometry("200x200")
    
    patternB=Tkinter.Button(menu,text=u'Set Pattern')
    patternB.bind("<Button-1>",patternM)
    patternB.pack()

    gestureB=Tkinter.Button(menu,text=u'Set')
    gestureB.bind("<Button-1>",gestureM)
    gestureB.pack()
	
    goB=Tkinter.Button(menu,text=u'GO!')
    goB.bind("<Button-1>",go)
    '''lambda event,LED_GO=1:0'''
    goB.pack()  

def go():
	LED_GO=1

#pattern menu
def patternM(event):
    menu=Tkinter.Tk()
    menu.title(u"pattern menu")
    menu.geometry("200x200")
	
    for n in range (9):
    	pname[n]=Tkinter.Entry(menu,width=3)
    	pname[n].insert(Tkinter.END,"0")
    	pname[n].place(x=10+(n%3)*50, y=50+(n/3)*50)

    check=Tkinter.Button(menu,text=u'OK')
    check.bind("<Button-1>",pattern_check)
    check.place(x=150,y=150)

def pattern_check(event):
	for n in range (9):
		led_status[n] = int(pname[n].get())

	print("led_status()",led_status)

#gesture menu
def gestureM(event):
    menu=Tkinter.Tk()
    menu.title(u"gesture menu")
    menu.geometry("200x200")
    bl = Tkinter.BooleanVar()
    gname[1]=Tkinter.Checkbutton(text=u"lightup all")
    gname[2]=Tkinter.Checkbutton(text=u"height of hand")
    gname[3]=Tkinter.Checkbutton(text=u"Swipe")
    gname[4]=Tkinter.Checkbutton(text=u"goopeer")
    for n in range(1,4):
    	gname[n].pack()

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
        self.c=Tkinter.Canvas(self.root,bg='black',width=self.w*10,height=self.h*10)
        self.led_id=[]
        global led_id
        global led_status
        global LED_GO
        global ebhandle
        global Mode
        global pname
        global gname
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
        for j in range(1,4):
            for i in range(1,4):
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
            #print("sub thread run()",id(led_status))
            for i in range(9):
                self.c.itemconfig(self.led_id[i],fill=self.color2hex([led_status[i],0,0]))
                #time.sleep(0.01)
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


