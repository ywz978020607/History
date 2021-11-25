import random
import csv
import math
import numpy as np
##file = 'c1_1.csv'
##fn = open(file,"w",newline = '')
##writer= csv.writer(fn)
out = []


#c.index(sorted(c)[2])
#参数
move = [20,33,46]
process = 560 #一道工序
change =[31,28] #上下料时间，偶，奇
clean = 25

product_num = 0

yingshe = {0:2,1:4,2:6,3:8,4:1,5:3,6:5,7:7}

#故障发生函数：
def guzhang():
    temptemp = random.randint(1,100)
    if temptemp == 1:
        return 1
    else:
        return 0
#故障数量
gz_num = 0
def weixiu():
    tempp = random.randint(10*60,20*60)
    return tempp

#计算移动时间：
def movetime(i,j):
    if i == j:
        return 0
    else:
##        print(i)
##        print(j)
        return move[int(math.fabs(i-j)-1)]

#当前位置 0 1 2 3
loc = 0

#消耗函数
def xiaohao(status,time):
    xiao = [0] * 8
    for i in range(8):
        if status[i] == 0 : # 空
            xiao[i] = movetime(loc,i%4) + change[int(i/4)]
        elif status[i] == 2:
            xiao[i] = movetime(loc,i%4) + change[int(i/4)] + clean
        #elif status[i] == 1:
           # xiao[i] = movetime(loc,i%4) + change[int(i/4)] + clean
        else:
            xiao[i] = 10000
    return xiao
# 得到消耗最小的机器编号
def get_least(xiao):
##    for i in range(len(xiao)):
##        if CNC_status[xiao.index(sorted(xiao)[0])]     
    return xiao.index(sorted(xiao)[0])



# 八个机器的状态码，0表示空，1表示正在加工，2表示呼叫抓手,3表示故障，4表示待上下料
CNC_status = [0]*8
# 八个机器的运行时间
CNC_time = [0] * 8
#八个机器的当前运行的工件编号
current_num = [0]*8
#总时间
alltime = 8*3600
#故障发生
breaktime = [0] *8
#回复时间
overtime = [0] *8
#等待时间
waittime = [0] *8

RGV_move = 0
RGV_time=0
RGV_work = 0

last_least = -1
last_work = -1
t = 0
#CNC 允许移动
move_CNC = 0
while t <= alltime:
##    print("loc:")
##    print(loc)
    #消耗最小的机器编号
    least = get_least(xiaohao(CNC_status,CNC_time))
##    print(least)
##    print(xiaohao(CNC_status,CNC_time))
#    print(loc)
    #如果需要移动,且未在工作和移动！！：
    if  loc != least % 4 and RGV_move == 0 and RGV_work == 0 and move_CNC == 1:
        #移动到对应位置
        target = least % 4
        delta_t = movetime(loc,target)
        RGV_time = t+delta_t
        RGV_move = 1
        last_least = least

    if RGV_move == 1 and t >= RGV_time:
        loc = last_least % 4
        RGV_move = 0  #停止移动
        move_CNC = 0
    if RGV_work ==1 and t>=RGV_time:
        RGV_work = 0
        CNC_status[last_work] = 1
        CNC_time[last_work] = 0

    if loc == least % 4 and move_CNC == 1:
        move_CNC = 0
#执行更替,一开始或呼叫状态时执行
    if move_CNC == 0 and RGV_work == 0 and RGV_move == 0 and loc == least % 4 and (CNC_status[least] == 2 or CNC_status[least] == 0):
        t0 = t
        #更替时间
        delta_t = change[int(least/4)]
        if CNC_status[least] == 2:
            delta_t += clean
            RGV_work = 1
            RGV_time = t + delta_t
            #完成的工作台
            print(least,end = ' : ')
            print("下料开始",end =',')
            print(t0,end = ',')
            #打印加工后的当前工件编号
            print(current_num[least])
            out[current_num[least]-1].append(t0)
            
        elif CNC_status[least] == 0:
            RGV_work = 1
            RGV_time = delta_t + t

        #放入新工件
        product_num += 1
        print(least,end = ' : ')
        print("上料开始",end=',')
        print(t0,end=',')
        print(product_num)
        out.append([yingshe[least],t0])


        
        current_num[least] = product_num
        last_work  = least
        
            
        #状态更新
        CNC_status[least] = 4 #等待上下料完成
        CNC_time[least] = 0
##
##        #计算故障
##        gz = guzhang()
##        if gz == 1:
##            #真正加工后的多久开始故障
##            breaktime[least] = random.randint(1,process) + t
##            gz_num += 1
##            overtime[least] = weixiu() +breaktime + t        
##                
##

    #如果完成
    for i in range(8):
        if CNC_time[i] >= process and CNC_status[i] == 1:
            CNC_status[i] = 2 #呼叫
            CNC_time[i] = process
           

    # 时间流逝
    for i in range(8):
        if CNC_status[i] == 1:
            CNC_time[i] += 1 
        if CNC_status[i] == 0 or CNC_status[i] == 2:
            waittime[i] += 1
            move_CNC = 1  #允许移动
    t += 1
##for i in range(len(out)):
##    if len(out[i]) == 3:
##        writer.writerow([i+1,out[i][0],out[i][1],out[i][2]])
##    else:
##        writer.writerow([i+1,out[i][0],out[i][1]])
##fn.close()
