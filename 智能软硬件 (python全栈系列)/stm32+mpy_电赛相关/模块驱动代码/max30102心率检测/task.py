import max30102
import hrcalc
from ssd1306_lib import SSD1306

#max30102模块初始化
m = max30102.MAX30102(pin='Y12')
#OLED显示屏初始化
display = SSD1306(pinout={'dc': 'X5',
                          'res': 'X4'},
                  height=64,
                  external_vcc=False)
state = False
#按键回调函数
def f():
    global state
    pyb.delay(10)          #消抖
    if sw():
        state = not state
        
#板载USR按键
sw = pyb.Switch()
sw.callback(f)
 
if __name__ == '__main__':
    display.poweron()       #启动模块
    display.init_display()  #初始化显示设置
    display.draw_image()    #根据字库绘制图片
    display.display()       #进行显示 
    pyb.delay(3000)
    while True:
        if state:
            display.draw_chinese('测量中',5,1)
            display.display()
            #采样250条数据，大约10秒钟
            red, ir = m.read_sequential(1000)
            #进行分析
            ir_avg = []
            red_avg = []
            for i in range(37):
                d = hrcalc.calc_hr_and_spo2(ir[25*i:25*i+100], red[25*i:25*i+100])
                #print(d)
                if d[1]:
                    ir_avg.append(d[0])
                if d[3]:
                    red_avg.append(d[2])
            ir_D = (sum(ir_avg) - max(ir_avg) - min(ir_avg)) // len(ir_avg)
            red_D = (sum(red_avg) - max(red_avg) - min(red_avg)) // len(red_avg)
            print('ir:',ir_D)
            print('red:',red_D)
            #将设定的区域清空
            #clear_area(x起始,y起始,x结束,y结束) 1个像素为1个单位
            display.clear_area(64,16,128,32)
            display.display()
            display.draw_text(85,16,str(ir_D),size=2)
            display.draw_chinese('次',5,2)
            display.draw_text(98,32,'/',size=2)
            display.draw_chinese('分',7,2)
            display.display()
            state = False


# #display.display()
# display.draw_chinese('次分',5,1)
# display.display()


# with open("red.log", "w") as f:
#     for r in red:
#         f.write("{0}\n".format(r))
# with open("ir.log", "w") as f:
#     for r in ir:
#         f.write("{0}\n".format(r))
# m.shutdown()
# red = []
# with open("red.log", "r") as f:
    # for r in f:
        # red.append(int(r))

# ir = []
# with open("ir.log", "r") as f:
    # for r in f:
        # ir.append(int(r))

# print('end')