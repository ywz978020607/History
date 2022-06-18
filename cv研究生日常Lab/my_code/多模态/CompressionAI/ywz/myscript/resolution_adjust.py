# 将2kInstereo 由1024,860 ->1024,832   832/16 = 52 ; 52/4 = 13
import os,glob
import os.path as osp

import cv2

#根目录 可以是移动硬盘，也可以是本地
root_path = "/media/sharklet/diskywz/DSIC/InStereo2K"
# root_path = "/home/sharklet/database"
#out
out_path = "/media/sharklet/diskywz/DSIC/aftercut"
#不存在则创建文件夹
if not osp.exists(out_path):
    os.system("mkdir "+out_path)
    print(out_path)
################################################################
def cut_pic(ori_file,out_file,W,H): #eg:W=1024,H=832
    image = cv2.imread(ori_file)  # numpy数组格式（H,W,C=3），通道顺序（B,G,R) H<W
    image = image[0:H,0:W] #H=832,W=1024
    cv2.imwrite(out_file,image)

######################################
# #test
# path2 =osp.join(root_path,"test")
# path2_list = sorted(glob.glob(osp.join(path2,"*")))
# path2_out = osp.join(out_path,"test")
# if not osp.exists(path2_out):
#     os.system("mkdir "+path2_out)
# if not osp.exists(osp.join(path2_out, "left")):
#     os.system("mkdir " + osp.join(path2_out, "left"))
# if not osp.exists(osp.join(path2_out, "right")):
#     os.system("mkdir " + osp.join(path2_out, "right"))
# #aftercut/test/left/1.png
# count = 0
# for path3 in path2_list:
#     #left
#     # path3_base = osp.basename(path3)
#     try:
#         cut_pic(osp.join(path3, "left.png"), osp.join(path2_out, "left", str(count) + ".png"), 1024, 832)
#         cut_pic(osp.join(path3, "right.png"), osp.join(path2_out, "right", str(count) + ".png"), 1024, 832)
#         print("\r"+path3,end='') #只占一行
#         count += 1
#     except:
#         print(path3)
#         raise ValueError('cannot find')
# print("")


# #train
# path2_list = []
# for temp_part in range(1,7):
#     path2 =osp.join(root_path,"train/part"+str(temp_part))
#     path2_list += sorted(glob.glob(osp.join(path2,"*")))
# print("train picture-pair numbers:")
# print(len(path2_list))
# path2_out = osp.join(out_path,"train")
# if not osp.exists(path2_out):
#     os.system("mkdir "+path2_out)
# if not osp.exists(osp.join(path2_out, "left")):
#     os.system("mkdir " + osp.join(path2_out, "left"))
# if not osp.exists(osp.join(path2_out, "right")):
#     os.system("mkdir " + osp.join(path2_out, "right"))
# #aftercut/test/left/1.png
# count = 0
# for path3 in path2_list:
#     #left
#     # path3_base = osp.basename(path3)
#     try:
#         cut_pic(osp.join(path3, "left.png"), osp.join(path2_out, "left", str(count) + ".png"), 1024, 832)
#         cut_pic(osp.join(path3, "right.png"), osp.join(path2_out, "right", str(count) + ".png"), 1024, 832)
#         print("\r"+path3,end='') #只占一行
#         count += 1
#     except:
#         print(path3)
#         raise ValueError('cannot find')
# print("")









