# 轻量轻依赖的桌面端嵌入工具类封装套壳框架
深度调研使用了tkinter，发现webview1/2难以兼顾隐藏任务栏/鼠标穿透功能，只用pyqt5不熟悉很难流畅设计，electron支持web套壳，也是之前一直用的方案，但打包体积也较大，特别是依赖多，离线安装不方便。

## pyqt5封装单页式vue文件套壳 clipweb.py
- clipweb.py: pyqt5主程序，实现了桌面嵌入、鼠标穿透、半透明组件、隐藏任务栏菜单栏、托盘图标、修改移动、加载本地/网络html显示
- config.json: 存放位置信息、模式、半透明度等数据
- ico.ico: 最小化托盘图标
- frontend: 前端相关 - frontend/index.html为加载对象，默认file协议
运行方式: python clipweb.py


## (可选)辅助使用python内置server - miniserver.py
通过http.server包，可以同时提供简易webapi后端功能以及静态文件服务器功能，将html文件以非本地读取(file协议)而是网络访问渲染(http)，结合后端server完成更加复杂的逻辑功能。

通过运行python miniserver.py 后，可微调clipweb.py中打开html方式改为http协议，并支持http.server写后端逻辑


## 打包
```
# pip install pyinstaller
pyi-makespec clipweb.py
pyinstaller -F -w 
```

