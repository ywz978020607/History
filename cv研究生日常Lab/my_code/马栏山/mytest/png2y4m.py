
import os.path as osp
import glob,os
import cv2
import numpy as np
from os.path import join,exists


## 4.png转y4m命名格式，准备上传
# ffmpeg -i xx%3d.bmp  -pix_fmt yuv420p  -vsync 0 xx.y4m -y
# 格式 mg_refine_xx.y4m
def func4():
    path1 = "./data/dataset_png/refine"
    to_path1 = "/data/output"
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

func4()   #png->y4m




