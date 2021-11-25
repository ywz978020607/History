MicroPython
WeAct_F411CE
重要：：
https://github.com/WeActTC/WeAct_F411CE.git

使用教程：
https://www.weact-tc.cn/2020/01/01/micropython/
https://www.weact-tc.cn/2019/11/30/STM32Download/

PA9 -接- RX
PA10 -接- TX



internal rom表示免焊接外置flash即可使用，推荐



烧录后  mpy的repl对应UART1，需要用串口连接，如果使用USB-HID等自动变为板载USB（UART6）

另：烧录后发现不用UART1接ttl模块，只用usb接电脑也可以进入repl



-----                              如何进入ISP模式                               -----

-----                                                                            -----
----- 方法1：上电状态下，按住BOOT0键和复位键，然后松开复位键，0.5秒后松开BOOT0键 -----
----- 方法2：掉电状态下，按住BOOT0键，上电后0.5S松开BOOT0                        -----





####

使用：板载user-key按键：a0,Pin.IN, PULL_UP  按下是低电平

C13 off 板载蓝灯亮