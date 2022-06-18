import tensorflow as tf
from tensorflow.python.ops import control_flow_ops
import glob
import random
import numpy as np

from utils import LoadImage, DownSample, DownSample_4D, BLUR, AVG_PSNR, depth_to_space_3D, DynFilter3D, LoadParams, cv2_imread, cv2_imsave, get_num_params, automkdir
from model.nets import FR_16L, FR_28L, FR_52L
from modules.videosr_ops import imwarp_forward




import os
import os.path as op


class VSR(object):
    def __init__(self):
        self.num_frames=7
        self.scale=4
        self.in_size=32
        self.gt_size=self.in_size*self.scale
        self.eval_in_size=[128,240]
        self.batch_size=16
        self.eval_basz=4
        self.learning_rate=1e-3
        self.end_lr=1e-4
        self.reload=True
        self.max_step=int(1.5e5+1)
        self.decay_step=1.2e5
        self.train_dir='./data/filelist_train.txt'
        self.eval_dir='./data/filelist_val.txt'
        self.save_dir='./checkpoint'
        self.log_dir='./eval_log.txt'
    

    def frvsr_input_producer(self):
        def read_data():
            idx0 = self.num_frames // 2
            data_seq = tf.random_crop(self.data_queue, [2, self.num_frames])
            input = tf.stack([tf.image.decode_png(tf.read_file(data_seq[0][i]), channels=3) for i in range(self.num_frames)])
            #gt = tf.stack([tf.image.decode_png(tf.read_file(data_seq[1][idx0]), channels=3)])
            gt = tf.stack([tf.image.decode_png(tf.read_file(data_seq[1][i]), channels=3) for i in range(self.num_frames)])
            input, gt = prepprocessing(input, gt)
            print('Input producer shape: ', input.get_shape(), gt.get_shape())
            return input, gt

        def prepprocessing(input, gt=None):
            input = tf.cast(input, tf.float32) / 255.0
            gt = tf.cast(gt, tf.float32) / 255.0

            shape = tf.shape(input)[1:]
            size = tf.convert_to_tensor([self.in_size, self.in_size, 3], dtype=tf.int32, name="size")
            check = tf.Assert(tf.reduce_all(shape >= size), ["Need value.shape >= size, got ", shape, size])
            shape = control_flow_ops.with_dependencies([check], shape)

            limit = shape - size + 1
            offset = tf.random_uniform(tf.shape(shape), dtype=size.dtype, maxval=size.dtype.max, seed=None) % limit

            offset_in = tf.concat([[0], offset], axis=-1)
            size_in = tf.concat([[self.num_frames], size], axis=-1)
            input = tf.slice(input, offset_in, size_in)
            offset_gt = tf.concat([[0], offset[:2] * self.scale, [0]], axis=-1)
            size_gt = tf.concat([[self.num_frames], size[:2] * self.scale, [3]], axis=-1)
            gt = tf.slice(gt, offset_gt, size_gt)

            input.set_shape([self.num_frames, self.in_size, self.in_size, 3])
            gt.set_shape([self.num_frames, self.in_size * self.scale, self.in_size * self.scale, 3])
            return input, gt
            

        pathlist=open(self.train_dir, 'rt').read().splitlines()
        random.shuffle(pathlist)
        with tf.variable_scope('input'):
            inList_all = []
            gtList_all = []
            for dataPath in pathlist:
                inList = sorted(glob.glob(op.join(dataPath, 'blur{}/*.png'.format(self.scale))))
                gtList = sorted(glob.glob(op.join(dataPath, 'truth/*.png')))
                inList_all.append(inList)
                gtList_all.append(gtList)
            inList_all = tf.convert_to_tensor(inList_all, dtype=tf.string)
            gtList_all = tf.convert_to_tensor(gtList_all, dtype=tf.string)

            self.data_queue = tf.train.slice_input_producer([inList_all, gtList_all], capacity=self.batch_size*2)
            input, gt = read_data()
            batch_in, batch_gt = tf.train.batch([input, gt], batch_size=self.batch_size, num_threads=3, capacity=self.batch_size*2)
        return batch_in, batch_gt




if __name__=='__main__':
    model=VSR()
    model.train()
    #model.testvideos()