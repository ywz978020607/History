#将y4m转为png，以备fusion训练,同时产出两个txt目录
from os.path import join,exists
import glob
import os

train_list = open("filelist_train.txt","w")
val_list = open("filelist_val.txt","w")

dataset_path = "/media/x/Database/mls/dataset/"
data_list = glob.glob(join(dataset_path,"*"))
# data_list = [join(dataset_path,"test_damage_B")]

png_path_index = "/media/x/Database/mls/dataset_png/"

#######一个数据包一个文件夹
# one_package = join(dataset_path,"val_ref_part1")  #in data_list = True 一个数据包 10G
for one_package in data_list:
    print(one_package)

    #测试集不要
    if "test" in one_package:
        continue

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
        if "damage" in one_package:
            if "val" in one_package:
                val_list.write(png_path_index2+"\n")
            elif "train" in one_package:
                train_list.write(png_path_index2+"\n")
            png_path_index3 = join(png_path_index2,"blur") #damage对应的png
        else:
            png_path_index2 = png_path_index2.replace("ref","damage") #都存damage
            
            png_path_index3 = join(png_path_index2,"truth")

        if not exists(png_path_index3):
            os.system("mkdir "+png_path_index3)
        print(png_path_index3)
        #输出png
        os.system("ffmpeg -i "+y4m_temp_path + " -vsync 0 "+ png_path_index3 +"/%4d.png -y")


###
train_list.close()
val_list.close()





