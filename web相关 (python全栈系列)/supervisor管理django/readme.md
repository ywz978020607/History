supervisor中放置此conf文件

/etc/supervisor/con.d/xxx.conf即可

具体看配置说明



tail -f -n 20 /xxx/xx.log 



# 配置注意

django-vue前端项目

运行对应的supervisor 某个端口 + nginx进行反代！！

在前端中将base_url改为 “/nginx_addr(/api/),(/test/)”