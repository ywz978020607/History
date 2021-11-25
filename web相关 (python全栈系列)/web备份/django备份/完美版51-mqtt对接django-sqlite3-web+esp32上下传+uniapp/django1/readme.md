# 基于Vue.js-Django-Sqlite前后端分离的免编译易迁移的认证+查表的网站开发

主要优点为不租云服务器时的网站开发方案

优点：

1. 适合小型网站快速开发
2. 适合内网穿透数量有限（花生壳）时，利用nginx静态+api转发，方便部署多个网站
3. 免配置数据库，利用文件类型数据库
4. 前端页面Vue.js双向绑定易改，免编译，如果需要nodejs编译成Vue工程，也方便迁移
5. Django后端自带session+前端cookie进行用户认证，保证基本安全
6. 前端纯静态页面可直接放在github.io建站，提高响应速度



# 配置注意

django-vue前端项目

conf文件见web备份/supervisor-django/

1. 运行对应的supervisor 某个端口 + nginx进行反代！！

2. 在前端中将base_url改为 “/nginx_addr(/api/),(/test/)” 其他一致