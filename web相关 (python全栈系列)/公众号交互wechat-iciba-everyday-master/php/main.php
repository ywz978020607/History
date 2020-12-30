<?php

// 引用类库
require_once "Iciba.php";

// 微信配置
$wechat_config = [
	'appid'			=>	'xxxxx', #(No.1)此处填写公众号的appid
	'appsecret'		=>	'xxxxx', #(No.2)此处填写公众号的appsecret
	'template_id'	=>	'xxxxx', #(No.3)此处填写公众号的模板消息ID
];

// 用户列表
$openids = [
	'xxxxx', #(No.4)此处填写你的微信号（微信公众平台上的微信号）
	#'xxxxx', #如果有多个用户也可以
];


// 实例化对象
$icb = new Iciba($wechat_config);

/* run()方法可以传入openids数组，也可不传参数
不传参数则对微信公众号的所有用户进行群发
*/
$icb->run();

