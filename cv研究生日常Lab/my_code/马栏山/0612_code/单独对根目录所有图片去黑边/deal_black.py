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


#图片目录
def func_black():
    dir_path = "refine"  # test/mg00/001.png
    out_path = "refine2"
    if not os.path.exists(out_path):
        os.system("mkdir " + out_path)

    path1_list = sorted(glob.glob(osp.join(dir_path,"*")))
    for path1_ii in range(len(path1_list)):
        path1_temp = path1_list[path1_ii]
        path1_out = path1_temp.replace(dir_path, out_path, 1)
        if not os.path.exists(path1_out):
            os.system("mkdir " + path1_out)

        #png list
        path2_list = sorted(glob.glob(osp.join(path1_temp,"*")))
        for path2_ii in range(len(path2_list)):
            path2_temp = path2_list[path2_ii]

            img = cv2.imread(path2_temp) #, cv2.IMREAD_UNCHANGED)
            # some images have 4 channels
            if img.shape[2] > 3:
                img = img[:, :, :3]

            #每一帧都读
            border = get_border2(img, 50)

            # 视频按照边界处理
            img = set_black(img,border)
            out_img_path = path2_temp.replace(dir_path,out_path,1) #开头替换

            cv2.imwrite(out_img_path,img)
            print(out_img_path)

##############################################################################


# 每一个视频读取npy文件，加载每一帧的border
def func_black_npy():
    npy_index = "/home/xql/projects/mls/dataset_png/border_test_damage_B"  #npy_index/mg00.npy
    #网络输出 refine
    dir_path = "/home/xql/projects/mls/dataset_png/refine/0611"  # test/mg00/001.png
    #去黑边输出 refine2
    out_path = "/home/xql/projects/mls/dataset_png/refine/0611_black"
    if not os.path.exists(out_path):
        os.system("mkdir " + out_path)

    path1_list = sorted(glob.glob(osp.join(dir_path,"*")))
    for path1_ii in range(len(path1_list)):
        path1_temp = path1_list[path1_ii]
        #加载当前视频所有border
        path1_name = os.path.split(path1_temp)[-1].replace("refine","test") #mg00

        npy_path = osp.join(npy_index, path1_name) + "_damage" + '.npy'
        video_border = np.load(npy_path)

        path1_out = path1_temp.replace(dir_path, out_path, 1)
        if not os.path.exists(path1_out):
            os.system("mkdir " + path1_out)
        print(path1_out)

        #png list
        path2_list = sorted(glob.glob(osp.join(path1_temp,"*")))
        for path2_ii in range(len(path2_list)):
            path2_temp = path2_list[path2_ii]

            img = cv2.imread(path2_temp) #, cv2.IMREAD_UNCHANGED)
            # some images have 4 channels
            if img.shape[2] > 3:
                img = img[:, :, :3]

            #每一帧都读
            # border = get_border2(img, 50)
            border = video_border[path2_ii]

            # 视频按照边界处理
            img = set_black(img,border)
            out_img_path = path2_temp.replace(dir_path,out_path,1) #开头替换

            cv2.imwrite(out_img_path,img)
            print(out_img_path)



# 测试每帧border，按视频存入npy文件
def func_save_border():
    dir_path = "/home/xql/projects/mls/dataset_png/test_damage_B"  # dir_path/mg00/001.png
    out_npy_path = "/home/xql/projects/mls/dataset_png/border_test_damage_B"
    if not os.path.exists(out_npy_path):
        os.system("mkdir "+out_npy_path)

    path1_list = sorted(glob.glob(osp.join(dir_path,"*")))
    for path1_ii in range(len(path1_list)):
        path1_temp = path1_list[path1_ii]
        path1_name = os.path.split(path1_temp)[-1] #mg00

        npy_path = osp.join(out_npy_path,path1_name) + ".npy"
        video_border = []

        #png list
        path2_list = sorted(glob.glob(osp.join(path1_temp,"*")))
        for path2_ii in range(len(path2_list)):
            path2_temp = path2_list[path2_ii]

            img = cv2.imread(path2_temp) #, cv2.IMREAD_UNCHANGED)
            # some images have 4 channels
            if img.shape[2] > 3:
                img = img[:, :, :3]

            #每一帧都读
            border = get_border2(img, 50)
            video_border.append(border)
            print(path2_ii)

        video_border = np.array(video_border)
        #保存
        np.save(npy_path,video_border)
        print(npy_path)

if __name__ == "__main__":
    # func_black()
    # func_save_border()
    func_black_npy()
    pass

