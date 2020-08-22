#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# app_task_receiver服务器端
# 导入app_task_receiver中的文件
import roslib; roslib.load_manifest('app_task_receiver')
# 导入rospy,进行python编写
import rospy
# 导入actionlib进行action通信
import actionlib
# 导入app_task_receiver中的msg,用于Goal、Feedback、Result的调用
import app_task_receiver.msg
# Twist用于控制Xbot进行移动
from app_task_receiver.msg import qushuAction

import cv2
import os
import time
import threading
import numpy as np
import pytesseract


# 建立Action服务器端
class qushuServer:
  # 定义变量_feedback用于查看任务进度,result查看完成的指令个数
  _feedback = app_task_receiver.msg.qushuFeedback()
  _result =app_task_receiver.msg.qushuResult()
  # 初始化对应变量
  _result.finish=0
  _feedback.complete_percent=0

  # 初始化服务器
  def __init__(self):
      # 打印提示信息
      rospy.loginfo('Initing!')
      # 设置action服务器，四个参数分别为（action名称、action类型、Callback函数、自启动设置）
      self.server = actionlib.SimpleActionServer('action_demo',qushuAction, self.execute, False)
      # 启动服务器
      self.server.start()
      # 显示提示信息
      rospy.loginfo('Start the server!')

  # 定义执行函数
  def execute(self, goal):
      rate = rospy.Rate(0.5)#仅为示意,展示时可以调快
      #打印索书号
      rospy.loginfo('THE GOAL IS: [%s]'%goal.book_id)
      count=0
      while count<100:
            count+=10
            self._feedback.complete_percent = count
            self.server.publish_feedback(self._feedback)
            rate.sleep()
      rospy.loginfo('COUNT DONE')

      self.server.set_succeeded()
      
      
      
      
      

  

# 主函数
if __name__ == '__main__':
   # 初始化acion节点
   rospy.init_node('action_server_demo')
   # 建立action服务器
   server = qushuServer()
   # 等待关闭服务器
   rospy.spin()
