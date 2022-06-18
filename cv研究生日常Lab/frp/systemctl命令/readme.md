https://blog.csdn.net/x7418520/article/details/81077652?utm_medium=distribute.pc_relevant_t0.none-task-blog-OPENSEARCH-1.control&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-OPENSEARCH-1.control



# systemctl

sudo vim /lib/systemd/system/frps.service

```
[Unit]
Description=fraps service
After=network.target syslog.target
Wants=network.target

[Service]
Type=simple
#启动服务的命令（此处写你的frps的实际安装目录）
ExecStart=/your/path/frps -c /your/path/frps.ini

[Install]
WantedBy=multi-user.target
```



然后就启动frps
`sudo systemctl start frps`
再打开自启动
`sudo systemctl enable frps`

- 如果要重启应用，可以这样，`sudo systemctl restart frps`
- 如果要停止应用，可以输入，`sudo systemctl stop frps`
- 如果要查看应用的日志，可以输入，`sudo systemctl status frps`



# nohup

nohup xxx #不太推荐



# supervisor

见上一级目录