def connect():
    import network
    import time
    ssid = "pyb_test"
    password = "11111111"
    station = network.WLAN(network.STA_IF)
    for i in range(200):
        station.active(True)
        station.connect(ssid, password)
        time.sleep_ms(100)
        if station.isconnected() == True:
            return True, station.ifconfig()[0]
    return False, 0