# 内网梯子(同时作为服务端+客户端)
## 目前BUAA校内服务器已部署
- 10808和10809分别对应socks5和http代理(ip保密需私聊, switch等游戏机也可以直接代理自动翻墙加速)
- 支持校内ss和vmess协议(保密需私聊)

## 1. 功能
```
内网梯子功能：
1. 实现校园网免流量(主要因为服务器上网免流，且内网互相通信免流)
2. 搭配外网梯子，实现自动识别国外ip代理上网，平时日常直接开全局
3. 同时监听本机的端口，实现对socks5或http协议的旁路代理，方便如Linux、PS5、Nintendo switch等不方便跑v2ray客户端的终端设备以及百度网盘、迅雷等需要设置网络代理的桌面端软件走代理，不需要开自己的电脑多一层旁代理。
4. 非校园网也可以参考使用，或直接使用v2rayN等客户端图形化实现，对于比较优秀的境外节点，可以直接代理NS等游戏机实现游戏加速。
5. 更新节点，支持订阅链接share.json-url或公开AES加密的url/单节点链接share.json-nodelink, 支持订阅-更新-自动合并(支持vmess和ss), 详情见merge.py
```


## 2.文件及部署说明
最新配置文件为**config.json**  
新机器部署时，只需放进去config.json，将订阅链接放入share.json，再运行merge.py即可
```
当境外节点失效时如何替换? 
# 1.用share.json中url字段的订阅链接（推荐）
python merge.py 0/1/2 #选择机场的第几个节点，支持ss和vmess
#若选用公开的AES加密过的url订阅 #pip3 install pycryptodome==3.14.1
wget xxx/v2rayconfig.tar
# tar cvf v2rayconfig.tar AES.py config.json merge.py readme.md share.json
tar xvf v2rayconfig.tar
python merge.py 0/1/2 passwd #passwd为最常用的组会房间号
# 2.更新share.json中nodelink的节点链接（需手动更新）
python merge.py
```
socks5代理监听端口为服务器的10808  
http代理监听端口为服务器的10809  

其他备份：  
.bak是只内网梯子（建议把block删掉或改direct，block表示局域网不允许访问）  
.double是内网kcp梯子+外网中转  
.ssdouble是内网ss梯子+外网中转  


## 3. 某航校园网内网梯子性能测评
性能测评如下图：

![](test.png)

## 参考
https://toutyrater.github.io/advanced/vps_relay.html
