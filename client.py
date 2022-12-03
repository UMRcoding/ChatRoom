import tkinter.filedialog
import tkinter.messagebox
import tkinter as tk
import threading
import hashlib
import socket
import time

import utils
# 登录界面
# 功能描述：基于tkinter模块搭建，含有账号输入框、密码输入框、登录按钮、注册按钮。
class Login_win:
    def show(self):
        # 进入消息循环
        self.win.mainloop()

    def destroy(self):
        self.win.destroy()

    def __init__(self):
        self.win = tk.Tk()
        # tk.StringVar() 同时保证了值的变更随时可以显示在界面上
        self.user = tk.StringVar()
        self.pwd = tk.StringVar()

        # 总窗口配置
        self.win.geometry("440x280")
        self.win.title("登录")
        # 设置窗口是否可变长、宽，True：可变，False：不可变
        self.win.resizable(width=True, height=True)
        # 设置背景颜色
        self.win.configure(background="#D1EDE1")

        # 左侧 账号文本 配置
        self.label1 = tk.Label(self.win)
        self.label1.place(relx=0.055, rely=0.1, height=31, width=89)
        self.label1.configure(text='账号')
        # 设置背景颜色
        self.label1.configure(background="#7BC5AE")

        # 用户账号输入文本框 配置
        self.entry_user = tk.Entry(self.win)
        self.entry_user.place(relx=0.28, rely=0.11, height=26, relwidth=0.554)
        self.entry_user.configure(textvariable=self.user)
        # 设置背景颜色
        self.entry_user.configure(background="#D1EDE9")

        # 左侧 密码文本 配置
        self.label2 = tk.Label(self.win)
        self.label2.place(relx=0.055, rely=0.27, height=31, width=89)
        self.label2.configure(text='密码')
        # 设置背景颜色
        self.label2.configure(background="#7BC5AE")

        # 用户密码输入文本框 配置
        self.entry_pwd = tk.Entry(self.win)
        self.entry_pwd.place(relx=0.28, rely=0.28, height=26, relwidth=0.554)
        self.entry_pwd.configure(show="*")
        self.entry_pwd.configure(textvariable=self.pwd)
        self.entry_pwd.configure(background="#D1EDE9")

        # 登录按钮 配置
        self.btn_login = tk.Button(self.win)
        self.btn_login.place(relx=0.13, rely=0.6, height=32, width=88)
        self.btn_login.configure(text='登录')
        self.btn_login.configure(background="#7BC5AE")

        # 注册按钮 配置
        self.btn_reg = tk.Button(self.win)
        self.btn_reg.place(relx=0.6, rely=0.6, height=32, width=88)
        self.btn_reg.configure(text='注册')
        self.btn_reg.configure(background="#7BC5AE")

# 聊天窗口界面
# 功能描述：基于tkinter模块搭建，含有其他已登录用户列表显示框、聊天记录显示框、发送消息输入框、发送消息按钮等。
class Main_win:
    closed_fun = None

    def show(self):
        # 进入消息循环
        self.win.mainloop()

    def destroy(self):
        try:
            self.closed_fun()
        except:
            pass
        self.win.destroy()

    # 构造方法，参数为按钮事件处理函数，从客户端main传进来，可以实现按钮回调
    def __init__(self):
        # 初始化参数实例变量，聊天室主页面
        self.win = tk.Tk()
        self.win.protocol('WM_DELETE_WINDOW', self.destroy)
        self.win.geometry("480x320")
        self.win.title("聊天室")
        self.win.resizable(width=True,height=True)

        self.msg = tk.StringVar()
        self.name = tk.StringVar()

        self.user_list = tk.Listbox(self.win)
        self.user_list.place(relx=0.75, rely=0.15, relheight=0.72, relwidth=0.23)

        self.label1 = tk.Label(self.win)
        self.label1.place(relx=0.76, rely=0.075, height=21, width=101)
        self.label1.configure(text='在线用户')

        self.history = tk.Text(self.win)
        self.history.place(relx=0.02, rely=0.24, relheight=0.63, relwidth=0.696)
        self.history.configure(state='disabled')

        self.entry_msg = tk.Entry(self.win)
        self.entry_msg.place(relx=0.02, rely=0.9, height=24, relwidth=0.59)
        self.entry_msg.configure(textvariable=self.msg)

        self.btn_send = tk.Button(self.win)
        self.btn_send.place(relx=0.62, rely=0.89, height=28, width=45)
        self.btn_send.configure(text='发送')

        self.label2 = tk.Label(self.win)
        self.label2.place(relx=0.24, rely=0.0, height=57, width=140)
        self.label2.configure(textvariable=self.name)

# 声明全局变量方便，在静态函数重调用
login_win = None
main_win = None
my_socket = None
user_name = ''
current_session = ''
users = {}

server_ip = "127.0.0.1"
server_port = "8888"


# 客户端相关函数
def close_socket():
    utils.send(my_socket, {'cmd': 'close'})
    my_socket.shutdown(2)
    my_socket.close()


# 功能描述：登录按钮点击事件：当登录按钮点击时向服务端请求登录，如果登录成功则关闭登录页面，开启聊天页面。
def on_btn_login_clicked():
    global my_socket, user_name, login_win, main_win
    # socket创建socket，客户端和服务端要用socket。AF_INET表示TCP协议族，SOCK_STREAM基于TCP
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.settimeout(5)
    if login_win.user.get() != '' and login_win.pwd != '':
        my_socket.connect((server_ip, int(server_port)))
        utils.send(my_socket, {'cmd': 'login', 'user': login_win.user.get(), 'pwd': hashlib.sha1(login_win.pwd.get().encode('utf-8')).hexdigest()})
        server_response = utils.recv(my_socket)
        if server_response['response'] == 'ok':
            user_name = login_win.user.get()
            # 销毁登录框
            login_win.destroy()
            main_win = Main_win()
            main_win.closed_fun = close_socket

            # 置顶欢迎
            main_win.name.set('上午好!   %s' % user_name)
            main_win.btn_send.configure(command=on_btn_send_clicked)
            main_win.user_list.bind('<<ListboxSelect>>', on_session_select)
            utils.send(my_socket, {'cmd': 'get_users'})
            utils.send(my_socket, {'cmd': 'get_history', 'people': ''})

            t = threading.Thread(target=recv_async, args=())
            t.setDaemon(True)
            t.start()
            main_win.show()
        elif server_response['response'] == 'fail':
            tkinter.messagebox.showerror('警告', '登录失败：' + server_response['reason'])
            close_socket()
    else:
        tkinter.messagebox.showerror('警告', '账号和密码不能为空！')

# 功能描述：注册按钮点击事件：当注册按钮点击时向服务端请求注册，得到回应后显示回应的消息（注册成功或注册失败、账号已存在等消息）。
def on_btn_reg_clicked():
    global my_socket, login_win
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.settimeout(5)
    if login_win.user.get() != '' and login_win.pwd.get() != '':
        my_socket.connect((server_ip, int(server_port)))
        utils.send(my_socket, {'cmd': 'register', 'user': login_win.user.get(), 'pwd': hashlib.sha1(login_win.pwd.get().encode('utf-8')).hexdigest()})
        server_response = utils.recv(my_socket)
        if server_response['response'] == 'ok':
            tkinter.messagebox.showinfo('注意', '注册成功！')
        elif server_response['response'] == 'fail':
            tkinter.messagebox.showerror('警告', '注册失败：' + server_response['reason'])
    else:
        tkinter.messagebox.showerror('警告', '账号和密码不能为空！')
    close_socket()

def recv_async():
    global my_socket, users, main_win, current_session
    while True:
        # 点击用户列表中的某用户时，显示与其一对一聊天的窗口。
        data = utils.recv(my_socket)
        # 功能描述：刷新所有已登录用户列表：当开启聊天页面或收到服务端发来的新用户登录/登出的消息时刷新用户列表。
        if data['type'] == 'get_users':
            users = {}
            for user in [''] + data['data']:
                users[user] = False
            refresh_user_list()
        # 功能描述：将聊天记录加入聊天记录显示框。
        elif data['type'] == 'get_history':
            if data['people'] == current_session:
                # 历史记录管理
                main_win.history['state'] = 'normal'
                main_win.history.delete('1.0', 'end')
                main_win.history['state'] = 'disabled'
                for entry in data['data']:
                    append_history(entry[0], entry[1], entry[2])
        # 功能描述：当用户刚登录时显示世界聊天聊天记录，当用户点击其他用户与其一对一聊天时显示与其的聊天记录。
        elif data['type'] == 'people_joined':
            users[data['people']] = False
            refresh_user_list()
        # 功能描述：接收服务端消息函数。该函数运行在一个独立的线程中，不断接收服务端发来的消息。
        elif data['type'] == 'people_left':
            if data['people'] in users.keys():
                del users[data['people']]
            if data['people'] == current_session:
                current_session = ''
                main_win.name.set('%s -> 世界聊天' % user_name)
                users[''] = False
                utils.send(my_socket, {'cmd': 'get_history', 'people': ''})
            refresh_user_list()
        elif data['type'] == 'msg':
            if data['people'] == current_session:
                append_history(data['people'], time.strftime('%m月%d日%H:%M', time.localtime(time.time())), data['msg'])
            else:
                users[data['people']] = True
                refresh_user_list()
        elif data['type'] == 'broadcast':
            if current_session == '':
                append_history(data['people'], time.strftime('%m月%d日%H:%M', time.localtime(time.time())), data['msg'])
            else:
                users[''] = True
                refresh_user_list()

def refresh_user_list():
    main_win.user_list.delete(0, 'end')
    for user in users.keys():
        name = '世界聊天室' if user == '' else user
        # 未读消息
        if users[user]:
            name += ' (*)'
        main_win.user_list.insert('end', name)

def append_history(sender, time, msg):
    main_win.history['state'] = 'normal'
    main_win.history.insert('end', '%s - %s\n' % (sender, time))
    main_win.history.insert('end', msg + '\n\n', 'text')
    main_win.history.see('end')
    main_win.history['state'] = 'disabled'

def on_btn_send_clicked():
    global my_socket, user_name, current_session, main_win
    if main_win.msg.get() != '':
        utils.send(my_socket, {'cmd': 'chat', 'people': current_session, 'msg': main_win.msg.get()})
        append_history(user_name, time.strftime('%m月%d日%H:%M', time.localtime(time.time())), main_win.msg.get())
        main_win.msg.set('')
    else:
        tkinter.messagebox.showinfo('警告', '消息不能为空！')

def on_session_select(event):
    global current_session, main_win, user_name, users
    w = event.widget
    changed = False
    if len(w.curselection()) != 0:
        index = int(w.curselection()[0])
        if index != 0:
            if current_session != w.get(index).rstrip(' (*)'):
                changed = True
                current_session = w.get(index).rstrip(' (*)')
                main_win.name.set('%s -> %s' % (user_name, current_session))
                users[current_session] = False
                refresh_user_list()
        elif index == 0:
            if current_session != '':
                changed = True
                current_session = ''
                main_win.name.set('%s -> global' % user_name)
                users[''] = False
                refresh_user_list()
        if changed:
            utils.send(my_socket, {'cmd': 'get_history', 'people': current_session})

if __name__ == '__main__':
    login_win = Login_win()
    login_win.btn_login.configure(command=on_btn_login_clicked)
    login_win.btn_reg.configure(command=on_btn_reg_clicked)
    login_win.show()