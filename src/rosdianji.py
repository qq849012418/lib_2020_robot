#!/usr/bin/env python
#coding=utf-8
import rospy
import math
#导入mgs到pkg中
from app_task_receiver.msg import cv
import RPi.GPIO as GPIO
import time
import threading
velocity = 0.001
#回调函数输入的应该是msg
def callback(cv):
    rospy.loginfo('Listener: cv_info  state=%s', cv.state)

def message_node():
    #根据模块名, 修改Publisher 函数第一个参数
    rospy.init_node('rosdianji', anonymous=True)
    #Subscriber函数第一个参数是接收目标topic的名称,Publisher则对应自身发送topic的名称
    sub = rospy.Subscriber('cv_info', cv, callback)
    #更新频率
    rate = rospy.Rate(1) 

class Move_Control :
    def setStep(self,mode, w1, w2, w3, w4) :  # mode:1代表竖直軸  2代表y轴  3代表x轴 4代表旋转
        if mode == 1 :
            GPIO.output (self.IN1, w1)
            GPIO.output (self.IN3, w2)
            GPIO.output (self.IN2, w3)
            GPIO.output (self.IN4, w4)
        if mode == 2 :
            GPIO.output (self.IN5, w1)
            GPIO.output (self.IN6, w2)
            GPIO.output (self.IN7, w3)
            GPIO.output (self.IN8, w4)
        if mode == 3 :
            GPIO.output (self.IN9, w1)
            GPIO.output (self.IN10, w2)
            GPIO.output (self.IN11, w3)
            GPIO.output (self.IN12, w4)
        if mode == 4 :
            GPIO.output (self.IN14, w1)
            GPIO.output (self.IN15, w2)
            GPIO.output (self.IN16, w3)
            GPIO.output (self.IN17, w4)


    def stop(self,mode) :
        __setStep (mode, 0, 0, 0, 0)


    def forward(self,mode, steps, delay=velocity) :#step是发送多少脉冲循环的意思，delay影响电机的运动速度
        num = int(steps)
        print("forward",num)
        #self.lock.acquire()
        count = 0
        for i in range (0, num) :
            self.setStep(mode,1, 0, 0, 0)
            time.sleep(delay)
            self.setStep(mode,0, 1, 0, 0)
            time.sleep(delay)
            self.setStep(mode,0, 0, 1, 0)
            time.sleep(delay)
            self.setStep(mode,0, 0, 0, 1)
            time.sleep(delay)
            count+=1
        #self.lock.release()
        print(count)


    def backward(self,mode, steps=1, delay=velocity) :
        num = int(steps)
        print("back",num)
        count = 0
        #self.lock.acquire()
        for i in range (0, num) :
            self.setStep(mode,0, 0, 0, 1)
            time.sleep(delay)
            self.setStep(mode,0, 0, 1, 0)
            time.sleep(delay)
            self.setStep(mode,0, 1, 0, 0)
            time.sleep(delay)
            self.setStep(mode,1, 0, 0, 0)
            time.sleep(delay)
            count+=1
        #self.lock.release()
        print(count)

    def __setup(self) :
        GPIO.setwarnings (False)
        GPIO.setmode (GPIO.BOARD)  # Numbers GPIOs by physical location
        GPIO.setup (self.IN1, GPIO.OUT)  # Set pin's mode is output
        GPIO.setup (self.IN2, GPIO.OUT)
        GPIO.setup (self.IN3, GPIO.OUT)
        GPIO.setup (self.IN4, GPIO.OUT)
        GPIO.setup (self.IN5, GPIO.OUT)  # Set pin's mode is output
        GPIO.setup (self.IN6, GPIO.OUT)
        GPIO.setup (self.IN7, GPIO.OUT)
        GPIO.setup (self.IN8, GPIO.OUT)
        GPIO.setup (self.IN9, GPIO.OUT)  # Set pin's mode is output
        GPIO.setup (self.IN10, GPIO.OUT)
        GPIO.setup (self.IN11, GPIO.OUT)
        GPIO.setup (self.IN12, GPIO.OUT)
        GPIO.setup (self.IN14, GPIO.OUT)  # Set pin's mode is output
        GPIO.setup (self.IN15, GPIO.OUT)
        GPIO.setup (self.IN16, GPIO.OUT)
        GPIO.setup (self.IN17, GPIO.OUT)
        # 舵机初始化
        GPIO.setup (self.IN13, GPIO.OUT)
        global pwmhand
        pwmhand = GPIO.PWM (self.IN13, 50)
        pwmhand.start (0)  # 回归0位
        print ("初始化")

    def __setDirection(self,direction):
        duty = 10/180*direction + 2.5
        pwmhand.ChangeDutyCycle(duty)
        time.sleep(5)

    def openhand(self):
        self.__setDirection(50)
        print("open")

    def closehand(self):
         self.__setDirection(150)
         print("close")

    def move_x(self,distance):#distance的单位是毫米
        #在这个函数中实现移动自由度x的目的，delay代表速度，step代表距离
        if distance == 0: return
        if distance > 0:
            self.forward(3, distance / self.d_x * self.r_x,0.00001)
            self.location_x += distance
        else:
            self.backward (3, -distance / self.d_x * self.r_x,0.00001)
            self.location_x += distance

    def move_y(self, distance):
        #在这个函数中实现移动自由度y的目的，delay代表速度，step代表距离
        if distance == 0: return
        if distance > 0 :
            self.forward (2, distance / self.d_y * self.r_y,0.0000008)
            self.location_y += distance
        else :
            self.backward (2, -distance / self.d_y * self.r_y,0.0000008)
            self.location_y += distance

    def move_z(self, distance):
        #在这个函数中实现移动自由度z的目的，delay代表速度，step代表距离
        if distance == 0: return
        if distance > 0 :
            self.forward (1, distance / self.d_z * self.r_z,0.000008)
            self.location_z += distance
        else :
            self.backward (1, -distance / self.d_z * self.r_z,0.000008)
            self.location_z += distance


    def move_seta(self, angle):
        #在这个函数中实现转动转盘的目的，delay代表速度，step代表圈数
        if angle == 0: return
        if self.location_rot+angle > 360:#防止把线绕道一起
            self.move_seta(angle-360)
            return
        elif self.location_rot + angle <-360:
            self.move_seta(angle+360)
            return
        if angle > 0:
            self.forward(4,angle/self.d_rotatio*self.r_rotation,0.0003)#这个速度有点慢,0.00005速度合适但是不能辨认方向
            self.location_rot += angle
        else:
            self.backward(4,-angle/self.d_rotatio*self.r_rotation,0.0003)
            self.location_x += angle
        print(angle)
        print(self.location_rot)

    def __destroy(self) :
        pwmhand.stop ()
        GPIO.cleanup ()

    def Reset(self):
        #机械臂回归初始位置
        self.move_to_target(0,0,0,0)
        #一般情况下不需要旋转轴归位，因为旋转轴用手是转不动的

    def move_to_target(self,x,y,z,rot):
        if x > self.X_MAX or x < 0:
            print("X轴越界")
            return
        if y > self.Y_MAX or y < 0:
            print("Y轴越界")
            return
        if z > self.Z_MAX or z < 0:
            print("Z轴越界")
            return
        t1 = threading.Thread (target=Move_Control.move_x, args=(self,x-self.location_x,))
        t2 = threading.Thread (target=Move_Control.move_y, args=(self,y-self.location_y,))
        t3 = threading.Thread (target=Move_Control.move_z, args=(self,z-self.location_z,))
        t4 = threading.Thread (target=Move_Control.move_seta, args=(self,rot-self.location_rot,))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        #print(y-self.location_y)
        #self.move_x(x-self.location_x)
        #self.move_y(y-self.location_y)
        #self.move_z(z-self.location_z)
        #self.move_seta(rot-self.location_rot)
        


    def __init__(self):
        self.IN1 = 29  # 绿色# 竖直轴的连接串口编号
        self.IN2 = 32  # 紫色
        self.IN3 = 31  # 蓝色
        self.IN4 = 33  # 灰色


        # y轴的连接串口编号，
        self.IN5 = 3  # 白色
        self.IN6 = 8  # 棕色
        self.IN7 = 5  # 黑色
        self.IN8 = 10  # 红色

        #x轴的连接串口编号，
        self.IN9 = 11  # 黄色
        self.IN10 = 12  #橙色
        self.IN11 = 13  #红色
        self.IN12 = 15 #棕色

        # 舵机的控制端口
        self.IN13 = 7

       # xuanzhuan轴的连接串口编号，
        self.IN14 = 36  # 黄色
        self.IN15 = 38  # 红色
        self.IN16 = 37  # 橙色
        self.IN17 = 40  # 棕色

        #电机参数:多少次脉冲电机转一圈
        self.r_x = 6400
        self.r_y = 1600
        self.r_z = 3200
        self.r_rotation = 400

        #同步带参数：电机转一圈，同步带移动的距离
        self.d_x = 72
        self.d_y = 76.8
        self.d_z = 75.25
        self.d_rotatio =  4.1744#电机转一圈，分度盘转多少度


        #机械臂最大工作范围
        self.X_MAX = 87#毫米
        self.Y_MAX = 200
        self.Z_MAX = 287
    
        self.__setup() #设置串口状态
        self.openhand()
        self.location_x = 0
        self.location_y = 0
        self.location_z = 0
        self.location_rot = 0
        self.lock = threading.Lock()



    def __del__(self):
        #将所有机械臂归位到初始位置
        self.move_to_target(0,0,0,0)
        self.openhand()
        self.__destroy() #释放串口
        print("gouwei")

    def forward_s(self,mode,delay, steps):
        deta = 1/steps
        percent = deta
        de = 0.001
        k = (0.001-delay)/0.01
        for i in range(0, steps):
            if percent < 0.1:
                de = k*(percent - 0.1)*(percent - 0.1) + delay
            elif percent >= 0.1 and percent <= 0.9:
                de = delay
            else:
                de = k*(percent - 0.9)*(percent - 0.9) + delay
            percent+=deta
            self.setStep(mode,1, 0, 0, 0)
            time.sleep(de)
            self.setStep(mode,0, 1, 0, 0)
            time.sleep(de)
            self.setStep(mode,0, 0, 1, 0)
            time.sleep(de)
            self.setStep(mode,0, 0, 0, 1)
            time.sleep(de)

    def backward_s(self,mode,delay, steps):
        deta = 1/steps
        percent = deta
        de = 0.001
        k = (0.001-delay)/0.01
        for i in range(0, steps):
            if percent < 0.1:
                de = k*(percent - 0.1)*(percent - 0.1) + delay
            elif percent >= 0.1 and percent <= 0.9:
                de = delay
            else:
                de = k*(percent - 0.9)*(percent - 0.9) + delay
            percent+=deta
            self.setStep(mode,0, 0, 0, 1)
            time.sleep(de)
            self.setStep(mode,0, 0, 1, 0)
            time.sleep(de)
            self.setStep(mode,0, 1, 0, 0)
            time.sleep(de)
            self.setStep(mode,1, 0, 0, 0)
            time.sleep(de)
if __name__ == '__main__':

    message_node()
    
    #dianjiorigintest
    P = Move_Control()
    P.move_to_target(50,100,100,90)
    time.sleep(10)
    #P.closehand()
    del P
    # 等待关闭服务器
    rospy.spin()
