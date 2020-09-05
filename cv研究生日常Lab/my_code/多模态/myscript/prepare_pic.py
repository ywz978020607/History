# mv pic to fit the project.

import os
import os.path as osp
import glob


folder = "/home/ywz/remote/flicker_2W_images"
train_folder = "/home/ywz/remote/pic/train"
test_folder =  "/home/ywz/remote/pic/test"

train_test_rate = 10

all_pic = sorted(glob.glob(osp.join(folder,"*")))
print(len(all_pic))

def move_pic(ori_file_path,to_path):
    # global
    to_file_path = osp.join(to_path , osp.basename(ori_file_path))
    os.system("cp "+ori_file_path +" "+ to_file_path)

def main():
    count = 0
    for pic_ii in all_pic:
        if count >= train_test_rate:
            move_pic(pic_ii,test_folder)
            count = 0
            print(pic_ii)
        else:
            move_pic(pic_ii,train_folder)
        count += 1

if __name__ == "__main__":
    main()


