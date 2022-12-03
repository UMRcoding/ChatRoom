import socketserver
import pickle
import time
import utils

users = None
history = None

# 用户管理相关函数
# 功能描述：包含从文件中加载所有已注册用户的信息（账号和密码对应的MD5值）
def load_users():
    # 读取文件
    try:
        # r是读取⼈⼯书写的数据，书写的时候是什么样⼦，读出来就是什么样。
        # rb是读取⼆进制⽂件，⾮⼈⼯书写的数据如.jpeg等这些
        return pickle.load(open('users.dat', 'rb'))
    except:
        return {}

# 功能描述：注册用户
def register(usr, pwd):
    if usr not in users.keys():
        users[usr] = pwd
        save_users()
        return True
    else:
        return False

# 功能描述：验证用户（看看密码的MD5值是否和文件中的值相同）。
def validate(usr, pwd):
    if usr in users.keys() and users[usr] == pwd:
        return True
    return False

# 功能描述：将所有已注册用户的信息保存到文件中。
def save_users():
    # wb仅对应字节写
    # w仅对应字符串写
    pickle.dump(users, open('users.dat', 'wb'))

# 聊天记录管理相关函数
# 功能描述：从文件中加载所有用户的所有聊天记录
def load_history():
    try:
        return pickle.load(open('history.dat', 'rb'))
    except:
        return {}

def get_key(u1, u2):
    return (u1, u2) if (u2, u1) not in history.keys() else (u2, u1)

# 功能描述：每条聊天记录为key-value形式，key为（sender，receiver），value为（sender，time，msg）
def append_history(sender, receiver, msg):
    if receiver == '':
        key = ('','')
    else:
        key = get_key(sender, receiver)
    if key not in history.keys():
        history[key] = []
    history[key].append((sender, time.strftime('%m月%d日%H:%M', time.localtime(time.time())), msg))
    save_history()

# 功能描述：把一条聊天记录存入内存中，返回某用户对某用户的聊天记录
def get_history(sender, receiver):
    if receiver == '':
        key = ('','')
    else:
        key = get_key(sender, receiver)
    return history[key] if key in history.keys() else []

# 功能描述：将所有用户的所有聊天记录保存到文件中。
def save_history():
    pickle.dump(history, open('history.dat', 'wb'))

# BaseRequestHandler类,可自动处理并发请求。
# 每有一个客户端请求连接时，都会new一个BaseRequestHandler类，然后在一个线程中处理相关请求。
class Handler(socketserver.BaseRequestHandler):
    clients = {}

    def setup(self):
        self.user = ''
        self.file_people = ''
        self.authed = False

    def handle(self):
        while True:
            # 每次处理一个请求，每轮询间隔秒关闭，直到关机。
            data = utils.recv(self.request)
            # 未认证
            if not self.authed:
                self.user = data['user']
                # 服务端处理登录请求、注册请求、获取所有已登录用户的列表、获取连接中的用户与其他用户的聊天记录。
                if data['cmd'] == 'login':
                    if validate(data['user'], data['pwd']):
                        utils.send(self.request, {'response': 'ok'})
                        self.authed = True
                        for user in Handler.clients.keys():
                            # 加入在线列表
                            utils.send(Handler.clients[user].request, {'type': 'people_joined', 'people': self.user})
                        Handler.clients[self.user] = self
                    else:
                        utils.send(self.request, {'response': 'fail', 'reason': '账号或密码错误！'})
                # 服务端处理注册请求
                elif data['cmd'] == 'register':
                    if register(data['user'], data['pwd']):
                        utils.send(self.request, {'response': 'ok'})
                    else:
                        utils.send(self.request, {'response': 'fail', 'reason': '账号已存在！'})
            else:
                # 服务端获取所有已登录用户的列表
                if data['cmd'] == 'get_users':
                    users = []
                    for user in Handler.clients.keys():
                        if user != self.user:
                            users.append(user)
                    utils.send(self.request, {'type': 'get_users', 'data': users})
                # 服务端获取连接中的用户与其他用户的聊天记录。
                elif data['cmd'] == 'get_history':
                    utils.send(self.request, {'type': 'get_history', 'people': data['people'], 'data': get_history(self.user, data['people'])})
                # 将连接中的用户的消息发给其期望接收的用户。
                elif data['cmd'] == 'chat' and data['people'] != '':
                    utils.send(Handler.clients[data['people']].request, {'type': 'msg', 'people': self.user, 'msg': data['msg']})
                    append_history(self.user, data['people'], data['msg'])
                # 全局广播
                elif data['cmd'] == 'chat' and data['people'] == '':
                    for user in Handler.clients.keys():
                        if user != self.user:
                            # 广播
                            utils.send(Handler.clients[user].request, {'type': 'broadcast', 'people': self.user, 'msg': data['msg']})
                    append_history(self.user, '', data['msg'])
                elif data['cmd'] == 'close':
                    self.finish()


    def finish(self):
        if self.authed:
            self.authed = False
            if self.user in Handler.clients.keys():
                del Handler.clients[self.user]
            for user in Handler.clients.keys():
                utils.send(Handler.clients[user].request, {'type': 'people_left', 'people': self.user})


if __name__ == '__main__':
    users = load_users()
    history = load_history()
    # 能处理并发请求的服务端。服务端能处理并发请求，每当有客户端请求连接时，服务端都会开启一个线程进行处理。
    # 因此当有多个客户端同时请求服务时不会造成阻塞。
    app = socketserver.ThreadingTCPServer(('127.0.0.1', 8888), Handler)
    # Handle one request at a time until shutdown
    app.serve_forever()

