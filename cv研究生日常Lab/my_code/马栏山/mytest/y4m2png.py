
import os.path as osp
import glob,os
import cv2
import numpy as np
from os.path import join,exists


#0.y4m->png：dataset_y4m2png.py
#将y4m转为png，以备fusion训练,同时产出两个txt目录

def func0(dir_name = "test_damage_B"):
    dataset_path = "/data/"
    # data_list = glob.glob(join(dataset_path,"*"))
    data_list = [join(dataset_path,dir_name)]

    # ./data
    temp_own_index = "./data"
    if not osp.exists(temp_own_index):
        os.system("mkdir "+temp_own_index)

    png_path_index = "./data/dataset_png/"

    if not osp.exists(png_path_index):
        os.system("mkdir "+png_path_index)

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
            # ffmpeg -y -s 512x512 -i /home/sharklet/database/aftercut512_yuv/test/0.yuv /home/sharklet/database/aftercut512_yuv/test/%4d.png

################################################################
     
func0()      # 0.y4m-》png   




