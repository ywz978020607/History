import os
import cv2
import sys
import glob
import time
import random
import os.path as op
import numpy as np
from math import ceil
from tqdm import tqdm
from functools import reduce
from operator import mul

from fusion_load_lmdb import *

sys.path.append('/home/xql/anaconda3/envs/tf/lib/python3.7/site-packages/')  # varies by env!!!
import tensorflow as tf
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.layers.convolutional import Conv2D, conv2d

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


def get_num_params(vars):
    num_params = 0
    for variable in vars:
        shape = variable.get_shape()
        num_params += reduce(mul, [dim.value for dim in shape], 1)
    return num_params

def cv2_imsave(img_path, img):
    img = np.squeeze(img)
    if img.ndim == 3:
        img = img[:, :, [2, 1, 0]]
    cv2.imwrite(img_path, img)

def cv2_imread(img_path):
    img=cv2.imread(img_path)
    if img.ndim == 3:
        img = img[:, :, [2, 1, 0]]  # bgr -> rgb
    return img


class PFNL():
    def __init__(self, tab):
        # forward
        self.num_frames = 5  # 7 frames for 1 center frame
        self.num_block = 40  # progressive fusion block num
        self.refactor = 2  # downsample for nonlocal
        
        #gpu_num
        self.num_gpus = 4

        # train
        self.in_size = 128  # 64 => OOM
        self.gt_size = self.in_size
        self.batch_size = 4
        self.train_dir = 'filelist_train.txt'

        self.reload = True  # if collasp, reload and train

        self.disp_step = 50
        self.learning_rate= 0.0005  # 1e-3
        self.end_lr= 5e-05  # 1e-4
        self.global_step = 0  # init
        self.max_step = int(1.5e5 + 1)
        self.decay_step = 1.2e4

        self.model_dir = op.join('checkpoint', tab)  # save model dir
        if not op.exists(self.model_dir):
            os.makedirs(self.model_dir)

        # val
        self.eval_step = 1000
        self.eval_in_size = [270, 480]  # [270, 480], the same as [1920, 1080] // 4. But 270 cannot be refactorred by 4
        self.eval_basz = 1  # crash when = 4,8,16,... and [270, 480]
        self.eval_gap = 56  # gap between two center frames. 14 may be too small (=> 430 test batches)
        self.eval_dir = 'filelist_val.txt'

        self.log_path = op.join(self.model_dir, 'log.txt')

        # test
        self.test_bs = 1  # batch size
        self.cut_time = 2  # h -> h // cut_time
    
    def forward(self, x):
        def _NonLocalBlock(input_x, out_channels, sub_sample=1, nltype=0 ,is_bn=False, scope='NonLocalBlock'):
            """
            https://github.com/nnUyi/Non-Local_Nets-Tensorflow
            """
            batchsize, height, width, in_channels = input_x.get_shape().as_list()
            typedict={0:'embedded_gaussian',1:'gaussian',2:'dot_product',3:'concat'}
            with tf.variable_scope(scope) as sc:
                if nltype<=2:
                    with tf.variable_scope('g') as scope:
                        g = conv2d(input_x, out_channels, 1, strides=1, padding='same', name='g')
                        if sub_sample>1:
                            g=average_pooling2d(g,pool_size=sub_sample,strides=sub_sample,name='g_pool')

                    with tf.variable_scope('phi') as scope:
                        if nltype==0 or nltype==2:
                            phi = conv2d(input_x, out_channels, 1, strides=1, padding='same', name='phi')
                        elif nltype==1:
                            phi=input_x
                        if sub_sample>1:
                            phi=average_pooling2d(phi,pool_size=sub_sample,strides=sub_sample,name='phi_pool')

                    with tf.variable_scope('theta') as scope:
                        if nltype==0 or nltype==2:
                            theta = conv2d(input_x, out_channels, 1, strides=1, padding='same', name='theta')
                        elif nltype==1:
                            theta = input_x
                    
                    g_x = tf.reshape(g, [batchsize, -1,out_channels])
                    theta_x = tf.reshape(theta, [batchsize, -1, out_channels])

                    # theta_x = tf.reshape(theta, [batchsize, out_channels, -1])
                    # theta_x = tf.transpose(theta_x, [0,2,1])
                    phi_x = tf.reshape(phi, [batchsize, -1, out_channels])
                    phi_x = tf.transpose(phi_x, [0,2,1])
                    #phi_x = tf.reshape(phi_x, [batchsize, out_channels, -1])

                    f = tf.matmul(theta_x, phi_x)
                    # ???
                    if nltype<=1:
                        # f_softmax = tf.nn.softmax(f, -1)
                        f = tf.exp(f)
                        f_softmax = f/tf.reduce_sum(f,axis=-1,keepdims=True)
                    elif nltype==2:
                        f = tf.nn.relu(f)#/int(f.shape[-1])
                        f_mean=tf.reduce_sum(f,axis=[2],keepdims=True)
                        #print(f.shape,f_mean.shape)
                        f_softmax = f/f_mean
                    y = tf.matmul(f_softmax, g_x)
                    y = tf.reshape(y, [batchsize, height, width, out_channels])
                    with tf.variable_scope('w') as scope:
                        w_y = conv2d(y, in_channels, 1, strides=1, padding='same', name='w')
                        # if is_bn:
                        #     w_y = slim.batch_norm(w_y)
                    z = w_y #input_x + w_y
                    return z
        """
        hyper-paras
        """
        mf = 64  # output feature map num for most convs
        dk = 3  # kernel size for most convs
        ds = 1  # stride for most convs
        activate = tf.nn.leaky_relu
        num_block = self.num_block  # progressive fusion block num
        ki = tf.contrib.layers.xavier_initializer()
        
        n, nf, w, h, c = x.shape
        # print(n, nf, w, h, c)

        with tf.variable_scope('network',reuse=tf.AUTO_REUSE) as scope:
            conv0=Conv2D(mf, 5, strides=ds, padding='same', activation=activate, kernel_initializer=ki, name='conv0')
            conv1=[Conv2D(mf, dk, strides=ds, padding='same', activation=activate, kernel_initializer=ki, name='conv1_{}'.format(i)) for i in range(num_block)]
            conv10=[Conv2D(mf, 1, strides=ds, padding='same', activation=activate, kernel_initializer=ki, name='conv10_{}'.format(i)) for i in range(num_block)]
            conv2=[Conv2D(mf, dk, strides=ds, padding='same', activation=activate, kernel_initializer=ki, name='conv2_{}'.format(i)) for i in range(num_block)]
            convout4 = Conv2D(256, 3, strides=ds, padding='same', activation=activate, kernel_initializer=ki, name='convout4')
            convout3 = Conv2D(128, 3, strides=ds, padding='same', activation=activate, kernel_initializer=ki, name='convout3')
            convout2 = Conv2D(64, 3, strides=ds, padding='same', activation=activate, kernel_initializer=ki, name='convout2')
            convout1 = Conv2D(3, 3, strides=ds, padding='same', activation=None, kernel_initializer=ki, name='convout1')

            """
            center for residual add
            """
            center_tensor = x[:, self.num_frames//2, :, :, :]  # (bs, h, w, c)
            # print(center_tensor.get_shape())

            """
            nonlocal + res
            """
            inp0 = [x[:,i,:,:,:] for i in range(nf)]  # [nf * (bs, h, w, c)]
            inp0 = tf.concat(inp0, axis=-1)  # (bs, h, w, c*nf)
            # print(inp0.get_shape())
            
            if self.refactor > 1:
                inp1 = tf.space_to_depth(inp0, self.refactor)  # space2depth: (h, w, c) -> (h//2, w//2, c*4)
            else:
                inp1 = inp0
            inp1 = _NonLocalBlock(inp1, int(c)*self.num_frames*self.refactor*self.refactor, sub_sample=1, nltype=1, scope='nlblock_{}'.format(0))
            if self.refactor > 1:
                inp1 = tf.depth_to_space(inp1, self.refactor)  # depth2space: (h//2, w//2, c*4) -> (h, w, c)
            
            inp0 += inp1  # (bs, h, w, c*nf)

            """
            5x5 conv
            """
            inp0 = tf.split(inp0, num_or_size_splits=self.num_frames, axis=-1)  # [nf * (bs, h, w, c)]
            # print(len(inp0))
            # print(inp0[0].get_shape())
            inp0 = [conv0(f) for f in inp0]  # [nf * (bs, h, w, 64)]
            # print(inp0[0].get_shape())

            """
            progressive fusion blocks
            """
            for i in range(num_block):
                inp1 = [conv1[i](f) for f in inp0]  # [nf * (bs, h, w, 64)]
                base = tf.concat(inp1, axis=-1)  # (bs, h, w, 64*nf)
                base = conv10[i](base)
                inp2 = [tf.concat([base,f],-1) for f in inp1]
                inp2 = [conv2[i](f) for f in inp2]
                inp0 = [tf.add(inp0[j],inp2[j]) for j in range(nf)]  # [nf * (bs, h, w, 64)]

            """
            merge
            """
            merge = tf.concat(inp0, axis=-1)  # (bs, h, w, 64*nf)
            out = convout4(merge)
            out = convout3(out)
            out = convout2(out)
            out = convout1(out)  # (bs, h, w, c)
        
        """
        residual
        """
        return tf.stack([out + center_tensor], axis=1, name='out')  # (bs, h, w, c) -> (bs, 1, h, w, c)

    def double_input_producer(self):
        def prepprocessing(inp, gt=None):
            inp = tf.cast(inp, tf.float32) / 255.0
            gt = tf.cast(gt, tf.float32) / 255.0

            shape = tf.shape(inp)[1:]
            size = tf.convert_to_tensor([self.in_size, self.in_size, 3], dtype=tf.int32, name="size")
            check = tf.Assert(tf.reduce_all(shape >= size), ["Need value.shape >= size, got ", shape, size])
            shape = control_flow_ops.with_dependencies([check], shape)

            limit = shape - size + 1
            offset = tf.random_uniform(tf.shape(shape), dtype=size.dtype, maxval=size.dtype.max, seed=None) % limit

            offset_in = tf.concat([[0], offset], axis=-1)
            size_in = tf.concat([[self.num_frames], size], axis=-1)
            inp = tf.slice(inp, offset_in, size_in)
            offset_gt = tf.concat([[0], offset[:2], [0]], axis=-1)
            size_gt = tf.concat([[1], size[:2], [3]], axis=-1)
            gt = tf.slice(gt, offset_gt, size_gt)

            inp.set_shape([self.num_frames, self.in_size, self.in_size, 3])
            gt.set_shape([1, self.in_size, self.in_size, 3])
            return inp, gt

        def read_data():
            idx0 = self.num_frames // 2  # center
            data_seq = tf.random_crop(self.data_queue, [2, self.num_frames])
            inp = tf.stack([tf.image.decode_png(tf.read_file(data_seq[0][i]), channels=3) for i in range(self.num_frames)])
            gt = tf.stack([tf.image.decode_png(tf.read_file(data_seq[1][idx0]), channels=3)])
            inp, gt = prepprocessing(inp, gt)

            flip = tf.random_uniform((1,3), minval=0.0, maxval=1.0, dtype=tf.float32, seed=None, name=None)  # if training gets worse, comment the data flip part out
            inp = tf.where(flip[0][0]<0.5, inp, inp[:,::-1])
            inp = tf.where(flip[0][1]<0.5,inp, inp[:,:,::-1])
            inp = tf.where(flip[0][2]<0.5,inp, tf.transpose(inp, perm=(0,2,1,3)))
            gt = tf.where(flip[0][0]<0.5, gt, gt[:,::-1])
            gt = tf.where(flip[0][1]<0.5, gt, gt[:,:,::-1])
            gt = tf.where(flip[0][2]<0.5, gt, tf.transpose(gt, perm=(0,2,1,3)))
            print('Input producer shape: ', inp.get_shape(), gt.get_shape())
            return inp, gt
        
        with tf.variable_scope('input'):
            """
            load path from txt
            shuffle
            generate png list
            """
            pathlist = open(self.train_dir, 'rt').read().splitlines()
            random.shuffle(pathlist)
            inList_all = []
            gtList_all = []
            for dataPath in pathlist:
                inList = sorted(glob.glob(op.join(dataPath, 'blur/*.png')))
                gtList = sorted(glob.glob(op.join(dataPath, 'truth/*.png')))
                inList_all.append(inList)  # a list of list: pngs of each video
                gtList_all.append(gtList)
            inList_all = [alist[0:120] for alist in inList_all]  # some 125, some 120, error
            gtList_all = [alist[0:120] for alist in gtList_all]
            inList_all = tf.convert_to_tensor(inList_all, dtype=tf.string)
            gtList_all = tf.convert_to_tensor(gtList_all, dtype=tf.string)

            """
            generate data_queue
            return batch
            """
            self.data_queue = tf.train.slice_input_producer([inList_all, gtList_all], capacity=self.batch_size*2)
            inp, gt = read_data()
            batch_in, batch_gt = tf.train.batch([inp, gt], batch_size=self.batch_size, num_threads=4, capacity=self.batch_size*2)
        return batch_in, batch_gt
            
    def save(self, sess, checkpoint_dir, step):
        if not op.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
        save_path = op.join(checkpoint_dir, "model")
        self.saver.save(sess, save_path, global_step=step)
        print(">>>Saved at %s" % (save_path+"-"+str(step)))

    def load(self, sess, checkpoint_dir, step=None):
        ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
        if ckpt and ckpt.model_checkpoint_path:
            ckpt_name = os.path.basename(ckpt.model_checkpoint_path)  # the last model in the checkpoint
            self.saver.restore(sess, os.path.join(checkpoint_dir, ckpt_name))
            print(">>>Checkpoint: %s loaded" % ckpt_name)
        else:
            print(">>>Checkpoint not exists!!!")

    def build(self):
        H = tf.placeholder(tf.float32, shape=[None, 1, None, None, 3], name='H_truth')  # for train/val
        L_train = tf.placeholder(tf.float32, shape=[self.batch_size, self.num_frames, self.in_size, self.in_size, 3], name='L_train')
        L_eval = tf.placeholder(tf.float32, shape=[self.eval_basz, self.num_frames, self.eval_in_size[0], self.eval_in_size[1], 3], name='L_eval')
        
        enhanced_L_train = self.forward(L_train)
        enhanced_L_eval = self.forward(L_eval)
        
        loss = tf.reduce_mean(tf.sqrt((enhanced_L_train - H)**2 + 1e-6))  # Charbonnier
        eval_mse = tf.reduce_mean((enhanced_L_eval - H)**2, axis=[2,3,4])
        
        self.loss, self.eval_mse = loss, eval_mse
        self.L, self.L_eval, self.H, self.SR = L_train, L_eval, H, enhanced_L_train
        
    def build2(self):
        H2 = tf.placeholder(tf.float32, shape=[None, 1, None, None, 3], name='H_truth2')  # for train/val
        L_train2 = tf.placeholder(tf.float32, shape=[self.batch_size, self.num_frames, self.in_size, self.in_size, 3], name='L_train2')
        L_eval2 = tf.placeholder(tf.float32, shape=[self.eval_basz, self.num_frames, self.eval_in_size[0], self.eval_in_size[1], 3], name='L_eval2')
        
        enhanced_L_train2 = self.forward(L_train2)
        enhanced_L_eval2 = self.forward(L_eval2)
        
        loss2 = tf.reduce_mean(tf.sqrt((enhanced_L_train2 - H2)**2 + 1e-6))  # Charbonnier
        eval_mse2 = tf.reduce_mean((enhanced_L_eval2 - H2)**2, axis=[2,3,4])
        
        self.loss2, self.eval_mse2 = loss2, eval_mse2
        self.L2, self.L_eval2, self.H2, self.SR2 = L_train2, L_eval2, H2, enhanced_L_train2

    def build3(self):
        H3 = tf.placeholder(tf.float32, shape=[None, 1, None, None, 3], name='H_truth3')  # for train/val
        L_train3 = tf.placeholder(tf.float32, shape=[self.batch_size, self.num_frames, self.in_size, self.in_size, 3], name='L_train3')
        L_eval3 = tf.placeholder(tf.float32, shape=[self.eval_basz, self.num_frames, self.eval_in_size[0], self.eval_in_size[1], 3], name='L_eval3')
        
        enhanced_L_train3 = self.forward(L_train3)
        enhanced_L_eval3 = self.forward(L_eval3)
        
        loss3 = tf.reduce_mean(tf.sqrt((enhanced_L_train3 - H3)**2 + 1e-6))  # Charbonnier
        eval_mse3 = tf.reduce_mean((enhanced_L_eval3 - H3)**2, axis=[2,3,4])
        
        self.loss3, self.eval_mse3 = loss3, eval_mse3
        self.L3, self.L_eval3, self.H3, self.SR3 = L_train3, L_eval3, H3, enhanced_L_train3

    def build4(self):
        H4 = tf.placeholder(tf.float32, shape=[None, 1, None, None, 3], name='H_truth4')  # for train/val
        L_train4 = tf.placeholder(tf.float32, shape=[self.batch_size, self.num_frames, self.in_size, self.in_size, 3], name='L_train4')
        L_eval4 = tf.placeholder(tf.float32, shape=[self.eval_basz, self.num_frames, self.eval_in_size[0], self.eval_in_size[1], 3], name='L_eval4')
        
        enhanced_L_train4 = self.forward(L_train4)
        enhanced_L_eval4 = self.forward(L_eval4)
        
        loss4 = tf.reduce_mean(tf.sqrt((enhanced_L_train4 - H4)**2 + 1e-6))  # Charbonnier
        eval_mse4 = tf.reduce_mean((enhanced_L_eval4 - H4)**2, axis=[2,3,4])
        
        self.loss4, self.eval_mse4 = loss4, eval_mse4
        self.L4, self.L_eval4, self.H4, self.SR4 = L_train4, L_eval4, H4, enhanced_L_train4

    def eval(self):
        print('>>>>>>>>>Evaluating...')

        """
        list all pngs
        """
        filenames = open(self.eval_dir, 'rt').read().splitlines()
        gt_list = [sorted(glob.glob(op.join(f, 'truth', '*.png'))) for f in filenames]
        inp_list = [sorted(glob.glob(op.join(f, 'blur', '*.png'))) for f in filenames]

        """
        load sess
        """
        if not hasattr(self, 'sess'):
            sess = tf.Session()
            self.load(sess, self.model_dir)
        else:
            sess = self.sess
            
        """
        eval
        """
        inp_h, inp_w = self.eval_in_size
        batch_gt = []
        batch_inp = []
        mse_acc = None
        total_batch = np.sum(np.array([len(list(range(self.num_frames//2, len(alist)-self.num_frames, self.eval_gap))) for alist in gt_list]))
        pbar = tqdm(range(total_batch), ncols=80, desc='batch')
        for ite_vid, gtlist in enumerate(gt_list):
            inplist = inp_list[ite_vid]
            nfs = len(gtlist)
            for idx0 in range(self.num_frames//2, nfs-self.num_frames, self.eval_gap):  # idx0 is center frame index
                pbar.update(1)
                """
                load all pngs
                crop, pre-process
                stack
                """
                index = np.array([i for i in range(idx0-self.num_frames//2, idx0+self.num_frames//2+1)])
                index = np.clip(index, 0, nfs-1).tolist()
                gt = [cv2_imread(gtlist[i]) for i in index]
                inp = [cv2_imread(inplist[i]) for i in index]
                th, tw, _ = inp[0].shape
                sh, sw = th//2 - inp_h//2, tw//2 - inp_w//2
                gt = [i[sh:inp_h+sh, sw:inp_w+sw, :].astype(np.float32) / 255.0 for i in gt]
                inp = [i[sh:inp_h+sh, sw:inp_w+sw, :].astype(np.float32) / 255.0 for i in inp]
                batch_gt.append(np.stack(gt, axis=0))
                batch_inp.append(np.stack(inp, axis=0))
                
                if len(batch_gt) == self.eval_basz:
                    batch_gt = np.stack(batch_gt, 0)
                    batch_inp = np.stack(batch_inp, 0)
                    """
                    eval mse
                    record
                    """
                    mse_val = sess.run(self.eval_mse, feed_dict={
                        self.L_eval: batch_inp,
                        self.H: batch_gt[:, self.num_frames//2:self.num_frames//2+1]})
                    if mse_acc is None:
                        mse_acc = mse_val
                    else:
                        mse_acc = np.concatenate([mse_acc, mse_val], axis=0)
                    
                    """
                    empty batch
                    """
                    batch_gt = []
                    batch_inp = []
        pbar.close()

        """
        eval psnr
        display
        """  
        psnr_acc = 10 * np.log10(1.0 / mse_acc)
        mse_avg = np.mean(mse_acc, axis=0)
        psnr_avg = np.mean(psnr_acc, axis=0)
        for i in range(mse_avg.shape[0]):
            tf.summary.scalar('val_mse{}'.format(i), tf.convert_to_tensor(mse_avg[i], dtype=tf.float32))
        print('Eval PSNR: %.3f, MSE: %.6f' % (psnr_avg, mse_avg))
        
        """
        write to log file
        """
        with open(self.log_path, 'a+') as f:
            mse_avg = (mse_avg*1e6).astype(np.int64) / (1e6)
            psnr_avg = (psnr_avg*1e6).astype(np.int64) / (1e6)
            f.write('{'+'"Iter": {} , "PSNR": {}, "MSE": {}'.format(self.global_step, psnr_avg.tolist(), mse_avg.tolist())+'}\n')

    def train(self):
        """when retrain in main.py, NotFoundError occurs 
        """
        tf.reset_default_graph()  # cause some error?

        """ywz
        average loss
        """
        def average_gradients(tower_grads):
            average_grads = []
            for grad_and_vars in zip(*tower_grads):
                grads = []
                for g, _ in grad_and_vars:
                    expend_g = tf.expand_dims(g, 0)
                    grads.append(expend_g)
                grad = tf.concat(grads, 0)
                grad = tf.reduce_mean(grad, 0)
                v = grad_and_vars[0][1]
                grad_and_var = (grad, v)
                average_grads.append(grad_and_var)
            return average_grads

        with tf.device("/cpu:0"):  # define on cpu
            """
            data
            """
            LR, HR = self.double_input_producer()
            
            """ywz
            build on 4 gpus
            cal grad
            """
            tower_grads = []  # store gradients of 4 gpu data
            lr = tf.train.polynomial_decay(self.learning_rate, self.global_step, self.decay_step, end_learning_rate=self.end_lr, power=1.)
            opt = tf.train.AdamOptimizer(lr)
            with tf.variable_scope(tf.get_variable_scope()):
                for i in range(self.num_gpus):
                    with tf.device('/gpu:{}'.format(i)):
                        if i==0:    
                            self.build()
                            tf.get_variable_scope().reuse_variables()  # reuse vars for parallel
                            
                            """
                            cal paras
                            """
                            vars_all=tf.trainable_variables()
                            print('Params num: ', get_num_params(vars_all))
                            
                            grads = opt.compute_gradients(self.loss)
                            tower_grads.append(grads)
                        elif i==1:
                            self.build2()
                            tf.get_variable_scope().reuse_variables()  # reuse vars for parallel
                            
                            grads = opt.compute_gradients(self.loss2)
                            tower_grads.append(grads)
                        elif i==2:
                            self.build3()
                            tf.get_variable_scope().reuse_variables()  # reuse vars for parallel
                            grads = opt.compute_gradients(self.loss3)
                            tower_grads.append(grads)
                        elif i==3:
                            self.build4()
                            tf.get_variable_scope().reuse_variables()  # reuse vars for parallel
                            grads = opt.compute_gradients(self.loss4)
                            tower_grads.append(grads)
            
            """ywz
            define lr and optizer
            merge gradients to one, and update
            """
            grads = average_gradients(tower_grads)
            train_op = opt.apply_gradients(grads)

            """
            define sess
            init vars
            """
            config = tf.ConfigProto() 
            config.gpu_options.allow_growth = True
            sess = tf.Session(config=config) 
            self.sess = sess
            sess.run(tf.global_variables_initializer())
            
            """
            define saver
            reload
            """
            self.saver = tf.train.Saver(max_to_keep=50, keep_checkpoint_every_n_hours=1)
            if self.reload:
                self.load(sess, self.model_dir)

            """
            ???
            """
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess=sess, coord=coord)

            """
            train step by step
            """

            start_time = time.time()
            for step in range(self.max_step):
                if (step > 0) and (step % self.disp_step == 0):
                    print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()), 'Step:{}, loss:{}'.format(step, loss_v))
                    
                if (step % self.eval_step == 0) and (step != 0):
                    if step > 0:
                        self.save(sess, self.model_dir, step)
                    
                    cost_time = time.time() - start_time
                    print('train %d steps cost %d s.' % (self.eval_step, cost_time))
                    
                    start_time = time.time()
                    self.eval()
                    cost_time = time.time() - start_time
                    print('val cost %d s.' % cost_time)

                    start_time = time.time() # re init

                """ywz
                load data
                """
                lr1, hr = sess.run([LR,HR])
                if self.num_gpus>1:
                    lr2, hr2 = sess.run([LR,HR])
                if self.num_gpus>2:
                    lr3, hr3 = sess.run([LR,HR])
                if self.num_gpus>3:
                    lr4, hr4 = sess.run([LR,HR])
                
                """ywz
                run
                """
                if self.num_gpus ==1:
                    _,loss_v = sess.run([train_op,self.loss], feed_dict={self.L:lr1, self.H:hr})
                elif self.num_gpus ==2:
                    _,loss_v = sess.run([train_op,self.loss], feed_dict={self.L:lr1, self.H:hr,self.L2:lr2, self.H2:hr2})
                elif self.num_gpus ==3:
                    _,loss_v = sess.run([train_op,self.loss], feed_dict={self.L:lr1, self.H:hr,self.L2:lr2, self.H2:hr2,self.L3:lr3, self.H3:hr3})
                elif self.num_gpus ==4:
                    _,loss_v = sess.run([train_op,self.loss], feed_dict={self.L:lr1, self.H:hr,self.L2:lr2, self.H2:hr2,self.L3:lr3, self.H3:hr3,self.L4:lr4, self.H4:hr4})

                self.global_step += 1  # for saving model

                """
                collasp
                """
                if (step > (self.eval_step//2)) and (loss_v > 10):
                    print('>>>>>Model collapsed with loss={}.'.format(loss_v))
                    print('Re-run main.py simply. If collapsed frequently, changed lr and end_lr to 0.1x.')
                    return True

    def test_video(self, inp_idx, save_dir, reuse=False):
        test_bs = self.test_bs
        cut_time = self.cut_time

        """
        load all pngs of this damaged video into lrs
        /225.
        """
        print("\n>>>>>>>>>>>>>>>>>>loding pngs...")
        ###ywz
        # imgs = sorted(glob.glob(op.join(inp_path, '*.png')))
        # lrs = [cv2_imread(i)/255. for i in imgs]  # [np.zeros((1080,1920,3)) for i in range(2)]
        # last_inp_idx = inp_idx - 1
        # if last_inp_idx < 0:
        #     last_inp_idx = 0
        # else:
        #     last_inp_idx = self.dir_vid_index_list[last_inp_idx-1]
        # temp_inp_idx = self.dir_vid_index_list[inp_idx] 
        # 加载索引
        last_inp_idx = self.dir_vid_index_list[inp_idx]
        next_inp_idx = self.dir_vid_index_list[inp_idx+1]
        # 同样是RGB且归一化[0,1]
        lrs = np.array([read_img(self.lmdb_env,i,self.lmdb_size) for i in self.key_paths[last_inp_idx:next_inp_idx]])
        
        ####
        nfs = len(lrs)
        h, w, c = lrs[0].shape
        print("lrs loaded: %d * (%d %d %d)" % (nfs, h, w, c))

        """
        cut imgs in case of OOM
        """
        print("\n>>>>>>>>>>>>>>>>>>cutting pngs...")
        cut_part = 4**cut_time
        for ite in range(cut_time):
            tmp = []
            th, tw, tc = lrs[0].shape
            for lr in lrs:
                tmp.append(lr[:th//2, :tw//2, :])
                tmp.append(lr[:th//2, tw//2:, :])
                tmp.append(lr[th//2:, :tw//2, :])
                tmp.append(lr[th//2:, tw//2:, :])
            lrs = tmp[:]
        lrs = np.array(lrs)
        del tmp
        nfs = len(lrs)
        h, w, c = lrs[0].shape
        print("cut done: %d * (%d %d %d)" % (nfs, h, w, c))

        """
        define lr -> hr
        """
        L_test = tf.placeholder(tf.float32, shape=[test_bs, self.num_frames, h, w, c], name='L_test')
        H_test = self.forward(L_test)

        """
        generate index_list for each frame
        """
        index_lists = []
        for i in range(nfs):
            index_list = list(range(
                i-self.num_frames//2*cut_part,
                i+self.num_frames//2*cut_part+1,
                cut_part
                ))
            index_list = np.clip(index_list, 0, nfs-1).tolist()
            index_lists.append(index_list)

        """
        init sess and load checkpoint if not reuse
        """
        if not reuse:
            config = tf.ConfigProto()
            config.gpu_options.allow_growth = True
            sess = tf.Session(config=config)
            self.sess=sess
            sess.run(tf.global_variables_initializer())
            self.saver = tf.train.Saver(max_to_keep=100, keep_checkpoint_every_n_hours=1)
            self.load(sess, self.model_dir, step=None)  # automatically load the last model

        """
        init save dir for pngs of this video
        """
        if not op.exists(save_dir):
            os.makedirs(save_dir)
        print('Save at {}'.format(save_dir))
        
        """
        run batch by batch
        """
        print("\n>>>>>>>>>>>>>>>>>>running...")
        total_test_time = []  # time
        img_list = []
        num_ite = ceil(nfs / test_bs)
        pbar = tqdm(range(num_ite), ncols=80, desc='batch')
        for i in pbar:
            """
            prepare damaged input batch: L_test
            """
            inp_list = []
            for j in range(i*test_bs, (i+1)*test_bs):
                index_list = index_lists[j]
                inp_list.append(np.array([lrs[k] for k in index_list]))  # (nf, h, w, c)
            inp_list = np.array(inp_list)  # (test_bs, nf, h, w, c)

            """
            run this batch
            """
            start_time = time.time()  # time
            h_batch = self.sess.run(
                H_test,
                feed_dict={L_test:inp_list}
                )  # (test_bs, 1, h w c)
            total_test_time.append(time.time() - start_time)  # time

            """
            post-precess and record this batch
            maybe save an img
            """
            for j in range(test_bs):
                # post-process
                img = h_batch[j][0] * 255.
                img = np.clip(img, 0, 255)
                img = np.round(img, 0).astype(np.uint8)

                # record
                img_list.append(img)

                # cat and save
                acc_num = i * test_bs + j
                if (acc_num+1) % cut_part == 0:
                    real_num = (acc_num+1) // cut_part - 1
                    for ite_cat in range(cut_time):
                        th, tw, tc = img_list[0].shape
                        tmp_cat_list = []
                        for ite_ite_cat in range(len(img_list) // 4):
                            tmp_cat_img = np.zeros((th*2, tw*2, tc), dtype=np.uint8)
                            tmp_cat_img[:th, :tw, :] = img_list[ite_ite_cat*4+0]
                            tmp_cat_img[:th, tw:, :] = img_list[ite_ite_cat*4+1]
                            tmp_cat_img[th:, :tw, :] = img_list[ite_ite_cat*4+2]
                            tmp_cat_img[th:, tw:, :] = img_list[ite_ite_cat*4+3]
                            tmp_cat_list.append(tmp_cat_img)
                        img_list = tmp_cat_list[:]
                    cat_img = img_list[0]
                    cv2_imsave(join(save_dir, '{:0>4}.png'.format(real_num)), cat_img)
                    img_list = []
        pbar.close()

        """
        cal time and fps
        """
        if max_frame > 0:
            print("\n>>>>>>>>>>>>>>>>>>")
            total_test_time = np.array(total_test_time)
            total_test_hour = np.sum(total_test_time) / 3600
            ave_test_s = np.mean(total_test_time[1:]) / test_bs
            print('consumed %.1f h in total, ave. %.1f s per frame' % (total_test_hour, ave_test_s))

    def test_videos(self,
            root_dir, save_dir , save_tag,
            start_vid=0, end_vid=149,
            ):
        """
        list and sorted all video folders into dir_vid_list
        cut into [start_vid: end_vid+1], start from any given index
        root_dir: 'xxxx.lmdb'
        """
        # test_dir = op.join(root_dir, 'test_damage_A')
        # dir_vid_list = sorted(glob.glob(op.join(test_dir, '*')))
        # dir_vid_list = [k for k in dir_vid_list if os.path.isdir(k)]
        # dir_vid_list = dir_vid_list[start_vid: end_vid+1]

        self.key_paths,_ = get_image_paths('lmdb',root_dir)
        self.lmdb_env =  lmdb.open(root_dir, readonly=True, lock=False, readahead=False,meminit=False)
        self.lmdb_size = (3,1080,1920)
        self.dir_vid_index_list = [] #到第几个换

        #############################################################
        # temp_key_head = '000_' #'000_00000000'
        # for idx,temp_key in enumerate(self.key_paths):
        #     if not temp_key_head in temp_key:
        #         self.dir_vid_index_list.append(idx)
        #     else:
        #         temp_key_head = temp_key.split('_')[0] + '_'
        
        last_key_head = ''
        for idx,temp_key in enumerate(self.key_paths):
            temp_key_head = temp_key.split('_')[0] 
            if temp_key_head != last_key_head:
                last_key_head = temp_key_head
                self.dir_vid_index_list.append(idx) #start_id 第一个是0
        #last_one
        self.dir_vid_index_list.append(len(self.key_paths))
        #############################################################
            


        

        """
        test and save each video into a single folder (consisting pngs of this vid)
        """
        reuse = False  # for the first video, load checkpoint
        # save_dir_pre = "/".join(test_dir.split("/")[:-1]) + "/refine/" + save_tag
        save_dir_pre = save_dir + save_tag
        for idx  in range(start_vid,(end_vid+1)):
            if idx > start_vid:
                reuse = True # for the video with index > 1, reuse checkpoint
            # inp_path = op.join(test_dir, dir_vid)


            # video_index = dir_vid.split("/")[-1].split("_")[2]  #
            base_index = 0
            video_index = idx + base_index
            video_index = (str)(video_index).zfill(4)

            save_dir = save_dir_pre + "/mg_refine_" + video_index #
            self.test_video(idx, save_dir, test_bs, cut_time, reuse=reuse)
