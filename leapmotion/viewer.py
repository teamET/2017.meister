#-*- Coding utf-8 -*-
import threading,time
import Tkinter
#when you want to update color of led ,you should change this list like main()
led_status=[0 for i in range(9)]
"""
shared[0]=LED_GO
shared[1]=Mode
Cycle=share[2]
brightness=shared[3]
"""
shared=[0 for i in range(4)]
tail=0
#koki start
#B:button
#M:menu

#show menu
def menu():
    menu = Tkinter.Tk()
    menu.title(u"menu")
    menu.geometry("200x50")

    led =Tkinter.Button(menu,text=u'LED')
    led.bind("<Button-1>",ledM)
    led.pack()

    motor=Tkinter.Button(menu,text=u'Motor')
    motor.bind("<Button-1>",motorM)
    motor.pack()

def motorM(event):
    def go_check(event):
        shared[1]=100
        print("Mode=",shared[1])
    
    global shared
    menu=Tkinter.Tk()
    menu.title(u"Motor menu")
    menu.geometry("200x50")

    goB=Tkinter.Button(menu,text=u'GO!')
    goB.bind("<Button-1>",go_check)
    goB.pack()

#show ledmenu
def ledM(event):

    menu=Tkinter.Tk()
    menu.title(u"led menu")
    menu.geometry("220x100")
    
    brightnessB=Tkinter.Button(menu,text=u'Set Brightness')
    brightnessB.bind("<Button-1>",brightnessM)
    brightnessB.pack()

    gestureB=Tkinter.Button(menu,text=u'Set Gesture')
    gestureB.bind("<Button-1>",gestureM)
    gestureB.pack()

    behaviorB=Tkinter.Button(menu,text=u'Set Behavior')
    behaviorB.bind("<Button-1>",behaviorM)
    behaviorB.pack()
    
#brightness menu
def brightnessM(event):
    def brightness_check(event):
        for n in range (9):
            led_status[n] = int(pname[n].get())
        print("led_status()",led_status)

        
    menu=Tkinter.Tk()
    menu.title(u"Brightness menu")
    menu.geometry("200x200")
    
    pname=[0 for i in range(9)]
    for n in range (9):
        pname[n]=Tkinter.Entry(menu,width=3)
        pname[n].insert(Tkinter.END,"0")
        pname[n].place(x=10+(n%3)*50, y=50+(n/3)*50)

    check=Tkinter.Button(menu,text=u'OK')
    check.bind("<Button-1>",brightness_check)
    check.place(x=150,y=150)

    label=Tkinter.Label(menu,text=u'Enter number between 0 to 254')
    label.place(x=10,y=5)



#gesture menu
def gestureM(event):
    global shared
    def gesture_check(event):
        shared[1]=int(eg.get())
        print("Mode=",shared[1])


    menu=Tkinter.Tk()
    menu.title(u"gesture menu")
    menu.geometry("200x130")
    
    eg=Tkinter.Entry(menu,width=1)
    eg.insert(Tkinter.END,"0")
    eg.pack()

    gn1=Tkinter.Label(menu,text=u'1:lightup all                       ')
    gn1.pack()

    gn2=Tkinter.Label(menu,text=u'2:move hand veritical       ')
    gn2.pack()

    gn3=Tkinter.Label(menu,text=u'3:move hand horizontal   ')
    gn3.pack()

    gn4=Tkinter.Label(menu,text=u'4:clasp and unclasp hand')
    gn4.pack()

    check=Tkinter.Button(menu,text=u'OK')
    check.bind("<Button-1>",gesture_check)
    check.pack()

#behavior menu
def behaviorM(event):
    global shared
    def behavior_check(event):
        def cycle_check(event):
            if ebnum==3:
                shared[2]=int(ce1.get())
                shared[3]=int(brn1.get())
                print("Cycle=",shared[2]," brightness=",shared[3])
            elif ebnum==4:
                shared[2]=int(ce2.get())
                shared[3]=int(brn2.get())
                print("Cycle=",shared[2]," Cycle Time=",shared[3])
            elif ebnum==5:
                shared[3]=int(brn3.get())
                print("Brightness=",shared[3])
        #cycle_check end

        ebnum=int(eb.get())+2
        print("ebnum=",ebnum)
        if ebnum==3:
            shared[0]=ebnum
            
            menu1=Tkinter.Tk()
            menu1.title(u"Set1")
            menu1.geometry("220x100")

            ce1=Tkinter.Entry(menu1,width=4)
            ce1.insert(Tkinter.END,"0")
            ce1.pack()      

            brn1=Tkinter.Entry(menu1,width=3)
            brn1.insert(Tkinter.END,"0")
            brn1.pack()

            cet1=Tkinter.Label(menu1,text=u'Cycle(msec)')
            cet1.place(x=0,y=0)

            brnt1=Tkinter.Label(menu1,text=u'Brightness(0-254)')
            brnt1.place(x=0,y=20)       

            check1=Tkinter.Button(menu1,text=u'OK')
            check1.bind("<Button-1>",cycle_check)
            check1.pack()

        elif ebnum==4:
            shared[0]=ebnum

            menu2=Tkinter.Tk()
            menu2.title(u"Set2")
            menu2.geometry("220x100")

            ce2=Tkinter.Entry(menu2,width=4)
            ce2.insert(Tkinter.END,"0")
            ce2.pack()      

            brn2=Tkinter.Entry(menu2,width=4)
            brn2.insert(Tkinter.END,"0")
            brn2.pack()

            cet2=Tkinter.Label(menu2,text=u'Cycle(msec)')
            cet2.place(x=0,y=0)

            brnt2=Tkinter.Label(menu2,text=u'Cycle time(sec)')
            brnt2.place(x=0,y=20)       

            check2=Tkinter.Button(menu2,text=u'OK')
            check2.bind("<Button-1>",cycle_check)
            check2.pack()
            
        elif ebnum==5:
            shared[1]=ebnum

            menu3=Tkinter.Tk()
            menu3.title(u"Set3")
            menu3.geometry("220x100")

            brn3=Tkinter.Entry(menu3,width=3)
            brn3.insert(Tkinter.END,"0")
            brn3.pack()      

            brnt3=Tkinter.Label(menu3,text=u'Brightness(0-254)')
            brnt3.place(x=0,y=0)     

            check3=Tkinter.Button(menu3,text=u'OK')
            check3.bind("<Button-1>",cycle_check)
            check3.pack()
        #if end
        print("Mode=",shared[1])
        print("LED_GO=",shared[0])           
    #behavior check end
                    
    menu=Tkinter.Tk()
    menu.title(u"behavior menu")
    menu.geometry("200x120")

    eb=Tkinter.Entry(menu,width=1)
    eb.insert(Tkinter.END,"0")
    eb.pack()

    """bn1=Tkinter.Label(menu,text=u'1:rotate right   ')
    bn1.pack()

    bn2=Tkinter.Label(menu,text=u'2.rotate left')
    bn2.pack()"""

    bn3=Tkinter.Label(menu,text=u'1.Flashing ver.1')
    bn3.pack()

    bn4=Tkinter.Label(menu,text=u'2.Flashing ver.2')
    bn4.pack()

    bn5=Tkinter.Label(menu,text=u'3.rotate')
    bn5.pack()

    check=Tkinter.Button(menu,text=u'OK')
    check.bind("<Button-1>",behavior_check)
    check.pack()
#behaviorM end

def cycleM(event):
    pass

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
        global shared
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
        """led_status=[i*cnt for i in range(9)]
        cnt+=1
        if cnt>9:
            cnt=0
        #print("main thread")"""
        time.sleep(0.01)
if __name__  == '__main__':
    main()


