# 重点项目
- docker_nginx_with_DjangoAuthUpload: 支持超管&上传开关&pipeline的nginx-docker，(普通nginx不支持上传
- docker_run_djangoweb: 物联网项目后端快速上云，将代码拷入后修改docker-compose外漏端口，由于前后端都是分离且可跨域的，不再重复构造nginx，前端文件即服务，也可共用nginx




django 测试 不重载：

python manage.py runserver 0.0.0.0:8000  --noreload