#!/usr/bin/env python
#coding=utf-8
import rospy
import math
#导入mgs到pkg中
from app_task_receiver.msg import cv

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


if __name__ == '__main__':

    message_node()
    # 等待关闭服务器
    rospy.spin()
