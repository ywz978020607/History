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







