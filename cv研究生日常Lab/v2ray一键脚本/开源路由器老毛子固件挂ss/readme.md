参考

https://www.johntitorblog.com/?p=690

路由后台——扩展功能——shad***ks，**把开关打开**（这步别忘记，否则你后面怎么设置都没用）

新人需要仔细阅读下方ss设置方法，不仔细后悔！

## ss帐号填写&设置方法：

```
代理类型 选择ss

工作模式 根据需求选择，上网用途选gfwlist模式，游戏用途选大陆白名单模式

服务器地址 server字段冒号内的字符

服务器端口 server_port字段后面的数字

服务器密码 password字段冒号内的字符

加密方式 method字段冒号内的字符

代理转发的tcp端口 上网用途用默认的22,80,443即可；游戏用途需要改成1:65535（英文冒号）

游戏模式(udp转发) 酌情开启，开了未必游戏效果好

重定向DNS(chromecast支持) 需要开启

DNS服务模式 选择pdnsd代理
```

然后点击最下面的**应用本页面设置**即可启动ss，验证是否生效，继续往下看。

------

## 验证代理是否生效的方法

电脑浏览器访问http://www.google.com/ncr，能打开就表示ss生效。

如果电脑打不开，手机却特妈的可以打开，可能是由于电脑的dns不是[自动获取](https://www.baidu.com/baidu?wd=win10+dns改为自动获取&tn=monline_dg&ie=utf-8)所导致的，所以，看在上帝的份儿上请把[dns改为自动获取](https://www.baidu.com/baidu?wd=win10+dns改为自动获取&tn=monline_dg&ie=utf-8)，然后重启电脑。