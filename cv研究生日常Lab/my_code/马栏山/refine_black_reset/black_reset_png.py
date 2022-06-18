import os.path as osp
import glob,os
import cv2
import numpy as np
from os.path import join,exists

########################################
# 获取黑边（包含）
def get_border(img,yuzhi): #纯黑在某一列/行比例

    def get_bili(img,temp,mode):
        if mode==0:
            count = 0
            for ii in range(len(img[temp])):
                if list(img[temp][ii]) == [0,0,0]:
                    count +=1
            return count / len(img[temp])
        else:
            #左右,竖直一列看比例
            count = 0
            for ii in range(len(img)):
                if list(img[ii][temp]) == [0,0,0]:
                    count +=1
            return count / len(img)

    x1 = 0
    x2 = len(img[0])-1
    y1 = 0
    y2 = len(img) -1

    #x1
    bili = get_bili(img,x1,1) #img,temp,mode（0=x，1=y）
    if bili>yuzhi:
        while bili>yuzhi:
            x1 +=1
            bili = get_bili(img,x1,1)
    else:
        x1 = -1

    # x2
    bili = get_bili(img, x2, 1)  # img,temp,mode（0=x，1=y）
    if bili > yuzhi:
        while bili > yuzhi:
            x2 -= 1
            bili = get_bili(img, x2, 1)
    else:
        x2 = -1

    # y1
    bili = get_bili(img, y1, 0)  # img,temp,mode（0=x，1=y）
    if bili > yuzhi:
        while bili > yuzhi:
            y1 += 1
            bili = get_bili(img, y1, 0)
    else:
        y1 = -1

    # y2
    bili = get_bili(img, y2, 0)  # img,temp,mode（0=x，1=y）
    if bili > yuzhi:
        while bili > yuzhi:
            y2 -= 1
            bili = get_bili(img, y2, 0)
    else:
        y2 = -1

    ###
    #退让x行/列
    waver_num = 3
    if x1>=0:
        x1 = (x1-waver_num) if (x1-waver_num)>=0 else 0
    if x2>=0:
        x2 = (x2+waver_num) if (x2+waver_num)<len(img[0]) else (len(img[0]) -1 )
    if y1 >= 0:
        y1 = (y1 - waver_num) if (y1 - waver_num) >= 0 else 0
    if y2 >= 0:
        y2 = (y2 + waver_num) if (y2 + waver_num) < len(img) else (len(img) - 1)

    return [x1,x2,y1,y2]


def get_border2(img,value=50): #有值大于50认为是边界
    #判断单点像素值
    def judge_value(img,temp,mode,value):
        #横看一行
        if mode == 0:
            for ii in range(len(img[temp])):
                if (img[temp][ii] > value).sum() > 0:
                    return True  # 是边界
        else:
            #左右,竖直一列看比例
            for ii in range(len(img)):
                if (img[ii][temp] > value).sum() > 0:
                    return True
        return False


    x1 = 0
    x2 = len(img[0])-1
    y1 = 0
    y2 = len(img) -1

    #x1
    # bili = get_bili(img,x1,1) #img,temp,mode（0=x，1=y）
    value_flag = judge_value(img,x1,1,value) #true表示是边界
    if  value_flag==False :
        while (value_flag==False):
            x1 +=1
            # bili = get_bili(img,x1,1)
            value_flag = judge_value(img, x1, 1, value)  # true表示是边界
    else:
        x1 = -1

    # x2
    # bili = get_bili(img, x2, 1)  # img,temp,mode（0=x，1=y）
    value_flag = judge_value(img, x2, 1, value)  # true表示是边界
    if  value_flag==False :
        while (value_flag==False):
            x2 -= 1
            # bili = get_bili(img, x2, 1)
            value_flag = judge_value(img, x2, 1, value)  # true表示是边界
    else:
        x2 = -1

    # y1
    # bili = get_bili(img, y1, 0)  # img,temp,mode（0=x，1=y）
    value_flag = judge_value(img, y1, 0, value)  # true表示是边界
    if  value_flag==False :
        while (value_flag==False):
            y1 += 1
            # bili = get_bili(img, y1, 0)
            value_flag = judge_value(img, y1, 0, value)  # true表示是边界
    else:
        y1 = -1

    # y2
    # bili = get_bili(img, y2, 0)  # img,temp,mode（0=x，1=y）
    value_flag = judge_value(img, y2, 0, value)  # true表示是边界
    if  value_flag==False :
        while (value_flag==False):
            y2 -= 1
            # bili = get_bili(img, y2, 0)
            value_flag = judge_value(img, y2, 0, value)  # true表示是边界
    else:
        y2 = -1

    ###
    #退让x行/列
    waver_num = 3
    if x1>=0:
        x1 = (x1-waver_num) if (x1-waver_num)>=0 else 0
    if x2>=0:
        x2 = (x2+waver_num) if (x2+waver_num)<len(img[0]) else (len(img[0]) -1 )
    if y1 >= 0:
        y1 = (y1 - waver_num) if (y1 - waver_num) >= 0 else 0
    if y2 >= 0:
        y2 = (y2 + waver_num) if (y2 + waver_num) < len(img) else (len(img) - 1)

    return [x1,x2,y1,y2]


def set_black(img,border):
    #包含边界border
    x1 = border[0]
    x2 = border[1]
    y1 = border[2]
    y2 = border[3]

    #上下黑边
    if  y1>=0:
        for ii in range(0,y1+1):
            img[ii][:] = [0,0,0]
    if y2 >= 0:
        for ii in range(y2,len(img)):
            img[ii][:] = [0, 0, 0]

    #左右黑边
    if x1 >= 0:
        for ii in range(0,x1+1):
            for line_ii in range(len(img)):
                img[line_ii][ii] = [0,0,0]
    if x2 >= 0:
        for ii in range(x2, len(img[0])):
            for line_ii in range(len(img)):
                img[line_ii][ii] = [0, 0, 0]

    return img
########################################


"""
demo
"""
if __name__ == "__main__":
    # img_path = "001.png"
    img_path = "mg_test_0888_damage/0002.png"
    img = cv2.imread(img_path) #, cv2.IMREAD_UNCHANGED) #maybe 4 channels
    # some images have 4 channels
    if img.shape[2] > 3:
        print("4 channels alert!")
        img = img[:, :, :3]

    #每个视频第一帧 读取边界
    # border = get_border(img,0.4)
    border = get_border2(img,50)
    # 视频按照边界处理
    img = set_black(img,border)

    img_out = img_path = "mg_test_0888_damage/out.png"
    cv2.imwrite(img_path,img)

    print("ok")

