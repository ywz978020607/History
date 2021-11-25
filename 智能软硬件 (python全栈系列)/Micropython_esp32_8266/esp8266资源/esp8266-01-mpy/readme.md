8266-01是指8针小模块
目前测试01版本ok
但01s不可以，文件系统无法使用！！

#注意
除了配套的继电器模块，如果要单独使用，需要注意几点
1.电源3.3V
2.EN拉高进入工作
3.启动时GPIO0&2或者悬空，或者拉高进入工作，[0低2高]是烧录模式。这一点如果使用自己的继电器要注意，记得拉高，不然启动后不正常工作。拉高阻值4.7k/10kΩ

8266没有execfile函数，需要都在main函数里写！！

8266 deepsleep

import machine
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
# set RTC.ALARM0 to fire after 60 seconds (waking the device)
rtc.alarm(rtc.ALARM0, 60000)
# put the device to sleep
machine.deepsleep()
