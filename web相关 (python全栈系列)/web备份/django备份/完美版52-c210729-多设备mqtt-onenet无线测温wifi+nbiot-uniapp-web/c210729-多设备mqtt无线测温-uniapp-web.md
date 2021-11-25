硬件功能： 红外模块/按键触发-- 非接触式测温iic读取--oled显示温度及时间--通过http/mqtt上传云端通过django后端保存到sqlite3数据库中，以及接收控制指令完成相应的操作。



软件功能：登录注册、超级管理员模块、绑定设备、设定阈值、邮件报警、查看最新数据、手动/自动控制远程硬件完成数据上下传。



方案一：esp32-wifi方案 -- 预计1000

主控芯片esp32，集成wifi

通信协议 http/mqtt-onenet

开发架构：uniapp + django + sqlite3 + onenet(如果使用mqtt)

客户端：web/小程序/app



方案二：stm32-nbiot方案 -- 预计1200

nbiot：bc35模块

通信协议 http + mqtt-onenet

开发架构：uniapp + django + sqlite3 + onenet -- mqtt相互订阅便于快速收发信号

客户端：web/小程序/app



注：功能没有完全细化，杜邦线原型机开发，价格仅供参考



--------------

mqtt-onenet账号

755720734  设备ID  755859674

234533  产品ID

2kJV69eUrcMgCLjkyOzT8k1WY0Y=    密钥




















