#esp32
from espmax30102 import *
import hrcalc

m = MAX30102()


def test(m):
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
