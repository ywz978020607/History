
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl

# # 手动配网版
import network
##手机打开浏览器 输入192.168.4.1
import wifimgr
wlan = wifimgr.get_connection()

sta_if = network.WLAN(network.STA_IF)
print("network config:", sta_if.ifconfig())

webrepl.start()
gc.collect()

