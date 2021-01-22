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