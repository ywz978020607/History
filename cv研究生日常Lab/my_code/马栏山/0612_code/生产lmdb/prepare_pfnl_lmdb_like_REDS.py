"""Create lmdb files for [General images (291 images/DIV2K) | Vimeo90K | REDS] training datasets"""
#malanshan by ywz

import sys
import os.path as osp
import glob
import pickle
from multiprocessing import Pool
import numpy as np
import lmdb
import cv2

sys.path.append(osp.dirname(osp.dirname(osp.abspath(__file__))))
import data.util as data_util  # noqa: E402
import utils.util as util  # noqa: E402


def main():
    dataset = 'general'  # vimeo90K | REDS | general (e.g., DIV2K, 291) | DIV2K_demo |test
    # mode = 'GT'  # used for vimeo90k and REDS datasets
    # vimeo90k: GT | LR | flow
    # REDS: train_sharp, train_sharp_bicubic, train_blur_bicubic, train_blur, train_blur_comp
    #       train_sharp_flowx4
    
    if dataset == 'general':
        opt = {}
        opt['dir_name'] = "test_damage_A"
    
        opt['img_folder'] = '/media/x/Database/mls/dataset_png/'
        opt['name'] = 'damage_test' #damage_train or damage_val
        # opt['kind_of_damage_or_val'] = 'blur' # 'blur' or 'truth'

        opt['lmdb_save_path'] = '/media/x/Database/mls/dataset_lmdb/'+opt['dir_name']+'.lmdb'
        general_image_folder(opt)

    elif dataset == 'test':
        test_lmdb('xxxx.lmdb', 'REDS')


def read_image_worker(path, key):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    return (key, img)


def general_image_folder(opt):
    """Create lmdb for general image folders
    Users should define the keys, such as: '0321_s035' for DIV2K sub-images
    If all the images have the same resolution, it will only store one copy of resolution info.
        Otherwise, it will store every resolution info.
    """
    #### configurations
    read_all_imgs = False  # whether real all images to memory with multiprocessing
    # Set False for use limited memory
    # BATCH = 5000  # After BATCH images, lmdb commits, if read_all_imgs = False
    BATCH = 100000 #100000
    n_thread = 40
    ########################################################
    # sub_dir_list = ['train_damage_part1', 'train_damage_part2', 'train_damage_part3', 'train_damage_part4',
    #                 'train_damage_part5', 'train_damage_part6']
    # sub_dir_list = ['val_damage_part1', 'val_damage_part2']
    sub_dir_list = [opt['dir_name']]
    # kind_of_damage_or_val = opt['kind_of_damage_or_val']

    lmdb_save_path = opt['lmdb_save_path']
    img_folder = opt['img_folder']
    meta_info = {'name': opt['name']}
    if not lmdb_save_path.endswith('.lmdb'):
        raise ValueError("lmdb_save_path must end with \'lmdb\'.")
    if osp.exists(lmdb_save_path):
        print('Folder [{:s}] already exists. Exit...'.format(lmdb_save_path))
        sys.exit(1)
    ##
    all_img_list = []
    for ii in range(len(sub_dir_list)):
        print(sub_dir_list[ii])
        #### read all the image paths to a list
        print('Reading image path list ...')
        # all_img_list = sorted(glob.glob(osp.join(img_folder, '*')))

        video_list = sorted(glob.glob(osp.join(img_folder,sub_dir_list[ii],"*")))
        for jj in range(len(video_list)):
            imgs_path_list = sorted(glob.glob(osp.join(video_list[jj],"*")))
            for zz in range(len(imgs_path_list)):
                all_img_list.append(imgs_path_list[zz])
        # print(all_img_list)
    all_img_list = all_img_list[0:(int)(len(all_img_list)/2)]
    keys = []
    for img_path in all_img_list:
        temp1 = img_path.split('/')[-2].split('_')[-2][1:] #000~589,val:600~xxx
        #when test
        temp1 = str((int)(temp1) - 800).zfill(3)  # 000~xxx
        #
        temp2 = osp.splitext(osp.basename(img_path))[0] #0001~0120
        temp2 = str((int)(temp2) - 1).zfill(4) #0000~0119
        keys.append(temp1+"_0000"+temp2) #3-8

    # print(keys)

    ###
    if read_all_imgs:
        #### read all images to memory (multiprocessing)
        dataset = {}  # store all image data. list cannot keep the order, use dict
        print('Read images with multiprocessing, #thread: {} ...'.format(n_thread))
        pbar = util.ProgressBar(len(all_img_list))

        def mycallback(arg):
            '''get the image data and update pbar'''
            key = arg[0]
            dataset[key] = arg[1]
            pbar.update('Reading {}'.format(key))

        pool = Pool(n_thread)
        for path, key in zip(all_img_list, keys):
            pool.apply_async(read_image_worker, args=(path, key), callback=mycallback)
        pool.close()
        pool.join()
        print('Finish reading {} images.\nWrite lmdb...'.format(len(all_img_list)))

    #### create lmdb environment
    data_size_per_img = cv2.imread(all_img_list[0], cv2.IMREAD_UNCHANGED).nbytes
    print('data size per image is: ', data_size_per_img)
    data_size = data_size_per_img * len(all_img_list)
    env = lmdb.open(lmdb_save_path, map_size=data_size * 10)

    #### write data to lmdb
    pbar = util.ProgressBar(len(all_img_list))
    txn = env.begin(write=True)
    resolutions = []
    for idx, (path, key) in enumerate(zip(all_img_list, keys)):
        pbar.update('Write {}'.format(key))
        key_byte = key.encode('ascii')
        data = dataset[key] if read_all_imgs else cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if data.ndim == 2:
            H, W = data.shape
            C = 1
        else:
            H, W, C = data.shape
        txn.put(key_byte, data)
        resolutions.append('{:d}_{:d}_{:d}'.format(C, H, W))
        if not read_all_imgs and idx % BATCH == 0:
            txn.commit()
            txn = env.begin(write=True)
    txn.commit()
    env.close()
    print('Finish writing lmdb.')

    #### create meta information
    # check whether all the images are the same size
    assert len(keys) == len(resolutions)
    if len(set(resolutions)) <= 1:
        meta_info['resolution'] = [resolutions[0]]
        meta_info['keys'] = keys
        print('All images have the same resolution. Simplify the meta info.')
    else:
        meta_info['resolution'] = resolutions
        meta_info['keys'] = keys
        print('Not all images have the same resolution. Save meta info for each image.')

    pickle.dump(meta_info, open(osp.join(lmdb_save_path, 'meta_info.pkl'), "wb"))
    print('Finish creating lmdb meta info.')

def test_lmdb(dataroot, dataset='LQGT'):
    env = lmdb.open(dataroot, readonly=True, lock=False, readahead=False, meminit=False)
    meta_info = pickle.load(open(osp.join(dataroot, 'meta_info.pkl'), "rb"))
    print('Name: ', meta_info['name'])
    print('Resolution: ', meta_info['resolution'])
    print('# keys: ', len(meta_info['keys']))
    # read one image
    if dataset == 'vimeo90k':
        key = '00001_0001_4'
    else:
        key = '000_00000001'
    print('Reading {} for test.'.format(key))
    with env.begin(write=False) as txn:
        buf = txn.get(key.encode('ascii'))
    img_flat = np.frombuffer(buf, dtype=np.uint8)
    C, H, W = [int(s) for s in meta_info['resolution'].split('_')]
    img = img_flat.reshape(H, W, C)
    cv2.imwrite('test.png', img)


if __name__ == "__main__":
    main()
