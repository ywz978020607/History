# pySrun4k


## 自动监控重登改进版 见autorec.py（填入账号密码），用supervisor自动管理配置文件见pylogin.conf



## 简介

pySrun4k是一个模仿Srun4k认证客户端协议，用Python3实现的认证客户端。

实现了登录，检查在线状态，登出当前终端，登出所有终端功能。

## 依赖

request

```pip install request```

## API

### 登录

```srun4k.do_login(username,pwd,mbytes=0,minutes=0)```

### 检查在线状态

```srun4k.check_online()```

### 登出当前终端

```srun4k.do_logout(username)```

### 登出所有终端

```srun4k.force_logout(username,password)```

## Login.py

可以直接通过命令行调用

### 登录
```python Login.py login <username> <password>```

### 检查在线状态
```python Login.py check_online```

### 登出当前终端
```python Login.py logout <username>```

### 登出所有终端
```python Login.py logout_all <username> <password>```


