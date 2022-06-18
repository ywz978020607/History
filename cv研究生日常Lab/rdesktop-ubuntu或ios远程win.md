win需要开启允许被远程控制

如果是ubuntu远程win，则win还要多一步：设置-搜远程-高级设置-将“需要计算机使用网络级别身份验证进行连接(建议)“的勾去掉



ubuntu连接脚本

rdesktop -u username -p password 10.136.xx.xx  -f

其中-f表示全屏沉浸式交互，体验优于向日葵，连接后通过ctrl+alt+enter退回ubuntu系统



若ios则安装RD Client 软件直接连接就好

