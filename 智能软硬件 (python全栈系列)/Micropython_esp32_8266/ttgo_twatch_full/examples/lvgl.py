import lvgl as lv
import lvgl_helper as lv_h
import lvesp32
import display
import time
import machine
import touchscreen as ts
import axp202
import random

i2c0 = machine.I2C(scl=22, sda=21)
pmu = axp202.PMU(i2c0)
pmu.enablePower(axp202.AXP202_LDO2)
pmu.setLDO2Voltage(3300)
tft = display.TFT()

sda_pin = machine.Pin(23)
scl_pin = machine.Pin(32)

i2c = machine.I2C(id=1, scl=scl_pin, sda=sda_pin, speed=400000)
ts.init(i2c)

tft.init(tft.ST7789,width=240, invrot=3,rot=1,bgr=False, height=240, miso=2, mosi=19, clk=18, cs=5, dc=27,speed=40000000,color_bits=tft.COLOR_BITS16,backl_pin=12,backl_on=1)

tft.clear(tft.RED)
time.sleep(1)
tft.clear(tft.GREEN)
time.sleep(1)
tft.clear(tft.BLUE)
time.sleep(1)

lv.init()
disp_buf1 = lv.disp_buf_t()
buf1_1 = bytes(240*10)
lv.disp_buf_init(disp_buf1,buf1_1, None, len(buf1_1)//4)
disp_drv = lv.disp_drv_t()
lv.disp_drv_init(disp_drv)
disp_drv.buffer = disp_buf1
disp_drv.flush_cb = lv_h.flush
disp_drv.hor_res = 240
disp_drv.ver_res = 240
lv.disp_drv_register(disp_drv)

indev_drv = lv.indev_drv_t()
lv.indev_drv_init(indev_drv) 
indev_drv.type = lv.INDEV_TYPE.POINTER
indev_drv.read_cb = lv_h.read
lv.indev_drv_register(indev_drv)


scr = lv.obj()
btn = lv.btn(scr)
btn.align(lv.scr_act(), lv.ALIGN.CENTER, 0, 0)
label = lv.label(btn)
label.set_text("Button")
lv.scr_load(scr)

#! If you import lvesp32 you don't need
'''
while True:
    tim = time.ticks_ms()
    lv.tick_inc(5)
    lv.task_handler()
    while time.ticks_ms()-tim < 0.005:
        pass
'''