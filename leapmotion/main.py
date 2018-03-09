# -*- coding : utf-8 -*-

"""
GUI_LeapMotion Specification 3/6/2018 S.Hirose
1.Raspberry-pi-Send-Data List: send = [MotorFrontRight,MotorFrontLeft,MotorBackRight,MotorBackLeft, LED0,LED1,LED2,LED3,LED4,LED5,LED6,LED7,LED8]
                    Motor
        FrontLeft           FrontRight
        Back Left           Back Right
                    LED
                    
            LED0    LED1    LED2
            LED3    LED4    LED5
            LED6    LED7    LED8
2.Variables
led_status : LED�̃f�[�^�i���ݏ�ԁjList[ [now] for i in range(9)]
             user�����߂�LED_pattern���i�[����
             0 1 2
             3 4 5
             6 7 8
Mode	   :�@Mode�̔ԍ��ɂ���ċ@�\���ω�����D
 Mode�͎��LeapMotion�ł̋@�\�̐؂�ւ��ɗ��p����
Mode : menu �̃C���[�W
    Mode == 0~99 �F�@LED
    Mode==0
        LED���[�h�@�iLeapMotion����LED���[�h�ɐ؂�ւ��j
    Mode==1
        �_���p�^�[�����ς���Ă��C�S���_��������Ԃ�ۂ�
    Mode==2
        ��̍����ɂ����LED�̓_����Ԃ��ω�����
    Mode==3
        Swipe�ɂ����LED�̓_����Ԃ��ω�����
    Mode==4
        ��̂��[�ρ[�ɂ����LED�̓_����Ԃ��ω�����
    Mode==5
        :
        :
        �F
    �@�\��ǉ�������Mode==5~99��LED�̐���Ɋւ��铮�삪�ς��
--------------------------------------------------------------
    Mode==100
        ���[�^�[�쓮�iGO!)�@�F�@��̊p�x�ɑ΂��ă��[�o�[�������ς��
    Mode==101
        ���[�^�[�쓮�iGO!)�@�F�@��̃x�N�g���ɑ΂��ă��[�o�[�������ς��
    �����Mode==100,101�Ɋ܂܂��Ǝv��
        :
        :
    �@�\��ǉ�������Mode==100~199�Ƀ��[�^�[�̐���Ɋւ��铮�삪�ς��
-------------------------------------------------------------
    Mode==200
        �B���R�}���h01 : ���y�i�H)�@
        :
        :
    �@�\��ǉ�������Mode==200~299�ɉB���R�}���h�Ɋւ��铮�������
status     : ���ׂẴf�[�^(���ݏ��)List[[now] for i in range(14)]
    �����Send����(Send Data�͏���Q��)
LED_GO	   : LED�̓_�����@��ω�������ϐ�
    LED_GO==0
        ���ʂɑS���_���iMode==1�ƈႤ�̂́C�_���p�^�[�����ς��΁C�_����Ԃ��ω����鏊�j
    LED_GO==1
        �E��]
    LED_GO==2
        ����]
    LED_GO==3
        �_��
        :
        :
        :
    �@�\��ǉ�������LED_GO�̒l�𑝂₷
Cycle   : �_�ł���щ�]�����i1��]�ɂ����鎞��) 	** �P�ʂ̓~���b
Cycle_t : �_�ł���щ�]�𑱂��鎞�ԁ@			** �P�ʂ͕b
tail    : LED����]�_��������Ƃ��̔��̌��̋����i�����͂��邩�킩��Ȃ��j
(��O�̖��邳�ɑ΂���[tail]%�̗\��j
"""

import os, sys, inspect,time
from time import sleep

import viewer
from viewer import led_status
from viewer import shared

LED_GO  = int(shared[0])
Mode    = int(shared[1])
Cycle   = int(shared[2])
Cycle_t = int(shared[3]) #changed variable name

print(id(LED_GO))
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'lib/x64' if sys.maxsize > 2**32 else 'lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
lib_dir = os.path.abspath(os.path.join(src_dir, 'lib'))
sys.path.insert(0, lib_dir)


import socket,json
#  UDP communication
#raspberry pi ip address
UDP_IP="192.168.0.100"
UDP_PORT=5005

"""""""""""""""
�萔��` Motor
PITCH_MAX:x�������̍ő�p�x
PITCH_MIN:x�������̍ŏ��p�x
ROLL_RIGHT:�E�ɓ|�������̍ő�p�x(���̒l�j
ROLL_LEFT:���ɓ|�������̍ŏ��p�x(���̒l�j
"""""""""""""""
PITCH_MAX=0.8
PITCH_MIN=-0.8
ROLL_RIGHT=-1.2
ROLL_LEFT=1.2

"""""""""""""""
�萔��` LED
Y_MAX:�ő�̍���
Y_MIN:�ŏ��̍���
LED�̑��M�f���[�e�B�[��̍ő�F254
LED�̑��M�f���[�e�B�[��̍ŏ��F0
('message', '0,0,0,254,254,254,254,254,254,254,254,254,0')
"""""""""""""""
Y_MAX=430
Y_MIN=40

#test
"""
Mode=0
LED_GO=0
Cycle=0
Cycle_t=0
"""

#LED Global
current=0
before =0
p=0
#pwm Global
pwm=[0 for i in range(13)]

status=[i for i in range(13)]

tail=0

#LED�̖��邳�̍ő�l
LED_B_MAX=254

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True
def send(message):
    print("message",message)
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(message.encode('utf-8'),(UDP_IP,UDP_PORT))
    sleep(0.01)

import Leap
class SampleListener(Leap.Listener):
    def on_connect(self,controller):
        print "connected"
    def on_frame(self,controller):
        frame=controller.frame()
        hand = frame.hands.rightmost
        finger=frame.finger
        
        #tkinter Global
        global led_status
        global shared
        #global Mode
        LED_GO  = int(shared[0])
        Mode    = int(shared[1])
        Cycle   = int(shared[2])
        Cycle_t = int(shared[3])
        print ('############main Mode222222222',Mode,id(Mode))
        global status
        """
        global Cycle
        global Cycle_t
        global tail
        """
        #leap Global
        global pwm
        
        status= init_status(status)
        pwm   = init_pwm(pwm)
        #menu
        """
        frame,hand
        """
        

        #LED
        if   Mode == 1:
            #�S���_����ۂ� 
            pwm=Led_All(LED_B_MAX)
            Led_Menu(LED_GO,frame,hand)
        elif Mode == 2:
            Led_Menu(LED_GO,frame,hand)
        elif Mode == 5:
            for hand in frame.hands:
                strength = hand.grab_strength
                hand_identifier = hand.id
                hand_name = "Left hand" if hand.is_left else "Right hand"
                if hand_name=="Right hand" and strength == 1.0:
                    print"Right hand"
                    Led_Spin_Right(pwm,Cycle,Cycle_t,tail)
                if hand_name=="Left hand" and strength == 1.0:
                    print "Left Hand"
                    Led_Spin_Left(pwm,Cycle,Cycle_t,tail)

        elif Mode == 100:
            for hand in frame.hands:
                pitch = hand.direction.pitch
                roll = hand.palm_normal.roll
                #morter control
                #hand_name = "Left hand" if hand.is_left else "Right hand"
                MotorControl_2(pitch,roll)
        """   
        elif Mode == 101:
        
        #Secret Command
    	elif Mode == 200:
    	"""
def init_status(status):
    status=[0 for i in range(13)]
    return status

def init_pwm(pwm):
    pwm=[p for i in range(9)]
    return pwm

def Led_Menu(LED_GO,frame,hand):
    global pwm
    global shared
    #global Mode
    LED_GO  = int(shared[0])
    Mode    = int(shared[1])
    Cycle   = int(shared[2])
    Cycle_t = int(shared[3])
    global led_status
    if Mode == 1:
        if LED_GO == 3:
            print"hello world"
            Led_Flash(pwm,Cycle,Cycle_t)
        elif LED_GO == 4:
            Led_Flash_update(pwm,Cycle,Cycle_t)

    if Mode == 2:
        if LED_GO == 3:
            for hand in frame.hands:
                pointable = frame.pointables.frontmost
                position = pointable.tip_position
                y=position.y #variable=vector.(x,y,z)
                #print(y)
                #position.y.range = 40 to 430
                #LED: 0 to 254 
                p=Led_Brightness(y)
                pwm=init_Led_status(p)
                #print(p)
                Led_Flash(pwm,Cycle,Cycle_t)
        elif LED_GO == 4:
            for hand in frame.hands:
                pointable = frame.pointables.frontmost
                position = pointable.tip_position
                y=position.y #variable=vector.(x,y,z)
                #print(y)
                #position.y.range = 40 to 430
                #LED: 0 to 254 
                p=Led_Brightness(y)
                pwm=init_Led_status(p)
                print(led_status)
                print(pwm)
                Led_Flash_update(pwm,Cycle,Cycle_t)

def Led_All(p):
    pwm=[p for i in range(9)]
    return pwm

def Led_Brightness(y):
    p=(254.0/(Y_MAX - Y_MIN))*(y-Y_MIN)
    #��ʎ�
    #a-b �͈̔͂̎� x=254/(b-a)*(y-a))
    if p>254:
        p=254
    elif p<0:
        p=0
    return p

def Led_Spin_Right(pwm,n,p,tail):
    #N�~���b��1��]����(���v���)
    #p�͌��̖��邳
    #tail�͔��̒���
    #atode
    n*=0.000125
    round_order=[1,2,5,8,7,6,3,0]
    pwm=init_pwm(pwm)
    for i in range(8):
        pwm=init_pwm(pwm)
        pwm[round_order[i]]=p
        L_status_update(pwm)
        sleep(n)

def Led_Spin_Left(pwm,n,p,tail):
    #N�~���b��1��]����(�����v���)
    #p�͌��̖��邳
    #tail�͔��̒���
    #atode
    n*=0.000125
    round_order=[1,0,3,6,7,8,5,2]
    pwm=init_pwm(pwm)
    for i in range(8):
        pwm=init_pwm(pwm)
        pwm[round_order[i]]=p
        L_status_update(pwm)
        sleep(n)

def init_Led_status(p):
    global led_status
    global pwm
    for i in range(9):
        if led_status[i] != 0 : pwm[i]=int(p)
    return pwm

def Led_Flash(pwm,n,m):
    #LED��main�Ŏ擾������Ԃ�ۂ��Ȃ������n�~���b��m�b�_�ł���.
    #global led_status
    pwm_current=pwm
    print(pwm_current)
    n=n*0.0005
    m/=2
    count=0
    while(True):
        pwm=[0 for i in range(9)]
        L_status_update(pwm)
        
        sleep(n)
        pwm=[pwm_current[i] for i in range(9)]
        L_status_update(pwm)
        if count==(m/n):
            break
        count+=1
        sleep(n)
    pwm=pwm_current
    L_status_update(pwm)

def Led_Flash_update(pwm,n,m):
    #LED������(�擾������ԁj�̏�Ԃ�"""�X�V�������Ȃ���"""����n�~���b��m�b�_�ł���.
    pwm_current=pwm
    print(pwm_current)
    n=n*0.0005
    global count
    pwm=[0 for i in range(9)]
    L_status_update(pwm)
    sleep(n)
    pwm=[pwm_current[i] for i in range(9)]
    L_status_update(pwm)
    sleep(n) 

def L_status_update(pwm):
    for i in range(9):
        led_status[i]=pwm[i]
    print(led_status)
    status=Led_Status_Convert(pwm)
    print "status={}".format(status)
    Led_Send(status)

def Led_Status_Convert(led_status):
    global status
    print(led_status)
    for i in range(9):
        status[i+4] = led_status[i]
    return status

def Led_Send(pwm):
    #print "pwm={}".format(pwm)
    #LED SEND BEGIN
    pwm_str=map(str,pwm)
    mes=','.join(pwm_str)
    send(mes)
    #LED SEND END

def MoterControl(pitch,roll):
    #print "hand:x:{}".format(pitch)
    speed=forward(pitch)
    #print "{}".format(roll)
    duty_right=duty(roll)
    #print "�E���̃f���[�e�B�[���{}%".format(duty_right)
    duty_left=100-duty_right
    speed_right = ConvertSP2(speed * duty_right *0.01)
    speed_left  = ConvertSP2(speed * duty_left  *0.01)
    #print "right:{0},left:{1}".format(speed_right,speed_left)
    status=Motor_Status_Convert(speed_right,speed_left)
    Motor_Send(status)
    """
    forward   : �O�i�X�s�[�h����@
    left �@   : ��i�X�s�[�h����
    ConvertSP : �p�x���X�s�[�h�ϊ��֐�
    *ConvertSP:
    """

def MotorControl_2(pitch,roll):
    speed=forward_back(pitch)
    duty_right=duty(roll)
    duty_left=100-duty_right
    speed_right = ConvertSP2(speed * duty_right *0.01)
    speed_left  = ConvertSP2(speed * duty_left  *0.01)

    status=Motor_Status_Convert(speed_right,speed_left)
    Motor_Send(status)

def forward(pitch):
    #�O�i
    
    if pitch > PITCH_MAX :
        #print "STOP"
        speed = 0

    elif pitch > PITCH_MIN:
        speed=ConvertSP(pitch)
        #print "speed: {}".format(speed)
    else:
        #print "MAX"
        speed=100
    return speed
    #send('{"right":{0},"left":{1}}'.format(speed,speed))

def back(pitch):
    
    if pitch > PITCH_MAX :
        #print "STOP"
        speed=-100

    elif pitch > PITCH_MIN:
        speed=ConvertSP(pitch)
        speed=-1*speed
        #print "speed: {}".format(speed)
    else:
        #print "MAX"
        speed=0

    return speed
    #send('{"right":{0},"left":{1}}'.format(speed,speed))

def forward_back(pitch):
    #print "pitch={}".format(pitch)
    if pitch > PITCH_MAX :
        speed = -254

    elif pitch > PITCH_MIN:
        speed=ConvertSP_fb(pitch)
        #print "speed: {}".format(speed)
    else:
        #print "MAX"
        speed= 254
    return speed

def ConvertSP(speed):
    speed=-62.5*(speed-PITCH_MAX)
    return speed

def ConvertSP2(speed):
    #speed range : (0 to 50)
    #254/50=5.08
    speed=5.08*speed
    if speed > 254:
        speed=254
    
    if speed < -254:
        speed=-254

    if speed < 50 and speed >-70 :
        speed = 0
    
    return speed

def ConvertSP_fb(speed):
    speed= -254 / PITCH_MAX * speed
    return speed

def duty(roll):
    #�E���[�^�[��]�����Z�o����֐���]��[duty]%
    #���̉�]��=100-�E�̉�]��
    if roll > ROLL_LEFT:
        #print "����ȏ㍶�ɓ|���Ă��Ӗ��Ȃ���"
        duty = 0
    elif roll > ROLL_RIGHT:
        #print "����"
        duty = ConvertDuty(roll)
    else :
        #print "����ȏ�E�ɓ|���Ă��Ӗ��Ȃ���"
        duty = 100
    return duty
  
def ConvertDuty(roll):
    x = roll+ROLL_LEFT
    y = (100*x)/(ROLL_LEFT-ROLL_RIGHT)
    return y
 
def Motor_Status_Convert(right,left):
    for i in range(4):
        if i%2==0 : status[i] = int(right)
        if i%2==1 : status[i] = int(left)
    return status

def Motor_Send(pwm):
    #print "pwm={}".format(pwm)
    #LED SEND BEGIN
    pwm_str=map(str,pwm)
    mes=','.join(pwm_str)
    send(mes)
    #LED SEND END

def main():
    global led_status
    listener=SampleListener()
    controller=Leap.Controller()
    controller.add_listener(listener)
    controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    controller.set_policy(controller.POLICY_IMAGES)
    controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    #Controller.set_policy
    
    v=viewer.viewer()
    v.setDaemon(True)
    v.start()

    while True : pass
    #frame=controller.frame()
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
