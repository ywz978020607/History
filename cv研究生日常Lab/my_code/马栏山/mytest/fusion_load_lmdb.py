import os.path as osp
import random
import numpy as np
import cv2
import os,glob
import pickle
import lmdb


###################### read images ######################
def _get_paths_from_lmdb(dataroot):
    """get image path list from lmdb meta info"""
    meta_info = pickle.load(open(os.path.join(dataroot, 'meta_info.pkl'), 'rb'))
    paths = meta_info['keys']
    sizes = meta_info['resolution']
    if len(sizes) == 1:
        sizes = sizes * len(paths)
    return paths, sizes


def get_image_paths(data_type, dataroot):
    """get image path list
    support lmdb"""
    paths, sizes = None, None
    if dataroot is not None:
        if data_type == 'lmdb':
            paths, sizes = _get_paths_from_lmdb(dataroot)
        else:
            raise NotImplementedError('data_type [{:s}] is not recognized.'.format(data_type))
    return paths, sizes

def _read_img_lmdb(env, key, size):
    """read image from lmdb with key (w/ and w/o fixed size)
    size: (C, H, W) tuple"""
    with env.begin(write=False) as txn:
        buf = txn.get(key.encode('ascii'))
    img_flat = np.frombuffer(buf, dtype=np.uint8)
    C, H, W = size
    img = img_flat.reshape(H, W, C)
    return img


def read_img(env, path, size=None):
    """read image by cv2 or from lmdb
    return: Numpy float32, HWC, BGR->RGB, [0,1]"""
    if env is None:  # img
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    else:
        # print(path)
        img = _read_img_lmdb(env, path, size)
    img = img.astype(np.float32) / 255.
    if img.ndim == 2:
        img = np.expand_dims(img, axis=2)
    # some images have 4 channels
    if img.shape[2] > 3:
        img = img[:, :, :3]
    
    img = img[:, :, [2, 1, 0]]

    return img


##########################################################

from fusion_load_lmdb import *
import time

lmdb_path = "/media/x/Database/mls/dataset_lmdb/test_damage_B.lmdb"
paths,_ = get_image_paths('lmdb',lmdb_path)
lmdb_env =  lmdb.open(lmdb_path, readonly=True, lock=False, readahead=False,meminit=False)
size =  (3, 1080, 1920)

# temp_yuv = []
# temp_yuv_num = '000'
# for ii in paths:
#     if temp_yuv_num+"_" in ii:
#         temp_yuv.append(ii)
#     elif not (temp_yuv == []):
#         break

# def func1():
#     start_time = time.time()
#     imgs = np.array([read_img(lmdb_env,i,size) for i in temp_yuv])
#     end_time = time.time()
#     print(end_time-start_time)

# func1()


# 对比原 png 读法  "/media/x/Database/mls/dataset_png/test_damage_A/mg_test_0800_damage"
# imgs=sorted(glob.glob(join(inp_path,'*.png')))
# imgs=np.array([cv2_imread(i) for i in imgs])/255.   #3 channels RGB模式！！ cv2.imread是BGR

# import cv2
# from os.path import join

# def cv2_imread(img_path):
#     img=cv2.imread(img_path)
#     if img.ndim == 3:
#         img = img[:, :, [2, 1, 0]]
#     return img

# def func2():
#     inp_path = "/media/x/Database/mls/dataset_png/test_damage_A/mg_test_0800_damage"
#     imgs = sorted(glob.glob(join(inp_path,'*.png')))
#     start_time = time.time()
#     imgs=np.array([cv2_imread(i) for i in imgs])/255.   #3 channels RGB模式！！ cv2.imread是BGR
#     end_time = time.time()
#     print(end_time-start_time)

# func2()