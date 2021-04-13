1. github注册仓库获得链接

2. 文件夹中打开bash

   git init

   git add -A

   git commit -m "up"

   git remote  add origin  https://github.com/ywz978020607/phddns_arm64_or_others_onenet.git

   git push origin master  # -f #强制push

------------------------

github使用本地翻墙socks代理

git config --global http.https://github.com.proxy socks5://127.0.0.1:10808

git config --global https.https://github.com.proxy socks5://127.0.0.1:10808



取消代理

git config --global --unset http.proxy 

git config --global --unset https.proxy  



查看已有配置

git config --global -l 