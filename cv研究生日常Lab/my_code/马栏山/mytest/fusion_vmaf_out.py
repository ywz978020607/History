from vmaf_func import *
from os.path import join,exists
import glob
import os


#默认使用env里的model文件夹内的模型
# model_path = "~/mls_code_test/vmaf/model"
##########################
#选择一个文件夹
fusion_yuv_path_index = "/media/x/Database/mls/fusion_ori_out/ori_fusion"  #ori_fusion/ori_yuv 分别指增强后和增强前的yuv 和ref里的ori_yuv比较vmaf和psnr！
one_damage_name = "val_damage_part1"

ori_yuv_path_index = "/media/x/Database/mls/fusion_ori_out/ori_yuv"
one_ref_name = "val_ref_part1"

ori_yuv_path = join(ori_yuv_path_index, one_ref_name)
fusion_yuv_path = join(fusion_yuv_path_index, one_damage_name)
# print(ori_yuv_path)
# print(fusion_yuv_path)

out_json_path = join(fusion_yuv_path, "vmaf_json")
if not exists(out_json_path):
    os.system("mkdir "+out_json_path)

###################
yuv_list = sorted(glob.glob(join(ori_yuv_path,"*")))
for ii in range(len(yuv_list)):
    ori_yuv_temp_path = yuv_list[ii]
    ori_yuv_temp_name = ori_yuv_temp_path.split(ori_yuv_path)[-1].strip("/") #xx.yuv

    fusion_yuv_temp_name_match = ori_yuv_temp_name.split(ori_yuv_temp_name.split('_')[-1])[0].strip("_")
    fusion_yuv_temp_path = glob.glob(join(fusion_yuv_path,fusion_yuv_temp_name_match+"*"))[0]
    if not exists(fusion_yuv_temp_path):
        print(fusion_yuv_temp_path)
        print("fusion yuv not exists!")
        break

    print(ori_yuv_temp_path)
    print(fusion_yuv_temp_path)
    print(out_json_path)
    # vmaf_json("yuv420p",1920,1080,ori_yuv_temp_path,fusion_yuv_temp_path,out_json_path)






