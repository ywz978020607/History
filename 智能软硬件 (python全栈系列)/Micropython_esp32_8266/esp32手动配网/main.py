import wifimgr

wlan = wifimgr.get_connection()
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  # you shall not pass :D

# Main Code goes here, wlan is a working network.WLAN(STA_IF) instance.
print("ESP OK")



################


##手机打开浏览器 输入192.168.4.1
import wifimgr
wlan = wifimgr.get_connection()