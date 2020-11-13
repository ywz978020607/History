import random
import csv
import math
import numpy as np
file = 'c1_1.csv'
file2 = 'guzhang.csv'
fn = open(file,"w",newline = '')
fn2 = open(file2,'w',newline = '')
writer= csv.writer(fn)
writer2 = csv.writer(fn2)
out = []
out_guzhang = {}
#参数
move = [20,33,46]
process = [400,378] #工序
change =[31,28] #上下料时间，偶，奇  （上排，下排）
clean = 25

yingshe = {0:2,1:4,2:6,3:8,4:1,5:3,6:5,7:7}

#故障发生函数：
def guzhang():
    temptemp = random.randint(1,100)
##    if temptemp == 1:
##        return 1
##    else:
##        return 0
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

#两轮消耗函数
def xiaohao(c1,c2,status,time):
    zuhe = {}
    for i in range(len(c1)):
        for j in range(len(c2)):
            temp = 0
            if status[c1[i]] == 0 or status[c1[i]] == 2:
                temp +=movetime(loc,c1[i]%4) + change[int(c1[i]/4)]
            elif status[c1[i]] == 1:
                #一道工序 process
                temp += max(movetime(loc,c1[i]%4),process[0] - time[c1[i]]) + change[int(c1[i]/4)]
            else:
                temp += 10000
                
#只有一不为空才考虑后续的消耗：
            if status[c1[i]] != 0:
                # && j对应的消耗
                if status[c2[j]] == 0 :#空
                    temp +=movetime(loc,c2[j]%4) + change[int(c2[j]/4)]
                elif status[c2[j]] == 2:
                    temp +=movetime(loc,c2[j]%4) + change[int(c2[j]/4)] + clean
                elif status[c2[j]] == 1:
                    #二道工序 process
                    temp += max(movetime(loc,c2[j]%4),process[1] - time[c2[j]]) + change[int(c2[j]/4)]
                else:
                    temp += 10000
            zuhe[c1[i],c2[j]] = temp
    return zuhe
def get_least(zidian):
    c = sorted(zidian.items(),key = lambda item:item[1])[0][0][0]
    d = sorted(zidian.items(),key = lambda item:item[1])[0][0][1]
    return [c,d]  #第一步机器，第二步机器

# 第二道故障，第一道重新寻路：
def ercichazhao(loc,c2,status,time):
    xiao = [0] * len(c2)
    for i in range(len(c2)):
        if status[c2[i]] == 0 : # 空
            xiao[i] = movetime(loc,c2[i]%4) + change[int(c2[i]/4)]
        ####新更新！lastday
        elif status[c2[i]] == 2:
            xiao[i] = movetime(loc,c2[i]%4) + change[int(c2[i]/4)] + clean
        elif status[c2[i]] == 1:
            #二道工序 process
            xiao[i] = max(movetime(loc,c2[i]%4),process[1] - time[c2[i]]) + change[int(c2[i]/4)] + clean
        else:
            xiao[i] = 10000
        
    return c2[xiao.index(sorted(xiao)[0])]


#当前位置 0 1 2 3
loc = 0


ceshizongshu = 0
#一二道工序机器的编号
CNC1 = [1,4,6,7]
CNC2 = [0,2,3,5]

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
#是否有故障
breakflag = [0] * 8

gz_time = [0] * 8

RGV_move = 0
RGV_time=0
RGV_work = 0
RGV_curnum = -1
xialiao = 0
#add,未修改
last_least = -1
last_least2 = -1
last_work = -1
last_work2 = -1
jiuyuan = -1
product_num = 0
t = 0
RGV_status = 0
while t <= alltime:
    #故障处理
    for i in range(8):
        if breakflag[i] == 1 and t >= breaktime[i] and t < overtime[i] and CNC_status[i] == 1:    #加工状态故障
            CNC_status[i] = 3  #故障状态
            print("故障",end= ' :')
            print(i,end=',')
            print(current_num[i],end=',')
            print(t)
            out_guzhang[current_num[i]] = [current_num[i],yingshe[i],t]
            if last_least == i:
                RGV_status = 0
            
        elif breakflag[i] == 1 and t >= overtime[i] and CNC_status[i] == 3:
            CNC_status[i] = 0 #修复后，工件作废！！
            CNC_time[i] = 0
            breakflag[i] = 0
            print("故障修复",end=':')
            print(current_num[i],end=',')
            print(t)
            out_guzhang[current_num[i]].append(t)
    

    
    if RGV_status == 0 or RGV_status == 4:
        #消耗最小的机器编号
        path = get_least(xiaohao(CNC1,CNC2,CNC_status,CNC_time))
        least1 = path[0]
        least2 = path[1]   #第二道的下家 
        least = least1
        jiuyuan = least%4 
        RGV_status = 1 #去执行1道工序
##        print(xiaohao(CNC1,CNC2,CNC_status,CNC_time))
    #第一部分执行完毕
    elif RGV_status == 2:
        #二次重新查找
        least = ercichazhao(jiuyuan,CNC2,CNC_status,CNC_time)
        RGV_status += 1
        
    
#    print(loc)

    #如果需要移动,且未在工作和移动！！：
    if  loc != least % 4 and RGV_move == 0 and RGV_work == 0:
        #移动到对应位置
        target = least % 4
        delta_t = movetime(loc,target)
        RGV_time = t+delta_t
        RGV_move = 1
        last_least = least
        last_least2 = least2
    if RGV_move == 1 and t >= RGV_time:
        loc = last_least % 4
        RGV_move = 0  #停止移动

    #上下料结束
    if RGV_work ==1 and t>=RGV_time:
        RGV_work = 0
        CNC_status[last_work] = 1
        CNC_time[last_work] = 0
        RGV_status += 1
        if xialiao == 0:
            RGV_status = 0






    #执行更替,一开始或呼叫状态时执行,RGV_status = 1/3
    if (RGV_status ==1 or RGV_status == 3) and RGV_work == 0 and RGV_move == 0 and loc == least % 4 and (CNC_status[least] == 2 or CNC_status[least] == 0):
        t0 = t
        #更替时间
        delta_t = change[int(least/4)]
#################################################################
        if RGV_status == 1:

            if CNC_status[least] == 2 :
                #完成的工作台
##                print(least,end = ' : ')
##                print("下料开始",end =',')
##                print(t0,end = ',')
##                #打印加工后的当前工件编号
##                print(current_num[least])

                #是否拿到半成品
                xialiao = 1
                RGV_curnum = current_num[least]

                out[current_num[least]-1].append(t)            

            #未拿到半成品
            else:
                xialiao = 0

        #放入新工件
            product_num += 1
            ceshizongshu += 1
##            print(least,end = ' : ')
##            print("上料开始",end=',')
##            print(t0,end=',')
##            print(product_num)
            
        #第一道工序的故障初始化
            breakflag[least] = guzhang()
            if breakflag[least] == 1:
                breaktime[least] = t + random.randint(1,process[0]) + change[0]
                overtime[least] =  breaktime[least] + weixiu()


            
            current_num[least] = product_num

            out.append([product_num,yingshe[least],t])  #真正的cnc
            #状态更新
            CNC_status[least] = 4 #等待上下料完成
            CNC_time[least] = 0
            RGV_work = 1                      ##
            RGV_time = delta_t + t            ##
#############################################################

        elif RGV_status == 3:
            
            #假设只有第二道结束后要清洗
            if CNC_status[least] == 2:  #有第一道的成品也不一定有第二次下料，单独判断！
                
                delta_t += clean
                RGV_work = 1
                RGV_time = t + delta_t
                #完成的工作台
##                print(least,end = ' : ')
##                print("第二次下料开始",end =',')
##                print(t0,end = ',')
##                #打印加工后的当前工件编号
##                print(current_num[least])

                out[current_num[least]-1].append(t)
                    
            if xialiao == 1: #有第一道的成品
                xialiao = 0
                
                current_num[least] = RGV_curnum

                out[current_num[least]-1].append(yingshe[least])  #真正的cnc
                out[current_num[least]-1].append(t)
                

##                print(least,end = ' : ')
##                print("第二次上料开始",end=',')
##                print(t0,end=',')
##                print(current_num[least])


                
                #状态更新
                CNC_status[least] = 4 #等待上下料完成
                CNC_time[least] = 0
                RGV_work = 1
                RGV_time = t + delta_t
                
                #第二道工序的故障初始化,前提：有第一道的半成品
                breakflag[least] = guzhang()
                if breakflag[least] == 1:
                    breaktime[least] = t + random.randint(1,process[1]) + change[1]
                    overtime[least] =  breaktime[least] + weixiu()
 
                
            #重新找第一道工序
            else:        
                RGV_status = 0
        #current_num[least] = product_num
###############################################################################
                
        last_work  = least
        
            

        

    #如果完成
    for i in range(8):
        if i in CNC1:
            if CNC_time[i] >= process[0] and CNC_status[i] == 1:
                CNC_status[i] = 2 #呼叫
                CNC_time[i] = process[0]
        #二道工序
        if i in CNC2:
            if CNC_time[i] >= process[1] and CNC_status[i] == 1:
                CNC_status[i] = 2 #呼叫
                CNC_time[i] = process[1]
                          
    # 时间流逝
    for i in range(8):
        if CNC_status[i] == 1:
            CNC_time[i] += 1 
        if CNC_status[i] == 0 or CNC_status[i] == 2:
            waittime[i] += 1
        if CNC_status[i] == 3:
            gz_time[i] += 1

    t += 1

for i in range(len(out)):
    if len(out[i]) == 7:
        writer.writerow([out[i][0],out[i][1],out[i][2],out[i][3],out[i][4],out[i][5],out[i][6]])
for i in range(len(out_guzhang.items())):
    writer2.writerow(list(out_guzhang.items())[i][1])
fn.close()
fn2.close()

