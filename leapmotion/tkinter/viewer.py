import Tkinter

w=h=50
root=Tkinter.Tk()
root.geometry('500x500')

def color2hex(rgb):
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

led_id=[]
led_status=[i for i in range(25)]
c=Tkinter.Canvas(root,width=w*10,height=h*10)
'''
#draw line
for i in range(1,7):
    c.create_line(w*i,h,  w*i,300)
    c.create_line(h  ,h*i,300, h*i)
    '''

#draw circle
for i in range(1,6):
    for j in range(1,6):
        led_id.append(c.create_oval(w*i  ,h*j,w*(i+1), h*(j+1),
                                fill=color2hex([i*16,i*16,i*16])))

#change color of circle by id based on led_status
def update_led():
    for i in range(25):
        c.itemconfig(led_id[i],fill=color2hex([led_status[i]*10,0,0]))
    root.after(500,update_led)

#change specific colot of circle by id
#c.itemconfig(led_id[0],fill=color2hex([0xff,0xff,0xff]))



c.pack()

update_led()
root.mainloop()


