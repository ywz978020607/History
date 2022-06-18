# 设置欢迎界面

60-mywelcome

/etc/update-motd.d

权限 755 



# 设置每个用户连接时候的脚本

~/.profile



# .bashrc不自动执行

如果每次需要手动source ~/.bashrc

则新建文件 vim ~/.bash_profile

```bash
if test -f .bashrc ; then
source .bashrc 
fi
```

保存即可



# 定时关机

vim /etc/crontab

假设 要每天的22点定时关机 命令如下

00 22 * * *  root    /sbin/shutdown -h now

#55 23 * * * root /sbin/shutdown -r 08:00 #实现23:00定时关机且8:00定时开机

