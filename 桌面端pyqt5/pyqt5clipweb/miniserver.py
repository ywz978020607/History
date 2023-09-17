#! /usr/bin/env python3
# -*- coding:UTF-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
# import cgi
import _thread

host = ('127.0.0.1',8003)

class TodoHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_error(415, 'Only post is supported')

    def do_POST(self):
        # ctype, pdict = cgi.parse_header(self.headers['content-type'])
        # print(ctype, pdict)
        print(self.headers)
        print(self.path)  # 获取请求的url)

        length = int(self.headers['content-length']) 
        datas = self.rfile.read(length) # 获取请求参数数据，请求数据为json字符串
        print(datas)
        # rjson = json.loads(datas.decode()) #不一定成功
        # print(rjson,type(rjson))

        # print(help(self))

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"code": 200}).encode())

def new_thread():
    import os
    file_port, file_ip = "8080", "127.0.0.1"
    os.system("python -m http.server {} --bind {}".format(file_port, file_ip))

if __name__ == '__main__':
    _thread.start_new_thread(new_thread,()) # 开启静态文件服务器

    server = HTTPServer(host, TodoHandler)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()