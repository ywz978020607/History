#使用精简版的net.py from 训练
import glob, os
import numpy as np
import tflearn
import tensorflow as tf
import tensorflow.contrib.slim as slim
from skimage.measure import compare_psnr, compare_ssim
import net_MFCNN

from tensorflow.python.client import timeline
ywz_times = -1

#run cmd: python main_test_ywz_timeline.py 480p 0 0 10

#changed by ywz

### Settings
dir_CmpVideo = "Videos/cmp"
dir_RawVideo = "Videos/ori"
dir_PQFLabel = "Data"
dir_model = "Models"

file_object = open("record_test.txt", 'w')

os.environ['CUDA_VISIBLE_DEVICES'] = '1'



"""
If there exist frames with different QPs in a video, you can record the QP of each frame in a list. And they will be enhanced by models with corresponding QP.
ApprQP: approximate QP. Because we have only 5 QP models (22,27,32,37,42), so we should record the nearest QP for each QP in a video. 
For example, if the QPs for 4 frames are: [21,28,25,33], then we should record: [22,27,27,32], and save it as "ApprQP_BasketballPass_416x240_500.npy".
"""
# dir_ApprQP = "Data"
# opt_QPLabel = True
"""
If all frames in a video are with the same QP:
"""
QP_video = 32 # for the test video in this demo(BasketballPass), all frames are with QP32. Record the QP_video here.
opt_QPLabel = False # no need for uploading QP label.



QP_list = [22,27,32,37,42]
net1_list = [37,42] # network1 for QP37 and 42, network2 for other QPs. See net_MFCNN for details.

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # only show error and warning
config = tf.ConfigProto(allow_soft_placement = True) # if GPU is not usable, then turn to CPU automatically

BATCH_SIZE = 1
CHANNEL = 1

### List all cmp test videos
CmpVideo_path_list = glob.glob(os.path.join(dir_CmpVideo, "*.yuv"))
num_CmpVideo = len(CmpVideo_path_list)


####copy from train

def transformer(batch, chan, flow, U , out_size, name='SpatialTransformer', **kwargs):

    def _repeat(x, n_repeats):
        with tf.variable_scope('_repeat'):
            rep = tf.transpose(
                tf.expand_dims(tf.ones(shape=tf.stack([n_repeats, ])), 1), [1, 0])
            rep = tf.cast(rep, 'int32')
            x = tf.matmul(tf.reshape(x, (-1, 1)), rep)
            return tf.reshape(x, [-1])

    def _repeat2(x, n_repeats):
        with tf.variable_scope('_repeat'):
            rep = tf.expand_dims(tf.ones(shape=tf.stack([n_repeats, ])), 1)
            rep = tf.cast(rep, 'int32')
            x = tf.matmul(rep, tf.reshape(x, (1, -1)))
            return tf.reshape(x, [-1])

    def _interpolate(im, x, y, out_size):
        with tf.variable_scope('_interpolate'):
            # constants
            num_batch = tf.shape(im)[0]
            height = tf.shape(im)[1]
            width = tf.shape(im)[2]
            channels = tf.shape(im)[3]

            x = tf.cast(x, 'float32')
            y = tf.cast(y, 'float32')
            height_f = tf.cast(height, 'float32')
            width_f = tf.cast(width, 'float32')
            out_height = out_size[0]
            out_width = out_size[1]
            zero = tf.zeros([], dtype='int32')
            max_y = tf.cast(tf.shape(im)[1] - 1, 'int32')
            max_x = tf.cast(tf.shape(im)[2] - 1, 'int32')

            x = tf.cast(_repeat2(tf.range(0, width), height * num_batch), 'float32') + x * 64
            y = tf.cast(_repeat2(_repeat(tf.range(0, height), width), num_batch), 'float32') + y * 64

            # do sampling
            x0 = tf.cast(tf.floor(x), 'int32')
            x1 = x0 + 1
            y0 = tf.cast(tf.floor(y), 'int32')
            y1 = y0 + 1

            x0 = tf.clip_by_value(x0, zero, max_x)
            x1 = tf.clip_by_value(x1, zero, max_x)
            y0 = tf.clip_by_value(y0, zero, max_y)
            y1 = tf.clip_by_value(y1, zero, max_y)
            dim2 = width
            dim1 = width*height
            base = _repeat(tf.range(num_batch)*dim1, out_height*out_width)

            base_y0 = base + y0*dim2
            base_y1 = base + y1*dim2
            idx_a = base_y0 + x0
            idx_b = base_y1 + x0
            idx_c = base_y0 + x1
            idx_d = base_y1 + x1

            # use indices to lookup pixels in the flat image and restore
            # channels dim
            im_flat = tf.reshape(im, tf.stack([-1, channels]))
            im_flat = tf.cast(im_flat, 'float32')
            Ia = tf.gather(im_flat, idx_a)
            Ib = tf.gather(im_flat, idx_b)
            Ic = tf.gather(im_flat, idx_c)
            Id = tf.gather(im_flat, idx_d)

            # and finally calculate interpolated values
            x0_f = tf.cast(x0, 'float32')
            x1_f = tf.cast(x1, 'float32')
            y0_f = tf.cast(y0, 'float32')
            y1_f = tf.cast(y1, 'float32')
            wa = tf.expand_dims(((x1_f-x) * (y1_f-y)), 1)
            wb = tf.expand_dims(((x1_f-x) * (y-y0_f)), 1)
            wc = tf.expand_dims(((x-x0_f) * (y1_f-y)), 1)
            wd = tf.expand_dims(((x-x0_f) * (y-y0_f)), 1)
            output = tf.add_n([wa*Ia, wb*Ib, wc*Ic, wd*Id])
            return output

    def _meshgrid(height, width):
        with tf.variable_scope('_meshgrid'):
            # This should be equivalent to:
            #  x_t, y_t = np.meshgrid(np.linspace(-1, 1, width),
            #                         np.linspace(-1, 1, height))
            #  ones = np.ones(np.prod(x_t.shape))
            #  grid = np.vstack([x_t.flatten(), y_t.flatten(), ones])
            x_t = tf.matmul(tf.ones(shape=tf.stack([height, 1])),
                            tf.transpose(tf.expand_dims(tf.linspace(-1.0, 1.0, width), 1), [1, 0]))
            y_t = tf.matmul(tf.expand_dims(tf.linspace(-1.0, 1.0, height), 1),
                            tf.ones(shape=tf.stack([1, width])))

            x_t_flat = tf.reshape(x_t, (1, -1))
            y_t_flat = tf.reshape(y_t, (1, -1))

            ones = tf.ones_like(x_t_flat)
            grid = tf.concat(axis=0, values=[x_t_flat, y_t_flat, ones])
            return grid

    def _transform(x_s, y_s, input_dim, out_size):
        with tf.variable_scope('_transform'):
            num_batch = tf.shape(input_dim)[0]
            height = tf.shape(input_dim)[1]
            width = tf.shape(input_dim)[2]
            num_channels = tf.shape(input_dim)[3]

            height_f = tf.cast(height, 'float32')
            width_f = tf.cast(width, 'float32')
            out_height = out_size[0]
            out_width = out_size[1]

            x_s_flat = tf.reshape(x_s, [-1])
            y_s_flat = tf.reshape(y_s, [-1])

            input_transformed = _interpolate(
                input_dim, x_s_flat, y_s_flat,
                out_size)

            output = tf.reshape(
                input_transformed, tf.stack([batch, out_height, out_width, chan]))
            return output

    with tf.variable_scope(name):
        dx, dy = tf.split(flow, 2, 3)
        output = _transform(dx, dy, U, out_size)
        return output


def warp_img(batch_size, imga, imgb, reuse, scope='easyflow'):

    n, h, w, c = imga.get_shape().as_list()

    with tf.variable_scope(scope, reuse=reuse):

        with slim.arg_scope([slim.conv2d], activation_fn=tflearn.activations.prelu,
                            weights_initializer=tf.contrib.layers.xavier_initializer(uniform=True),
                            biases_initializer=tf.constant_initializer(0.0)), \
             slim.arg_scope([slim.conv2d_transpose], activation_fn=tflearn.activations.prelu,
                            weights_initializer=tf.contrib.layers.xavier_initializer(uniform=True),
                            biases_initializer=tf.constant_initializer(0.0)):
            inputs = tf.concat([imga, imgb], 3, name='flow_inp')
            c1 = slim.conv2d(inputs, 24, [5, 5], stride=2, scope='c1')
            c2 = slim.conv2d(c1, 24, [3, 3], scope='c2')
            c3 = slim.conv2d(c2, 24, [5, 5], stride=2, scope='c3')
            c4 = slim.conv2d(c3, 24, [3, 3], scope='c4')
            c5 = slim.conv2d(c4, 32, [3, 3], activation_fn=tf.nn.tanh, scope='c5')
            c5_hr = tf.reshape(c5, [n, int(h / 4), int(w / 4), 2, 4, 4])
            c5_hr = tf.transpose(c5_hr, [0, 1, 4, 2, 5, 3])
            c5_hr = tf.reshape(c5_hr, [n, h, w, 2])
            img_warp1 = transformer(batch_size, c, c5_hr, imgb, [h, w])

            c5_pack = tf.concat([inputs, c5_hr, img_warp1], 3, name='cat')
            s1 = slim.conv2d(c5_pack, 24, [5, 5], stride=2, scope='s1')
            s2 = slim.conv2d(s1, 24, [3, 3], scope='s2')
            s3 = slim.conv2d(s2, 24, [3, 3], scope='s3')
            s4 = slim.conv2d(s3, 24, [3, 3], scope='s4')
            s5 = slim.conv2d(s4, 8, [3, 3], activation_fn=tf.nn.tanh, scope='s5')
            s5_hr = tf.reshape(s5, [n, int(h / 2), int(w / 2), 2, 2, 2])
            s5_hr = tf.transpose(s5_hr, [0, 1, 4, 2, 5, 3])
            s5_hr = tf.reshape(s5_hr, [n, h, w, 2])
            uv = c5_hr + s5_hr
            img_warp2 = transformer(batch_size, c, uv, imgb, [h, w])

            s5_pack = tf.concat([inputs, uv, img_warp2], 3, name='cat2')
            a1 = slim.conv2d(s5_pack, 24, [3, 3], scope='a1')
            a2 = slim.conv2d(a1, 24, [3, 3], scope='a2')
            a3 = slim.conv2d(a2, 24, [3, 3], scope='a3')
            a4 = slim.conv2d(a3, 24, [3, 3], scope='a4')
            a5 = slim.conv2d(a4, 2, [3, 3], activation_fn=tf.nn.tanh, scope='a5')
            a5_hr = tf.reshape(a5, [n, h, w, 2, 1, 1])
            a5_hr = tf.transpose(a5_hr, [0, 1, 4, 2, 5, 3])
            a5_hr = tf.reshape(a5_hr, [n, h, w, 2])
            uv2 = a5_hr + uv
            img_warp3 = transformer(batch_size, c, uv2, imgb, [h, w])

            tf.summary.histogram("c5_hr", c5_hr)
            tf.summary.histogram("s5_hr", s5_hr)
            tf.summary.histogram("uv", uv)
            tf.summary.histogram("a5", uv)
            tf.summary.histogram("uv2", uv)

    return img_warp3


#####


def y_import(video_path, height_frame, width_frame, nfs, startfrm):
    """Import Y channel from a yuv video.

    startfrm: start from 0
    return: (nfs * height * width), dtype=uint8."""

    fp = open(video_path,'rb')

    # target at startfrm
    blk_size = int(height_frame * width_frame * 3 / 2)
    fp.seek(blk_size * startfrm, 0)

    d0 = height_frame // 2
    d1 = width_frame // 2

    Yt = np.zeros((height_frame, width_frame), dtype=np.uint8) # 0-255

    for ite_frame in range(nfs):

        for m in range(height_frame):
            for n in range(width_frame):
                Yt[m,n] = ord(fp.read(1))
        for m in range(d0):
            for n in range(d1):
                fp.read(1)
        for m in range(d0):
            for n in range(d1):
                fp.read(1)

        if ite_frame == 0:
            Y = Yt[np.newaxis, :, :]
        else:
            Y = np.vstack((Y, Yt[np.newaxis, :, :]))

    fp.close()
    return Y


def return_PQFIndices(PQF_label, QP, ApprQP_label):
    """Find all PQFs and their pre/sub PQFs pertain to this QP."""

    PQF_indices = [i for i in range(len(PQF_label)) if PQF_label[i] == 1]
    
    ApprQPLabel_PQF = [ApprQP_label[i] for i in range(len(ApprQP_label)) if i in PQF_indices]

    PQF_order_part = [o for o in range(len(ApprQPLabel_PQF)) if ApprQPLabel_PQF[o] == QP]
    PQFIndex_list_part = [PQF_indices[o] for o in range(len(PQF_indices)) if o in PQF_order_part]
    
    if len(PQFIndex_list_part) == 0:
        return [],[],[]
        
    num_PQF = len(PQFIndex_list_part)
    
    CmpPQFIndex_list_part = PQFIndex_list_part.copy()
    PrePQFIndex_list_part = PQFIndex_list_part[0: (num_PQF - 1)]
    SubPQFIndex_list_part = PQFIndex_list_part[1: num_PQF]
    
    PrePQFIndex_list_part = [PQFIndex_list_part[0]] + PrePQFIndex_list_part
    SubPQFIndex_list_part.append(PQFIndex_list_part[-1])
    
    return PrePQFIndex_list_part, CmpPQFIndex_list_part, SubPQFIndex_list_part
    

def return_NPIndices(PQF_label, QP, ApprQP_label):
    """Find all non-PQFs and their pre/sub PQFs pertain to this QP."""

    PQFIndex_list = [i for i in range(len(PQF_label)) if PQF_label[i] == 1]

    # Find unqualified non-PQFs and their sub PQFs. Pre PQFs are themselves.
    NonPQFIndex_list = [i for i in range(len(PQF_label)) if (PQF_label[i] == 0) and (i < PQFIndex_list[0])]
    PrePQFIndex_list = NonPQFIndex_list.copy()
    SubPQFIndex_list = [PQFIndex_list[0]] * len(NonPQFIndex_list)
    
    # Find qualified non-PQFs and their pre/sub PQFs.
    NonPQFIndex_list_good = [i for i in range(len(PQF_label)) if (PQF_label[i] == 0) and (i > PQFIndex_list[0]) and (i < PQFIndex_list[-1])]
    NonPQFIndex_list += NonPQFIndex_list_good
    num_NonPQF = len(NonPQFIndex_list_good)
    for ite_NonPQF in range(num_NonPQF):
        
        index_NonPQF = NonPQFIndex_list_good[ite_NonPQF]
        
        for ite_PQF in range(len(PQFIndex_list) - 1):
            
            if (PQFIndex_list[ite_PQF] < index_NonPQF) and (PQFIndex_list[ite_PQF + 1] > index_NonPQF):
            
                PrePQFIndex_list.append(PQFIndex_list[ite_PQF])
                SubPQFIndex_list.append(PQFIndex_list[ite_PQF + 1])
                break
                
    # Find unqualified non-PQFs and their sub PQFs. Sub PQFs are themselves.
    NonPQFIndex_list_bad = [i for i in range(len(PQF_label)) if (PQF_label[i] == 0) and (i > PQFIndex_list[-1])]
    NonPQFIndex_list += NonPQFIndex_list_bad
    PrePQFIndex_list += [PQFIndex_list[-1]] * len(NonPQFIndex_list_bad)
    SubPQFIndex_list += NonPQFIndex_list_bad
          
    # Find non-PQFs pertain to this QP      
    ApprQPLabel_nonPQF = [ApprQP_label[i] for i in range(len(ApprQP_label)) if i in NonPQFIndex_list]

    NonPQF_order_part = [o for o in range(len(ApprQPLabel_nonPQF)) if ApprQPLabel_nonPQF[o] == QP]
    NonPQFIndex_list_part = [NonPQFIndex_list[o] for o in range(len(NonPQFIndex_list)) if o in NonPQF_order_part]

    if len(NonPQFIndex_list_part) == 0:
        return [],[],[]
    
    PrePQFIndex_list_part = [PrePQFIndex_list[o] for o in range(len(PrePQFIndex_list)) if o in NonPQF_order_part]
    SubPQFIndex_list_part = [SubPQFIndex_list[o] for o in range(len(SubPQFIndex_list)) if o in NonPQF_order_part]   
                
    return PrePQFIndex_list_part, NonPQFIndex_list_part, SubPQFIndex_list_part


def isplane(frame):
    """Detect black frames or other plane frames."""

    tmp_array = np.squeeze(frame).reshape([-1])

    if all(tmp_array[1:] == tmp_array[:-1]): # all values in this frame are equal
        return True
    else:
        return False

#ywz_timeline
def func_enhance(dir_model_pre, QP, PreIndex_list, CmpIndex_list, SubIndex_list):
    """Enhance PQFs or non-PQFs, record dpsnr, dssim and enhanced frames."""
    #ywz
    global ywz_times

    global enhanced_list, sum_dpsnr, sum_dssim
    
    tf.reset_default_graph()

    ### Defind enhancement process
    x1 = tf.placeholder(tf.float32, [BATCH_SIZE, height, width, CHANNEL])  # previous
    x2 = tf.placeholder(tf.float32, [BATCH_SIZE, height, width, CHANNEL])  # current
    x3 = tf.placeholder(tf.float32, [BATCH_SIZE, height, width, CHANNEL])  # subsequent
        
    if QP in net1_list:
        is_training = tf.placeholder_with_default(False, shape=())
    
    x1to2 = warp_img(BATCH_SIZE, x2, x1, False)
    x3to2 = warp_img(BATCH_SIZE, x2, x3, True)
    
    if QP in net1_list:
        x2_enhanced = net_MFCNN.network(x1to2, x2, x3to2, is_training)
    else:
        x2_enhanced = net_MFCNN.network2(x1to2, x2, x3to2)
    
    saver = tf.train.Saver()
    
    with tf.Session(config = config) as sess:
        # ywz
        if ywz_times==0:
            options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
        #

        # Restore model
        # model_path = os.path.join(dir_model_pre, "model_step2.ckpt-" + str(QP))
        model_path = os.path.join(dir_model_pre, "model_step2.ckpt-0")

        # saver.restore(sess, model_path)
        module_file = tf.train.latest_checkpoint(model_path)
        # with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        if module_file is not None:
            saver.restore(sess, module_file)



        nfs = len(CmpIndex_list)
        
        sum_dpsnr_part = 0.0
        sum_dssim_part = 0.0
    
        for ite_frame in range(nfs):
          
            # Load frames
            pre_frame = y_import(CmpVideo_path, height, width, 1, PreIndex_list[ite_frame])[:,:,:,np.newaxis] / 255.0
            cmp_frame = y_import(CmpVideo_path, height, width, 1, CmpIndex_list[ite_frame])[:,:,:,np.newaxis] / 255.0
            sub_frame = y_import(CmpVideo_path, height, width, 1, SubIndex_list[ite_frame])[:,:,:,np.newaxis] / 255.0
            
            # if cmp frame is plane?
            if isplane(cmp_frame):
                continue

            # if PQF frames are plane?
            if isplane(pre_frame):
                 pre_frame = np.copy(cmp_frame)
            if isplane(sub_frame):
                 sub_frame = np.copy(cmp_frame)


            # ywz
            if ywz_times==0:
                run_metadata = tf.RunMetadata()
                # Enhance
                if QP in net1_list:
                    enhanced_frame = sess.run(x2_enhanced,options = options, feed_dict={x1:pre_frame, x2:cmp_frame, x3:sub_frame, is_training:False}, run_metadata=run_metadata)
                else:
                    enhanced_frame = sess.run(x2_enhanced,options = options, feed_dict={x1:pre_frame, x2:cmp_frame, x3:sub_frame}, run_metadata=run_metadata)

            else:
                # Enhance
                if QP in net1_list:
                    enhanced_frame = sess.run(x2_enhanced, feed_dict={x1: pre_frame, x2: cmp_frame, x3: sub_frame,is_training: False})
                else:
                    enhanced_frame = sess.run(x2_enhanced, feed_dict={x1: pre_frame, x2: cmp_frame, x3: sub_frame})

            #
            # ywz
            # timeline record
            # Create the Timeline object, and write it to a json file
            if ywz_times==0:
                fetched_timeline = timeline.Timeline(run_metadata.step_stats)
                chrome_trace = fetched_timeline.generate_chrome_trace_format()
                with open("timeline/timeline_" + str(ite_frame) + ".json", 'w') as f:
                    f.write(chrome_trace)
            #


            # Record for output video
            enhanced_list[CmpIndex_list[ite_frame]] = np.squeeze(enhanced_frame)
            
            # Evaluate and accumulate dpsnr
            raw_frame = np.squeeze(y_import(RawVideo_path, height, width, 1, CmpIndex_list[ite_frame])) / 255.0
            cmp_frame = np.squeeze(cmp_frame)
            enhanced_frame = np.squeeze(enhanced_frame)
            
            raw_frame = np.float32(raw_frame)
            cmp_frame = np.float32(cmp_frame)
            
            psnr_ori = compare_psnr(cmp_frame, raw_frame, data_range=1.0)
            psnr_aft = compare_psnr(enhanced_frame, raw_frame, data_range=1.0)

            ssim_ori = compare_ssim(cmp_frame, raw_frame, data_range=1.0)
            ssim_aft = compare_ssim(enhanced_frame, raw_frame, data_range=1.0)
            
            sum_dpsnr_part += psnr_aft - psnr_ori
            sum_dssim_part += ssim_aft - ssim_ori

            print("\r %d | %d at QP = %d" % (ite_frame + 1, nfs, QP), end="")

            #ywz
            ywz_times += 1

        print("              ", end="\r")
        
        sum_dpsnr += sum_dpsnr_part
        sum_dssim += sum_dssim_part
        
        average_dpsnr = sum_dpsnr_part / nfs
        average_dssim = sum_dssim_part / nfs
        print("dPSNR: %.3f - dSSIM: %.3f - nfs: %4d" % (average_dpsnr, average_dssim, nfs), flush=True)
        file_object.write("dPSNR: %.3f - dSSIM: %.3f - nfs: %4d\n" % (average_dpsnr, average_dssim, nfs))
        file_object.flush()

### Enhancement video by video
for ite_CmpVideo in range(num_CmpVideo):
    ### Extract info from cmp video path
    CmpVideo_path = CmpVideo_path_list[ite_CmpVideo].replace('\\','/')
    CmpVideo_name = CmpVideo_path.split("/")[-1].split(".")[0].replace('\\','/')
    
    RawVideo_name = "_".join(CmpVideo_name.split("_")[0:3]).replace('\\','/')
    RawVideo_path = os.path.join(dir_RawVideo, RawVideo_name + ".yuv").replace('\\','/')
    
    nfs = int(CmpVideo_name.split("_")[2])
    
    dims_list = CmpVideo_name.split("_")[1]
    width = int(dims_list.split("x")[0])
    height = int(dims_list.split("x")[1])
    
    # Load PQF label and ApprQP label
    PQF_label = list(np.load(os.path.join(dir_PQFLabel, "PQFLabel_" + CmpVideo_name + ".npy").replace('\\','/')))
    if opt_QPLabel:
        ApprQP_label = list(np.load(os.path.join(dir_ApprQP, "ApprQP_" + CmpVideo_name + ".npy").replace('\\','/')))
    else:
        ApprQP_label = [QP_video] * nfs
    
    # Initialize enhanced_list
    enhanced_list = np.zeros((nfs, height, width), dtype=np.float32)
    
    # Record dpsnr and dssim
    sum_dpsnr = 0.0
    sum_dssim = 0.0

    ### PQF enhancement
    print("enhancing PQF...")
    # for QP in QP_list:
    #
    #     # Find all PQFs and their pre/sub PQFs pertain to this QP
    #     PrePQFIndex_list_part, CmpPQFIndex_list_part, SubPQFIndex_list_part = return_PQFIndices(PQF_label, QP, ApprQP_label)
    #     if len(PrePQFIndex_list_part) == 0:
    #         continue
    #
    #     # Enhance PQF
    #     dir_model_pre = dir_model + "/PQF_enhancement" + "/model_QP" + str(QP)
    #     func_enhance(dir_model_pre, QP, PrePQFIndex_list_part, CmpPQFIndex_list_part, SubPQFIndex_list_part)
    #
    ### Non-PQF enhancement
    print("enhancing non-PQFs...")
    #ywz
    ywz_times = 0
    for QP in QP_list:
        
        # Find pre-PQFs, non-PQFs and sub-PQFs pertain to this QP
        PrePQFIndex_list_part, NonPQFIndex_list_part, SubPQFIndex_list_part = return_NPIndices(PQF_label, QP, ApprQP_label)
        if len(PrePQFIndex_list_part) == 0:
            continue
                    
        # Enhance non-PQF
        # dir_model_pre = dir_model + "/NP_enhancement" + "/model_QP" + str(QP)
        dir_model_pre = "model_QP32"

        func_enhance(dir_model_pre, QP, PrePQFIndex_list_part, NonPQFIndex_list_part, SubPQFIndex_list_part)


    ### Output and record result
    average_dpsnr = sum_dpsnr / nfs
    average_dssim = sum_dssim / nfs
    print("dPSNR: %.3f - dSSIM: %.3f - nfs: %4d - %s" % (average_dpsnr, average_dssim, nfs, CmpVideo_name), flush=True)
    file_object.write("dPSNR: %.3f - dSSIM: %.3f - nfs: %4d - %s\n" % (average_dpsnr, average_dssim, nfs, CmpVideo_name))
    file_object.flush()
    
    ### Output bmp
    # Here we have enhanced_list that records all enhanced frames. If you want to output enhanced images, code here.
    pass
    
       