/*
 *action服务端
 */
#include <ros/ros.h>
#include <actionlib/server/simple_action_server.h>
#include "app_task_reciver/qushuAction.h"    /* 这个头文件每个人写的的名字都可能不同，package name/header file name.h */

typedef actionlib::SimpleActionServer<app_task_reciver::qushuAction> Server;

/*
 *action 接口
 */
void execute(const app_task_reciver::qushuGoalConstPtr& goal, Server* as)
{
    ros::Rate r(0.2); /* 设置运行频率，这里设置为0.2hz */
    app_task_reciver::qushuFeedback feedback;    /* 创建一个feedback对象 */

    ROS_INFO("THE GOAL IS: [%s]", goal ->book_id.c_str());

    int count = 0;
        for (; count <100; count+=10)
        {
            feedback.complete_percent = count;
            as -> publishFeedback(feedback);

            r.sleep();
        }

    ROS_INFO("COUNT DONE");

    as -> setSucceeded();   /* 发送result */
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "action_server_demo");
    ros::NodeHandle nh;

    /* 创建server对象; */
    Server server(nh, "action_demo", boost::bind(&execute, _1, &server), false);

    server.start();

    ros::spin();
    return 0;
}