import Tkinter

led_id=[]
led_status=[i for i in range(25)]

class viewer:
    def __init__(self):
        print("init")
        self.w=50
        self.h=50
        self.root=Tkinter.Tk()
        self.root.geometry('500x500')
        self.c=Tkinter.Canvas(self.root,width=self.w*10,height=self.h*10)
        global led_id
        global led_Status
        self.init_led(self.h,self.w)
        self.update_led()
        self.root.mainloop()
        
    def color2hex(self,rgb):
        ih=list('0123456789abcdef')
        #print(ih)
        color='#'
        for c in rgb:
            if c<16:
                color+='0'+ih[c]
            else:
                color+=ih[c/16]+ih[c%16]
            print('c',c,'color',color)
        print(color)
        return color

    #draw circle
    def init_led(self,h,w):
        for i in range(1,6):
            for j in range(1,6):
                led_id.append(self.c.create_oval(w*i  ,h*j,w*(i+1), h*(j+1),
                                        fill=self.color2hex([i*16,i*16,i*16])))
        self.c.pack()

    #change color of circle by id based on led_status frequentry
    def update_led(self):
        print("update_led")
        for i in range(25):
            self.c.itemconfig(led_id[i],fill=self.color2hex([led_status[i]*10,0,0]))
        self.root.after(500,self.update_led)
'''
#draw line
for i in range(1,7):
    c.create_line(w*i,h,  w*i,300)
    c.create_line(h  ,h*i,300, h*i)
    '''

#change specific colot of circle by id
#c.itemconfig(led_id[0],fill=color2hex([0xff,0xff,0xff]))

v=viewer()
