当串口资源不够用，需要复用0号引脚时，才推荐使用webrepl

支持手动配网版（后续可以添加自动上传本地局域网ip到云onenet等）


#ap版 ws://192.168.4.1:8266   http://micropython.org/webrepl/ 提示：：需要用chrome浏览器才行
密码 micropythoN 
修改密码 
import network
ap= network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="micropython-xxx", authmode=network.AUTH_WPA_WPA2_PSK, password="micropythoN")

#简洁版 需要先在repl内输入import webrepl_setup，设置密码
import   webrepl
webrepl.start()

