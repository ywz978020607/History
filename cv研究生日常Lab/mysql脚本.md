mysql -u root -p



#修改密码

set password = ‘123456’;



#创建数据库\用户

```
create DATABASE db1;
create user 'ywz'@'%' identified by 'password'; #也可以@'localhost'
grant all privileges on db1.* to 'ywz'@'%' with grant option; #db1的所有权限

FLUSH PRIVILEGES;
```