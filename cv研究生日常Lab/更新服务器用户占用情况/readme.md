# nvidia-smi命令升级版，查看当前服务器使用情况（个人版）

```
watch -n 2 python sys_user.py  #每两秒自动刷新显示

# 输出样式eg:
============================
CPU:96.2%       MEM:88.6%
============================
0       17313MiB / 24268MiB
1       16075MiB / 24268MiB
2       11276MiB / 24268MiB
3       23341MiB / 24265MiB
============================
============================
0:
        wsj--2187MiB
        lep--15113MiB
----------------------------
1:
        fyb--947MiB
        lep--15115MiB
----------------------------
2:
        XJY--11263MiB
----------------------------
3:
        wsj--23105MiB
----------------------------

```

# 监控显卡情况并发送邮件提醒（个人版）
```
# 安装email包   pip install PyEmail
# 执行demo
# python watch_alert.py 4.5 ywzsunny@buaa.edu.cn all  # 阈值/G 邮箱 监控显卡
```

# 监控命令结束后发送通知（脚本同上）
```
#可嵌入任何脚本结束
# [python xxx(你的脚本) ]   && python -c "from watch_alert import alert; alert('978020607@qq.com')"
```


# 集群逐个配置保存文件&nginx反代，一次性查看所有服务器的情况（运维版）

default: nginx配置文件

*.conf: supervisor配置文件

get_user.py：放置对应目录下待执行

*.html: /var/www/html目录下 （先清空html目录）



==========================================

搭配nginx--autoindex on以及supervisor自启动食用~



status.html 读取txt自动刷新显示 (需要nginx等才能测试)



一看多的话，需要跨域访问: 

#nginx autoindex on; 后面+

add_header Access-Control-Allow-Origin *;
add_header Access-Control-Allow-Credentials true;







