'''
MIT License

Copyright (c) 2019 lewis he

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

pcf8563_alarm.py - MicroPython library for NXP PCF8563 Real-time clock/calendar
Created by Lewis he on September 17, 2019.
github:https://github.com/lewisxhe/PCF8563_PythonLibrary
'''
import utime
import time
import pcf8563
from machine import I2C
from machine import Pin

def handle_interrupt(pin):
    if r.check_for_alarm_interrupt():
        print('is alarm clock interrupt')
    else:
        print('is not for alarm interrupt')
    r.clear_alarm()

irq = Pin(37, mode=Pin.IN,handler=handle_interrupt,trigger=Pin.IRQ_FALLING)
i2c = I2C(scl=22, sda=21)
r = pcf8563.PCF8563(i2c)

print('rtc time')
r.datetime()
time.sleep(1)

print('Clear alarm config register')
r.clear_alarm()

print('Setting current clock datetime')
r.write_all(50,30,15,3,17,9,49)

print('Set the alarm to match for minutes')
r.set_daily_alarm(minutes=31)

print('Enable rtc chip interrupt')
r.enable_alarm_interrupt()

while True:
    r.datetime()
    time.sleep(1)