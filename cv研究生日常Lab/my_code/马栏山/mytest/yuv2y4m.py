#A榜数据增强后的yuv转y4m

import os
import glob
from os.path import exists,join

yuv_path_index = "/media/x/Database/mls/fusion_ori_out/ori_fusion/"
one_damage_name = "test_damage_A"

y4m_path_index = "/media/x/Database/mls/fusion_ori_out/fusion_y4m_test_damage_A"

yuv_path = join(yuv_path_index,one_damage_name)
yuv_list = sorted(glob.glob(join(yuv_path,"*")))
for ii in range(len(yuv_list)):
    yuv_temp_path = yuv_list[ii]
    yuv_temp_name = yuv_temp_path.split(yuv_path)[-1].strip("/") #xx.yuv

    y4m_temp_name = yuv_temp_name.replace(".yuv",".y4m")
    y4m_temp_path = join(y4m_path_index,y4m_temp_name)
    print(yuv_temp_path)
    print(y4m_temp_path)

    cmd = "ffmpeg -s 1920x1080 -i "+yuv_temp_path+" -vsync 0 "+y4m_temp_path+" -y"
    os.system(cmd)

