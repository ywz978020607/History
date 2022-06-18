# ssh-双向代理使用说明

参考 https://zhuanlan.zhihu.com/p/57630633

## 1. 正向代理 -L

正向代理可能是最需要的一种，在解决了内网穿透问题后，我们常常需要查看其他非22端口的内容，比如在使用tensorboardX等调试网页时，通过正向代理(跳板机)，我们可以将可以ssh链接到的网络中任意一台电脑的任意一个端口映射到本机的某个端口，最后在本机浏览器输入**http://localhost:xxxx/**即可访问。

用法1：远程端口映射到其他机器 （两台机）--前提是B(本机)能通过ssh连接到C机，即需要C机的内网/外网ip地址

HostB 上启动一个 PortB 端口，映射到 HostC:PortC 上，在 HostB 上运行：

```bash
HostB$ ssh -L 0.0.0.0:PortB:HostC:PortC user@HostC
```

这时访问 HostB:PortB 相当于访问 HostC:PortC。

如果本机B连接C的ssh对应不是22端口(如内网穿透等) 则需要在最后面加 -p xx （其中xx为端口号）

eg :    ```ssh -L 127.0.0.1:8008:127.0.0.1:6006 user@frp0.buaamc2.net -p 3000``` 

其中127.0.0.1:8008是本机B对应的ip端口，127.0.0.1:6006是远端要转发的C机对自己的ip+端口，user是用户名，frp0.buaamc2.net和-p 3000可以换成对应B--(ssh)->C机远程对应的ip/域名和端口(默认22)



用法2：本地端口通过跳板映射到其他机器 （跳板机） --前提是A(本机)能通过ssh连接到B机，即需要B机的内网/外网ip地址 + B能够直接访问HostC:PortC

HostA 上启动一个 PortA 端口，通过 HostB 转发到 HostC:PortC上，在 HostA 上运行：

```bash
HostA$ ssh -L 0.0.0.0:PortA:HostC:PortC  user@HostB
```

这时访问 HostA:PortA 相当于访问 HostC:PortC。

两种用法的区别是，第一种用法本地到跳板机 HostB 的数据是明文的，而第二种用法一般本地就是 HostA，访问本地的 PortA，数据被 ssh 加密传输给 HostB 又转发给 HostC:PortC。



## 2. 反向代理 -R

此处所说的反向代理可以理解为内网穿透功能，ssh的反向代理不太稳定，尽量用frp实现的更加可靠的内网穿透或使用autossh

autossh -R 可以作为临时的反向代理操作，比如校内机器没有分配到10网段的ip时，可以穿透到校内服务器上实现校内快速访问，如将本机的22转发到校内402服务器ip对应的6600端口：

autossh -R 10.130.159.225:6600:127.0.0.1:22 ywz@10.130.159.225  

添加 -f 参数可以后台运行

（10.130.159.225（host C）机器需要更改/etc/ssh/sshd_config 添加GatewayPorts yes）

## 3. SS/SSR -D

ssh也可进行sock5转发代理，实现科学上网，这种方法不太可靠，也不再叙述



## - 补充

可以通过安装使用 autossh 代替 ssh命令， 实现自动重连。