import os
from model.vespcn import VESPCN
from model.ltdvsr import LTDVSR
from model.mcresnet import MCRESNET
from model.drvsr import DRVSR
from model.frvsr import FRVSR
from model.dufvsr import DUFVSR
from model.pfnl import PFNL

from os.path import join,exists
import glob

os.environ["CUDA_VISIBLE_DEVICES"] = "1"

###
#1. 将y4m转为bmp,yuv
dataset_path = "/media/x/Database/mls/dataset/"
data_list = glob.glob(dataset_path+"*")

#######一个数据包一个文件夹
one_package = join(dataset_path,"val_damage_part1")  #in data_list = True 一个数据包 10G
one_package_temp_name1 = one_package.split(dataset_path)[-1].strip("/") #文件夹名字


################################
#输出原转换yuv位置
yuv_path_index = "/media/x/Database/mls/fusion_ori_out/ori_yuv/"
yuv_path = join(yuv_path_index,one_package_temp_name1)
#不存在则创建文件夹
if not exists(yuv_path):
    os.system("mkdir "+yuv_path)
    print(yuv_path)

#fusion_yuv位置
fusion_yuv_path_index = "/media/x/Database/mls/fusion_ori_out/ori_fusion/"
fusion_yuv_path = join(fusion_yuv_path_index,one_package_temp_name1)
#不存在则创建文件夹
if not exists(fusion_yuv_path):
    os.system("mkdir "+fusion_yuv_path)
    print(fusion_yuv_path)
######################################################
#每一个视频输出yuv
y4m_list = sorted(glob.glob(join(one_package,"*")))
for ii in range(len(y4m_list)):
    y4m_temp_path = y4m_list[ii]
    y4m_temp_name = y4m_list[ii].split(one_package)[-1].strip("/") #xx.y4m
    yuv_temp_name = y4m_temp_name.split(".y4m")[0]+".yuv" #xx.yuv
    yuv_temp_path = join(yuv_path,yuv_temp_name)

    if not exists(yuv_temp_path):
        os.system("ffmpeg -i "+y4m_temp_path+" -vsync 0 "+yuv_temp_path+"  -y")

    #######################
    ##fusion
    #fusion输出yuv文件完整路径
    fusion_yuv_temp_path = join(fusion_yuv_path,yuv_temp_name)

    if not exists(fusion_yuv_temp_path):
        # #删除
        os.system("rm ./test/truth/*")
        os.system("rm ./test/pfnl/*")

        os.system("ffmpeg -i "+y4m_temp_path + " -vsync 0 ./test/truth/%4d.png -y")
        #2. 运行fusion 输出
        model=PFNL()
        # model.train()
        model.test_video_truth("./test/", name="pfnl", reuse=False, part=1000)

        #3. 将输出图片转为yuv
        os.system("ffmpeg -i ./test/pfnl/%4d.png -s 1920x1080 -pix_fmt yuv420p "+ fusion_yuv_temp_path)
        # #删除
        # os.system("rm ./test/truth/*")
        # os.system("rm ./test/pfnl/*")





