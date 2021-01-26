# Nginx+uwsgi+django(.sock)+local.ini (Linux)

- 实现nginx部署
- 文件拖拽、选择上传
- 静态文件服务器显示
- 一次性跨设备留言板
- 简易静态网站展示
- 本地ini数据文件作简易数据库
- 方便易部署



食用方法：如果遇到文件夹权限问题，记得`sudo chmod -R 777 目录名`

1. ` sudo apt install nginx`
2. var_www目录下东西放在ubuntu的 `/var/www/`
3. 按照nginx目录的readme配置nginx，重启`sudo service nginx restart`
4. 安装django相应服务

```
pip install django==2.2.0 -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install django-cors-headers -i https://pypi.tuna.tsinghua.edu.cn/simple/

###
# anaconda3环境下安装uwsgi参考（推荐！）
https://blog.csdn.net/xiefeisd/article/details/89486934
https://www.cnblogs.com/jiaxiaoxin/p/10642263.html
conda install -c conda-forge uwsgi 
conda install -c conda-forge libiconv

#也可以安装apt版本uwsgi，详见uwsgi.ini配置中说明
apt install uwsgi
apt install uwsgi-plugin-python3

#或pip版
pip install uwsgi -i https://pypi.tuna.tsinghua.edu.cn/simple/
#如果报错，可以降低gcc版本
```

5. 最终部署为两步
   - ` uwsgi -d --ini /var/www/django1_nginx/uwsgi.ini` 
   - （重启为uwsgi --reload /var/www/django1_nginx/uwsgi.ini, 停止为uwsgi --stop ...略)
   - sudo service nginx start（开机默认启动）
6. 开机自启动
   - 由于nginx自启动，所以配置uwsgi即可，一般在/etc/rc.local中添加即可
   - ` uwsgi -d --ini /var/www/django1_nginx/uwsgi.ini` 
   - 非root安装环境：
     - `su - user1 -c "/home/user1/anaconda3/bin/uwsgi -d --ini /var/www/django1_nginx/uwsgi.ini" `



