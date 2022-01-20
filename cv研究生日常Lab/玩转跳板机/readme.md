# 跳板机之便捷管理所有远程内网机器-ssh&scp

## 1. vscode版配置
见[config](./config)，将vscode的远程配置进行参考修改，再远程即可  

## 2. 类linux-命令行版配置
见[env.sh](./env.sh)  
使用方法`. env.sh` 或 `. env.sh nojump/1/2/3`  然后输入相应指令即可，以跳板机-ssh为例:`s518` 如果scp推荐使用`mapping $ip518 (22) 9050`将远程ip映射到本机自定义端口，具体ip请根据各自情况修改配置  
兼容IPAD/IOS-iSH软件(Alphine系统)，安卓-AidLux/Termux，以及WIN-WSL，MACOS等  


## 3. mobaxterm-配置-仅限win用户
### 3.1端口映射  
<img src=".img/chuantou.png" style="zoom:50%;" /><br>  
原理参考env.sh中端口映射mapping函数，改为图形化操作：将本地端口映射到远程内网机ip+端口  

### 3.2跳板机代理ssh  
原理参考env.sh中跳板机代理ssh，改为图形化操作：编辑Session-正常填写host和用户名、端口(默认22). 填写完成后再填写跳板机配置: 下方Network Settings-Connect through ssh gateway-填入跳板机ssh映射的公网ip和端口号以及跳板机的随意一个账号即可

<br>
<br>
<br>
<br>


# [多开发/执行机器协同开发git管理参考](../中心化多机器开发推荐配置.md)