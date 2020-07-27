8266-01是指8针小模块
目前测试01版本ok
但01s不可以，文件系统无法使用！！


8266没有execfile函数，需要都在main函数里写！！

8266 deepsleep

import machine
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
# set RTC.ALARM0 to fire after 60 seconds (waking the device)
rtc.alarm(rtc.ALARM0, 60000)
# put the device to sleep
machine.deepsleep()
