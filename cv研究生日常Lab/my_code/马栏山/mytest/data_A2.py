#处理test_A,调用EDVR模型，一条龙处理，5个func，可以单独调用 A2: 在func3中添加了边框黑色处理

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
                if list(img[temp][ii]) == [0,0,0,255]:
                    count +=1
            return count / len(img[temp])
        else:
            #左右,竖直一列看比例
            count = 0
            for ii in range(len(img)):
                if list(img[ii][temp]) == [0,0,0,255]:
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

def set_black(img,border):
    #包含边界border
    x1 = border[0]
    x2 = border[1]
    y1 = border[2]
    y2 = border[3]

    #上下黑边
    if  y1>=0:
        for ii in range(0,y1+1):
            img[ii][:] = [0,0,0,255]
    if y2 >= 0:
        for ii in range(y2,len(img)):
            img[ii][:] = [0, 0, 0, 255]

    #左右黑边
    if x1 >= 0:
        for ii in range(0,x1+1):
            for line_ii in range(len(img)):
                img[line_ii][ii] = [0,0,0,255]
    if x2 >= 0:
        for ii in range(x2, len(img[0])):
            for line_ii in range(len(img)):
                img[line_ii][ii] = [0, 0, 0, 255]

    return img
########################################


#0.y4m->png：dataset_y4m2png.py
#将y4m转为png，以备fusion训练,同时产出两个txt目录

def func0():
    dataset_path = "/media/x/Database/mls/dataset/"
    # data_list = glob.glob(join(dataset_path,"*"))
    data_list = [join(dataset_path,"test_damage_A")]

    png_path_index = "/media/x/Database/mls/dataset_png/"

    #######一个数据包一个文件夹
    # one_package = join(dataset_path,"val_ref_part1")  #in data_list = True 一个数据包 10G
    for one_package in data_list:
        print(one_package)

        #测试集不要
        # if "test" in one_package:
            # continue

        one_package_temp_name1 = one_package.split(dataset_path)[-1].strip("/") #文件夹名字

        #输出png，xxx/dataset_png/train_damage_part1/xxx(y4m_name)/001.png
        png_path_index1 = join(png_path_index,one_package_temp_name1)
        if not exists(png_path_index1):
            os.system("mkdir "+png_path_index1)
        
        y4m_list = sorted(glob.glob(join(one_package,"*")))
        for y4m_temp_path in y4m_list:
            print(y4m_temp_path)
            y4m_temp_name0 = y4m_temp_path.split(one_package)[-1].strip("/").split(".y4m")[0]
            png_path_index2 = join(png_path_index1,y4m_temp_name0)
            # print(png_path_index2)
            if not exists(png_path_index2):
                os.system("mkdir "+png_path_index2)
            #输出路径
            #只有damage存一次，防止重复
            png_path_index3 = png_path_index2
            # if "damage" in one_package:
            #     png_path_index3 = join(png_path_index2,"blur") #damage对应的png
            # else:
            #     png_path_index2 = png_path_index2.replace("ref","damage") #都存damage
                
            #     png_path_index3 = join(png_path_index2,"truth")
            # if not exists(png_path_index3):
            #     os.system("mkdir "+png_path_index3)
            print(png_path_index3)
            #输出png
            os.system("ffmpeg -i "+y4m_temp_path + " -vsync 0 "+ png_path_index3 +"/%4d.png -y")

#1.图像分割一般1920*1080-》1920*544 + 1920*544 =>只要第二张的最后360维度进行拼接
#将1920*1080转两份544文件夹*n (n为30份一大包，以免EDVR导致swap超标)

def func1():
    def cut(img,start_x,start_y,end_x,end_y):
        return img[start_y:end_y,start_x:end_x,:]
    
    path1_index = "/media/x/Database/mls/dataset_png/test_damage_A"
    to_path_list = ["/media/x/Database/mls/dataset_png/test_damage_A_1","/media/x/Database/mls/dataset_png/test_damage_A_2"]
    pixel_set=[[0,0,1920,544],[0,1080-544,1920,1080]]

    #swap会爆，每个再按30个视频分一次
    count_for_swap = 0
    count_for_swap_name = 0
    
    for ii in range(len(to_path_list)):
        count_for_swap = 0
        count_for_swap_name = 0

        path1 = sorted(glob.glob(osp.join(path1_index,"*")))
        for path1_ii in path1:
            count_for_swap += 1
            if count_for_swap >= 30:
                count_for_swap = 0
                count_for_swap_name += 1

            to_path = to_path_list[ii] + '_' + str(count_for_swap_name)

            if not osp.exists(to_path):
                os.system('mkdir '+to_path)

            path1_name = path1_ii.split('/')[-1]
            to_path1 = osp.join(to_path,path1_name) #val_damage_512/mg00
            if not osp.exists(to_path1):
                os.system('mkdir '+to_path1)

            path2  = sorted(glob.glob(os.path.join(path1_ii,"*"))) #img paths #val_damage/mg00/000.png
            for path2_ii in path2:
                path2_name = path2_ii.split("/")[-1]
                ori_file_path = path2_ii
                wr_file_path = osp.join(to_path1,path2_name)#val_damage_512/mg00/000.png

                print(wr_file_path)

                img = cv2.imread(ori_file_path, cv2.IMREAD_UNCHANGED)
                write_png_data = cut(img,pixel_set[ii][0],pixel_set[ii][1],pixel_set[ii][2],pixel_set[ii][3])
                cv2.imwrite(wr_file_path,write_png_data)

##2. EDVR 执行（两次，更改.yml对应的数据位置）
def func2():
    move_to_path = "/media/x/Database/mls/dataset_out"

    #A_x
    path1_list = ["A_1","A_2"]
    for ii in range(len(path1_list)):
        path1 = path1_list[ii]

        # path1 = "A_2"
        cmd = "python test_A.py -opt options/test/"+path1+"_0.yml"
        os.system(cmd)

        cmd = "python test_A.py -opt options/test/"+path1+"_1.yml"
        os.system(cmd)

        move_to_path1 = osp.join(move_to_path,path1)
        if not osp.exists(move_to_path1):
            os.system("mkdir "+move_to_path1)

        cmd = "mv  ~/mls_code_test/EDVR/results/EDVR/REDS4/* "+move_to_path1
        os.system(cmd)    
        
        ############################################

## 3.EDVR->合并png
def double_png_conver_one(img1,img2,final_y):
    #img数组索引是先y后x
    #y方向组合
    return np.concatenate((img1,img2[(len(img1)+len(img2)-final_y):]),axis=0)

def func3():
    path1 = "/media/x/Database/mls/dataset_out/A_1"
    path2 = "/media/x/Database/mls/dataset_out/A_2"
    
    to_path = "/media/x/Database/mls/dataset_out/test_A_1_2"
    if not osp.exists(to_path):
        os.system("mkdir "+to_path)

    ## 视频级
    path3_list = sorted(glob.glob(osp.join(path1,"*")))
    for ii in range(len(path3_list)):
        path3_name = path3_list[ii].split("/")[-1] #mg00
        
        from_path3 = path3_list[ii]
        from2_path3 = osp.join(path2,path3_name)  #test_A_1_2/mg00
        
        to_path3 = osp.join(to_path,path3_name)
        if not osp.exists(to_path3):
            os.system("mkdir "+to_path3)

        #图片级--files
        path4_list = sorted(glob.glob(osp.join(from_path3,"*")))
        for path4_ii in range(len(path4_list)):
            path4_name = path4_list[path4_ii].split("/")[-1] #xx.png
            
            from_path4 = path4_list[path4_ii]
            from2_path4 = osp.join(from2_path3,path4_name)
            
            to_path4 = osp.join(to_path3,path4_name) #xxxxxxx.png
            #合并输出
            img1 = cv2.imread(from_path4, cv2.IMREAD_UNCHANGED)
            img2 = cv2.imread(from2_path4, cv2.IMREAD_UNCHANGED)

            out_img = double_png_conver_one(img1,img2,1080)

            # ywz 可以加黑边处理 path4_ii==0时读取更新黑边，然后按此边界进行处理
            #每个视频第一帧 读取边界
            if path4_ii == 0:
                border = get_border(out_img,0.4)
            # 视频按照边界处理
            out_img = set_black(out_img,border)

            cv2.imwrite(to_path4,out_img)            
            

            print(to_path4)


## 4.png转y4m命名格式，准备上传
# ffmpeg -i xx%3d.bmp  -pix_fmt yuv420p  -vsync 0 xx.y4m -y
# 格式 mg_refine_xx.y4m
def func4():
    path1 = "/media/x/Database/mls/dataset_out/test_A_1_2"
    to_path1 = "/media/x/Database/mls/dataset_out/test_A_y4m"
    if not osp.exists(to_path1):
        os.system("mkdir "+to_path1)

    #视频级
    path2_list = sorted(glob.glob(osp.join(path1,"*")))
    for path2_ii in range(len(path2_list)):
        path2_name = path2_list[path2_ii].split('/')[-1] #mg_test_0800_damage
        path2 = path2_list[path2_ii]
        
        to_path2_name = path2_name.split("_")[-2] #0800
        to_path2_name = "mg_refine_"+to_path2_name+".y4m"
        to_path2 = osp.join(to_path1,to_path2_name)

        #图片转视频
        os.system("ffmpeg -i "+ path2+"/"+"%3d.png" +"  -pix_fmt yuv420p  -vsync 0 "+to_path2+" -y")

        print(to_path2)


################################################################

     
# func0()      # 0.y4m-》png   
# func1()     # 1.png——1080->544*2*n
# func2()   #EDVR and copy to media
# func3()   #convert one
# func4()   #png->y4m




