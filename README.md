# 开源项目说明

**目的：学术研究**

如果您遇到任何安装或使用问题，可以通过QQ或issue的方式告诉我。同时使用本项目写论文或做其它学术研究的朋友，如果想把自己的研究成果展示在下面，也可以通过QQ或issue的方式告诉我。看到的小伙伴记得点点右上角的Star~

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202212040012791.png)



## 一、实验名称

计网实践作业ChatRoom——基于python Tkinter和python socket的网络聊天室



## 二、实验目的

1.了解并掌握python Tkinter模块的使用，并能熟练利用Tkinter模块快速搭建GUI应用。

2.理解并掌握TCP/IP网络传输的工作原理。

3.掌握python socket模块的使用，能用python socket模块快速实现数据的TCP、UDP传输。

4.了解基本的数据加密算法（如AES，MD5等），并能应用于本项目中。

5.掌握python多线程处理问题的方法。



## 三、实验内容

基于python Tkinter和python socket实现一个网络聊天室，可进行世界聊天和一对一聊天。

1. 精美的UI。本项目用python的Tkinter模块进行GUI开发。经过本人的不懈努力，最终绘制出了赏心悦目的界面。
2. 能处理并发请求的服务端。服务端能处理并发请求，每当有客户端请求连接时，服务端都会开启一个线程进行处理，因此当有多个客户端同时请求服务时不会造成阻塞。
3. 实现用户注册功能。用户输入账号和密码，点击注册，如果账号在后台中不存在，则进行注册，将账号和密码的MD5值以key-value的形式保存。
4. 实现用户登录功能。用户输入账号和密码，点击登录，如果账号在后台存在，并且用户输入的密码的MD5值与后台一致，则登录成功。
5. 世界聊天功能。任何已登录的用户都能在世界聊天窗口发送消息，且该消息能被其他所有用户看到。任何已登录的用户都能在世界聊天窗口看到其他用户在世界聊天窗口发送的消息。
6. 一对一聊天功能。所有已登录的其他用户都显示在在线用户列表中，用户可以点击任意其他已登录用户与其进行一对一聊天。
7. 保存历史聊天记录功能。无论是世界聊天还是一对一聊天，期间的所有聊天记录都会保存在后台中。用户一旦登录便会加载过往的聊天记录。
8. 数据传输加密功能。本项目所有在网络上传输的数据都用AES算法进行加密。



## 四、项目结构

### 运行环境

+ Python-310
+ pycryptodome-3.15.0



切记使用 pycrytodome 库，大小写问题也不用管了，安装方式如下：

```python
pip install pycryptodome
```

>1. pycrypto，pycrytodome和crypto是一个东西，crypto在python上面的名字是pycrypto它是一个第三方库，但是已经停止更新三年了，所以不建议安装这个库。
>
>2. windows下python3.6安装也不会成功！这个时候pycryptodome就来了，它是pycrypto的延伸版本，用法和pycrypto 一模一样。
>
>3. 所以，直接安装：pip install pycryptodome
>
>4.  在使用的时候导包可能是有问题的，这个时候只要修改一个文件夹的名称就可以完美解决这个问题
>
>   C:\Users\Administrator\AppData\Local\Programs\Python\Python36\Lib\site-packages 找到这个路径，下面有一个文件夹叫做crypto，将c改成C，改成大写就ok了！



### 运行配置

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202301040026938.png)



## 五、运行截图

### 登陆页面

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202301040034665.png)



### 注册页面

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202301040035637.png)



### 聊天室首页

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202301040035625.png)



### 世界聊天室界面

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202301040036196.png)



### 单聊界面

![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202301040037391.png)



![](https://umrcoding.oss-cn-shanghai.aliyuncs.com/Obsidian/202301040037403.png)



