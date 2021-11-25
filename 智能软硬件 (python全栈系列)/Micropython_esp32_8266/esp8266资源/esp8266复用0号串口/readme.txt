8266串口资源0号常用于repl，1号仅TX可以用，rx用于连接flash chip
UART0:UART0 is on Pins 1 (TX) and 3 (RX)
UART1 is on Pins 2 (TX) and 8 (RX) however Pin 8 is used to connect the flash chip, so UART1 is TX only.

而0号串口如果使用需要花式使用
详见 https://docs.micropython.org/en/latest/esp8266/quickref.html#

建议搭配webrepl使用
详见webrepl、8266复用0号串口和826-01-mpy/复用0号串口文件夹


To detach the REPL from UART0, use:

import uos
uos.dupterm(None, 1)
The REPL is attached by default. If you have detached it, to reattach it use:

import uos, machine
uart = machine.UART(0, 115200)
uos.dupterm(uart, 1)