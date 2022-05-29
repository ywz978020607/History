# 摸鱼大鸽-物理网项目docker运行--只需将代码拷贝进来再运行即可

# 使用方式
```
#将自己的django文件夹替换到django1内
#修改dev_start.sh #如果需要mqtt 请启动相应的注释
cd docker
#修改docker-compose.yml #ports
. env.sh
build
start
```

# docker-compose配置
## 1.无nginx
默认不启用nginx

## 2.启动nginx
需要对docker-compose.yml中取消nginx相关注释部分，并注释web的ports部分  
再到nginx/django.conf中查看或修改端口定义以符合自己要求  
目前是nginx(80)->django(容器依赖内部的8000端口，不开放到宿主机)