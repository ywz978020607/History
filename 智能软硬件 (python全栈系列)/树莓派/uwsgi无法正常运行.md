sudo apt-get install uwsgi-plugin-python

后面加上python3的插件(或尝试python)

uwsgi -d log --ini /var/www/django1_nginx/uwsgi.ini  --plugin python3

或者在uwsgi.ini中加一行 plugin=python3即可



如果要自启动，注意uwsgi的完整路径