import sys
import os.path as op

# TRAIN
fp = open(op.join(sys.path[0], 'filelist_train.txt'), 'w')

str_pre = "/home/xql/projects/mls/dataset_png/train_damage_part1/mg_train_"
str_suf = "_damage\n"
for num in range(0, 100):
    strr = str_pre + "{:04d}".format(num) + str_suf
    fp.write(strr)

str_pre = "/home/xql/projects/mls/dataset_png/train_damage_part2/mg_train_"
str_suf = "_damage\n"
for num in range(100, 200):
    strr = str_pre + "{:04d}".format(num) + str_suf
    fp.write(strr)

str_pre = "/home/xql/projects/mls/dataset_png/train_damage_part3/mg_train_"
str_suf = "_damage\n"
for num in range(200, 300):
    strr = str_pre + "{:04d}".format(num) + str_suf
    fp.write(strr)

str_pre = "/home/xql/projects/mls/dataset_png/train_damage_part4/mg_train_"
str_suf = "_damage\n"
for num in range(300, 400):
    strr = str_pre + "{:04d}".format(num) + str_suf
    fp.write(strr)

str_pre = "/home/xql/projects/mls/dataset_png/train_damage_part5/mg_train_"
str_suf = "_damage\n"
for num in range(400, 500):
    strr = str_pre + "{:04d}".format(num) + str_suf
    fp.write(strr)

str_pre = "/home/xql/projects/mls/dataset_png/train_damage_part6/mg_train_"
str_suf = "_damage\n"
for num in range(500, 600):
    strr = str_pre + "{:04d}".format(num) + str_suf
    fp.write(strr)

fp.close()

# VAL only 50 video!!!!!!!!!!!!!!
fp = open(op.join(sys.path[0], 'filelist_val.txt'), 'w')

str_pre = "/home/xql/projects/mls/dataset_png/val_damage_part1/mg_val_"
str_suf = "_damage\n"
for num in range(600, 700, 4):
    strr = str_pre + "{:04d}".format(num) + str_suf
    fp.write(strr)

str_pre = "/home/xql/projects/mls/dataset_png/val_damage_part2/mg_val_"
str_suf = "_damage\n"
for num in range(700, 800, 4):
    strr = str_pre + "{:04d}".format(num) + str_suf
    fp.write(strr)

fp.close()