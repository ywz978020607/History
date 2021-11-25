# import network,webrepl
# sta_if = network.WLAN(network.STA_IF)
# if not sta_if.isconnected():
#     print("connecting to network...")
#     sta_if.active(True)
#     sta_if.connect("<ap_name>", "<password>") # Connect to an AP <ap_name>&<password> is your route name&password
#     while not sta_if.isconnected(): # Check for successful connection
#         pass
# print("network config:", sta_if.ifconfig())
# webrepl.start()

# # 手动配网版
# import network,webrepl
# ##手机打开浏览器 输入192.168.4.1
# import wifimgr
# wlan = wifimgr.get_connection()

# sta_if = network.WLAN(network.STA_IF)
# print("network config:", sta_if.ifconfig())
# webrepl.start()

#######################################################
##ap版
#简洁版 需要先在repl内输入import webrepl_setup，设置密码
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
webrepl.start()
gc.collect()

