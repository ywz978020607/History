# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import mywifi
mywifi.WIFI()

import webrepl
webrepl.start()
