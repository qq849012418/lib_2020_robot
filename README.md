# APP_TASK_RECEIVER_FOR_LIB_ROBOT

本模块基于ros和阿里云linkSDK编写，主要完成app与机器人的通信

其他模块可参考本模块的server端编写代码, 完成索书号读取,并修改状态反馈形式(目前为了测试完整性,设置的是接到任务自动计时自动完成)

action的具体格式如下:

```c++
#goal 关键的目标索书号,若需要正确printf,需要加.c_str()
string book_id
---
#result 发送是否完成,目前默认一定能完成
bool finish
---
#feedback 包括当前状态 自定义文字 完成百分比,可灵活选用
string state
string text
float32 complete_percent

```

重要的源文件有4个:

##### action_server.py 该节点使用Python编写, 代码较简洁, 可以接收client发送的含索书号的action指令,其他节点可以参考移植

##### action_client_sample.cpp 包含部分阿里云sdk代码, 与阿里云建立网络通信的通道, 也定义了ros client端, 向机器人其他模块发送状态查询信息.

aiot_dm_api.c 物模型定义文件, 里面的 static void *_dm_*recv*_property_*set_handler 函数实现了接收到app取书任务后的解析与显示.

action_server_sample.cpp 定义了server模块的C++模板

废弃的源文件: app*_node_*pub_sub.cpp 7月初测试topic通信的部分代码





 

### 使用方法(需搭配App - 下载地址 [https://jbox.sjtu.edu.cn/l/XH2KQr](https://jbox.sjtu.edu.cn/l/XH2KQr)):

将本项目clone到catkin_ws/src目录下 可修改名称为app_task_receiver便于与其他模块区分

###### 回到catkin_ws 文件夹下：
```shell
catkin_make
source devel/setup.bash
```

ctrl+alt+t 创建终端

终端1

```shell
roscore
```

终端2

若使用c++

```
rosrun app_task_receiver action_server 
```

若使用python

```
rosrun app_task_receiver action_server.py
```

若提示找不到文件或文件不可用,请在app_task_receiver/src目录下添加可执行:

```shell
sudo chmod +x action_server.py
```

终端3

```
rosrun app_task_receiver action_client 
```

#### 终端3出现以下提示信息说明client和server已建立联系

```
[ INFO] [1595127395.618794009]: ACTION SERVER START !
```

打开图书馆手机app或阿里云测试app, 借阅一本书

在client可以看到

```shell
appname=Bgfp8GoamGgVJKAUdCV6
data={"bookname":"番茄工作法图解 简单易行的时间管理方法","path":"A400","code":"C935-64/1 2011"}
code=C935-64/1 2011
[ INFO] [1595096045.994996194]: ACTIVE
[ INFO] [1595096045.995065026]: THE NUMBER RIGHT NOM IS: 0.000000
[ INFO] [1595096050.994935927]: THE NUMBER RIGHT NOM IS: 10.000000
[ INFO] [1595096055.994930777]: THE NUMBER RIGHT NOM IS: 20.000000
[ INFO] [1595096060.994933426]: THE NUMBER RIGHT NOM IS: 30.000000
[ INFO] [1595096065.994966674]: THE NUMBER RIGHT NOM IS: 40.000000
[ INFO] [1595096070.994963359]: THE NUMBER RIGHT NOM IS: 50.000000
[ INFO] [1595096075.995018244]: THE NUMBER RIGHT NOM IS: 60.000000
[ INFO] [1595096080.995008601]: THE NUMBER RIGHT NOM IS: 70.000000
[ INFO] [1595096085.994888934]: THE NUMBER RIGHT NOM IS: 80.000000
[ INFO] [1595096090.994956635]: THE NUMBER RIGHT NOM IS: 90.000000
[ INFO] [1595096095.995064020]: DONE

```

在server可以看到

```shell
[ INFO] [1595096141.329962866]: THE GOAL IS: [C935-64/1 2011]
[ INFO] [1595096191.330028019]: COUNT DONE
```

