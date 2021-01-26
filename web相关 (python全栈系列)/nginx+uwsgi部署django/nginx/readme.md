/etc/nginx/site-enable/default 文件更改



如果有权限问题，记得将/etc/nginx/nginx.conf第一行用户组改为

##user www-data;
user root root;