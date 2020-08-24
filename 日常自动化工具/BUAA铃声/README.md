# BUAA 在家上课铃声脚本(win用户)



*在家上课，共克时艰，来点上课铃助助兴*



方法一、直接下载此exe，但是会报木马，添加信任即可（皮毛技术，毫无内涵）



方法二、 自己动手，生成脚本*（注：需python3环境且需安装playsound包、pyinstaller包）*

​	a. 安装py包

​		pip（pip3）安装playsound和pyinstaller即可



​	b. 输入代码本地测试，两个mp3文件放在同级目录，buaa_alert.py如下

```python
from playsound import playsound
import datetime
import time

open_time = ['08:00','08:50','09:50','10:40','14:00','14:50','15:50','16:40']
close_time = ['08:45','09:35','10:35','11:25','14:45','15:45','16:35','17:25']
last_time = '00:00'

while 1:
    try:
        temp_time = datetime.datetime.now().strftime('%H:%M')
        if temp_time != last_time:
            last_time = temp_time
            if temp_time in open_time:
                playsound('1.mp3')
            if temp_time in close_time:
                playsound('2.mp3')
    except:
        print("error")
        pass

    time.sleep(30) #30s
```



​	c. 使用pyintaller打包成单个exe

​		cmd命令行在同级目录输入

`		pyinstaller -F -w buaa_alert.py`

​		其中-F表示生成单个无依赖文件的exe程序，之后即可在同级目录下的dist文件夹中看到孤零零的exe文件，添加信任即可，此exe即可单独食用



- 双击exe运行后，自动后台运行不可见，打开任务管理器会看到对应的同名进程，可以手动结束。





## 最后祝早日在学校见到大家~