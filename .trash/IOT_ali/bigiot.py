"""
贝壳物联是一个让你与智能设备沟通更方便的物联网云平台，你可以通过互联网以对话、遥控器等形式与你的智能设备聊天、发送指令，查看实时数据，
跟实际需求设置报警条件，通过APP、邮件、短信、微博、微信等方式通知用户。

| 在使用前,需要先到贝壳物联注册账号,并增加设备 https://www.bigiot.net
| 贝壳物联平台通讯协议：https://www.bigiot.net/help/1.html
"""
"""
The MIT License (MIT)

Copyright (c) 2019, labplus@Tangliufeng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import _thread
import socket
import json
import time

Server_IP = "www.bigiot.net"
Server_Port = 8282


class Device:
    """
    构建bigiot设备

    :param id(int): 智能设备ID号,类型为整形
    :param api_key(str): 智能设备APIKEY,类型为字符串
    """

    def __init__(self, id, api_key):
        self.ID = str(id)
        self.K = api_key
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(True)
        self.socket.connect((Server_IP, Server_Port))
        _thread.start_new_thread(self._reciver_loop, ())
        self.say_cb = None
        self.checkinOK = False
        self._send_return = None
        self.check_out()
        for i in range(3):
            self.check_in()
            if self.checkinOK:
                break
            time.sleep(1)

# Send data, and wait for a return

    def _socket_send(self, str):
        self._send_return = None
        try:
            self.socket.send(str)
            # print("Send: %s" % str)
        except OSError as e:
            if e.args[0] == 104:
                self.__init__(self.ID, self.K)
                self.socket.send(str)
            else:
                raise e

    def say_callback(self, f):
        """
        接收设备通讯的回调函数

        :param f(function): 回调函数,f(msg,id,name)。``msg`` 参数为接收消息, ``id`` 参数为发送设备ID, ``name`` 参数为设备名称。
        """
        self.say_cb = f

# Sockets receive data

    def _reciver_loop(self):
  
        while True:
    
            res = self.socket.recv(512).decode()

            if len(res) == 0:
                continue
            dict_res = json.loads(res)
            # 应答服务器的心跳包
            if dict_res["M"] == 'b':
                self.socket.send('{"M":"beat"}\n')
                continue
            # 服务器连接成功
            elif dict_res["M"] == "WELCOME TO BIGIOT":
                print("WELCOME TO BIGIOT !")
                continue

            self.respon = dict_res
            # print(self.respon)

            method = dict_res["M"]

            # check login
            if method == "checkinok":
                self.checkinOK = True

            if method == "isOL":
                self._send_return = dict_res["R"]

            if method == "checked" or method == "connected":
                self._send_return = dict_res["M"]

            if method == "time":
                self._send_return = dict_res["T"]

            # say 指令
            if method == "say" and dict_res["C"] is not None:
                msg = (dict_res["C"], dict_res["ID"], dict_res["NAME"])
                self.say_cb(msg)

            self.isRecv = True

    def check_in(self):
        """
        设备登录
        """
        obj = {"M": "checkin", "ID": self.ID, "K": self.K}
        obj = json.dumps(obj) + "\n"
        self._socket_send(obj)

    def check_out(self):
        """
        设备下线
        """
        obj = {"M": "checkout", "ID": self.ID, "K": self.K}
        obj = json.dumps(obj) + "\n"
        self._socket_send(obj)

    def say(self, user_id=None, group_id=None, device_id=None, msg=None):
        """
        设备间的通讯

        :param user_id(int): 用户ID。如你的用户ID为U5600,则user_id=5600。可用于web、微信、app平台间通讯。
        :param group_id(int): 群组ID。你可以在平台设置多个设备为一个群组,编译相互通讯。
        :param device_id(int): 设备ID。
        :param msg(str):发送消息。
        """
        while True:
            if user_id is not None:
                ID = "U" + str(user_id)
                break
            if group_id is not None:
                ID = "G" + str(group_id)
                break
            if device_id is not None:
                ID = "D" + str(device_id)
                break

        obj = {"M": "say", "ID": ID, "C": msg}
        obj = json.dumps(obj) + "\n"
        self._socket_send(obj)

# Submit data to the data interface

    def update(self, id, data):
        """
        向接口发送数据。先在平台新增并设置接口。

        :param id(int): 接口ID,类型为整形
        :param data(str): 发送数据,类型为字符串,一般用于上传传感器数据。
        """
        dict_data = {}
        dict_data[str(id)] = data
        obj = {"M": "update", "ID": str(id), "V": dict_data}
        obj = json.dumps(obj) + "\n"
        self._socket_send(obj)

# Check online

    def is_online(self, device_id):
        """
        查询设备是否在线

        :param device_id(int): 你要查询的设备ID
        :return: 返回设备状态。0代表不在线，1代表在线
        """
        self.isRecv = False
        obj = {"M": "isOL", "ID": "D" + str(device_id)}
        obj = json.dumps(obj) + "\n"
        start_time = time.time()
        self._socket_send(obj)
        while not self.isRecv:
            if time.time() - start_time > 2:
                return None
        return int(self._send_return["D" + str(device_id)])

    def status(self):
        """
        查询当前设备状态,两次查询间隔不得小于10s

        :return: connected代表已连接服务器尚未登录，checked代表已连接且登录成功
        """
        self.isRecv = False
        obj = {"M": "status"}
        obj = json.dumps(obj) + "\n"
        self._socket_send(obj)
        start_time = time.time()
        while not self.isRecv:
            if time.time() - start_time > 1:
                return None
        return self._send_return

    def time(self, format="stamp"):
        """
        查询服务器时间

        :param format(str): stamp(1466659300)、"Y-m-d"(2016-06-21)、Y.m.d(2016.06.21)、Y-m-d H:i:s(2016-06-21 10:25:30)
        :return: 返回时间
        """
        self.isRecv = False
        obj = {"M": "time", "F": format}
        obj = json.dumps(obj) + "\n"
        self._socket_send(obj)
        start_time = time.time()
        while not self.isRecv:
            if time.time() - start_time > 1:
                raise bigiotException("Bigiot Server no response ")
        return self._send_return


# #Send an alert
#     def alert(self, C, B):
#         obj = {"M": "alert", "C": C, "B": B}
#         obj = json.dumps(obj)+"\n"
#         self.socket.send(obj)


