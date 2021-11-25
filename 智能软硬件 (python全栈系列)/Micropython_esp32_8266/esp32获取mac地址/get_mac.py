import network
sta_if = network.WLAN(network.STA_IF)
s = sta_if.config('mac')
mymac = ('%02x%02x%02x%02x%02x%02x') %(s[0],s[1],s[2],s[3],s[4],s[5])
