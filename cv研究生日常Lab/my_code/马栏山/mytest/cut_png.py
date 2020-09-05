import os.path as osp
import glob,os
import cv2
import numpy as np

def cut(img,start_x,start_y,end_x,end_y):
    return img[start_y:end_y,start_x:end_x,:]

kernel_size=512
start_x =  1920//2 - kernel_size//2 
end_x = 1920//2 + kernel_size//2
start_y = 1080//2 - kernel_size//2 
end_y = 1080//2 + kernel_size//2
#####################

path1_index = "/media/x/Database/mls/dataset_png/val_damage"
to_path = "/media/x/Database/mls/dataset_png/val_damage_512"

path1 = sorted(glob.glob(osp.join(path1_index,"*")))
for path1_ii in path1:
    path1_name = path1_ii.split('/')[-1]
    to_path1 = osp.join(to_path,path1_name) #val_damage_512/mg00
    if not osp.exists(to_path1):
        os.system('mkdir '+to_path1)

    path2  = sorted(glob.glob(os.path.join(path1_ii,"*"))) #img paths #val_damage/mg00/000.png
    for path2_ii in path2:
        path2_name = path2_ii.split("/")[-1]
        ori_file_path = path2_ii
        wr_file_path = osp.join(to_path1,path2_name)#val_damage_512/mg00/000.png

        img = cv2.imread(ori_file_path, cv2.IMREAD_UNCHANGED)
        write_png_data = cut(img,start_x,start_y,end_x,end_y)
        cv2.imwrite(wr_file_path,write_png_data)
        
        print(wr_file_path)


