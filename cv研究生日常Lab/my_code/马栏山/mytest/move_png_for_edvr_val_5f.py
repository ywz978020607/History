import os.path as osp
import os,glob

from_path = "/media/x/Database/mls/dataset_png/val_damage_part1"
kind = 'blur'

to_path = "/media/x/Database/mls/dataset_png/val_damage"

path1 = sorted(glob.glob(osp.join(from_path,"*")))
for path1_ii in path1:
    path1_name = path1_ii.split('/')[-1]
    to_path1 = osp.join(to_path,path1_name) #val_damage/mg00
    if not osp.exists(to_path1):
        os.system('mkdir '+to_path1)
    
    path2 = osp.join(path1_ii,kind)
    path3 = sorted(glob.glob(os.path.join(path2,"*"))) #img paths #val_damage/mg00/blur/000.png
    for path3_ii in path3[50:55]:
        path3_name = path3_ii.split('/')[-1]
        to_path3_ii = osp.join(to_path1,path3_name) #val_damage/mg00/001.png

        os.system('cp '+ path3_ii +' '+to_path3_ii)
        print(to_path3_ii)





