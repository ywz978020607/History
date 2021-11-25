#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : ShiMeng
# @File    : send_sms.py
# @Software: PyCharm
from twilio.rest import Client
# Your Account SID from twilio.com/console
account_sid = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx" #"AC848159xxxxxxxxxxxx"
# Your Auth Token from twilio.com/console
auth_token  = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
client = Client(account_sid, auth_token)
message = client.messages.create(
    # 这里中国的号码前面需要加86
    to="+861565257xxx",#"+接收者的号码",
    from_="+170840xxxx",#"+twilio给你的号码 ",
    body="Hello from Python!")
print(message.sid)