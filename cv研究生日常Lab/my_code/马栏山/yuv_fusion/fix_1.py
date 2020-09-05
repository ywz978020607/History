import tensorflow as tf
import numpy as np
import random
from tensorflow.python.ops import control_flow_ops
import glob,os
import cv2

class VSR(object):

    def __init__(self):
        self.num_frames = 7
        self.scale = 1
        self.in_size = 32
        self.gt_size = self.in_size * self.scale
        self.eval_in_size = [128, 240]
        self.batch_size = 16
        self.eval_basz = 4
        self.learning_rate = 1e-3
        self.end_lr = 1e-4
        self.reload = True
        self.max_step = int(1.5e5 + 1)
        self.decay_step = 1.2e5
        self.train_dir = 'train.txt'

    def double_input_producer(self):
        def read_data():
            print(read_data)
            idx0 = self.num_frames // 2
            data_seq = tf.random_crop(self.data_queue, [2, self.num_frames])
            input = tf.stack(
                [tf.image.decode_png(tf.read_file(data_seq[0][i]), channels=3) for i in range(self.num_frames)])
            gt = tf.stack([tf.image.decode_png(tf.read_file(data_seq[1][idx0]), channels=3)])

            # input = tf.stack(
            #     [cv2.imread(data_seq[0][i] ) for i in range(self.num_frames)])
            # gt = tf.stack([cv2.imread(data_seq[1][idx0] )])

            print("load ok")
            input, gt = prepprocessing(input, gt)

            flip = tf.random_uniform((1, 3), minval=0.0, maxval=1.0, dtype=tf.float32, seed=None,
                                     name=None)  # if training gets worse, comment the data flip part out
            input = tf.where(flip[0][0] < 0.5, input, input[:, ::-1])
            input = tf.where(flip[0][1] < 0.5, input, input[:, :, ::-1])
            input = tf.where(flip[0][2] < 0.5, input, tf.transpose(input, perm=(0, 2, 1, 3)))
            gt = tf.where(flip[0][0] < 0.5, gt, gt[:, ::-1])
            gt = tf.where(flip[0][1] < 0.5, gt, gt[:, :, ::-1])
            gt = tf.where(flip[0][2] < 0.5, gt, tf.transpose(gt, perm=(0, 2, 1, 3)))
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
            size_gt = tf.concat([[1], size[:2] * self.scale, [3]], axis=-1)
            gt = tf.slice(gt, offset_gt, size_gt)

            input.set_shape([self.num_frames, self.in_size, self.in_size, 3])
            gt.set_shape([1, self.in_size * self.scale, self.in_size * self.scale, 3])
            return input, gt

        print('start0')
        pathlist = open(self.train_dir, 'rt').read().splitlines()
        random.shuffle(pathlist)
        print('start')
        with tf.variable_scope('input'):
            inList_all = []
            gtList_all = []
            for dataPath in pathlist:
                inList = sorted(glob.glob(os.path.join(dataPath, 'blur/*.png')))
                gtList = sorted(glob.glob(os.path.join(dataPath, 'truth/*.png')))
                inList_all.append(inList)
                gtList_all.append(gtList)
            print(inList_all)
            inList_all = tf.convert_to_tensor(inList_all, dtype=tf.string)
            gtList_all = tf.convert_to_tensor(gtList_all, dtype=tf.string)


            self.data_queue = tf.train.slice_input_producer([inList_all, gtList_all], capacity=self.batch_size * 2)
            #
            # return self.data_queue

            input, gt = read_data()
            print("ywz1")

            # return input,gt

            batch_in, batch_gt = tf.train.batch([input, gt], batch_size=self.batch_size, num_threads=3,
                                                capacity=self.batch_size * 2)
            # batch_in, batch_gt = tf.train.batch(self.data_queue, batch_size=self.batch_size, num_threads=1,
            #                                     capacity=self.batch_size * 2)
            print('ywz2')
        return batch_in, batch_gt

################################
model=VSR()

LR, HR= model.double_input_producer()
sess = tf.Session()
#############
coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)
#############
sess.run(tf.global_variables_initializer())
lr1,hr=sess.run([LR,HR])
print(lr1)

# ###
# data_queue = model.double_input_producer()
# sess = tf.Session()
# #############
# coord = tf.train.Coordinator()
# threads = tf.train.start_queue_runners(sess=sess, coord=coord)
# #############
# sess.run(tf.global_variables_initializer())
# a = sess.run(data_queue[0])
# print(a)
# pass
