import gc, os, glob, argparse
import h5py
import numpy as np
import tflearn
import tensorflow as tf
import tensorflow.contrib.slim as slim
from functools import reduce  # for calculating PSNR
from operator import mul  # for calculating the num of parameters
import net_MFCNN

# import net_MFCNN_G
# import net_MFCNN_Gs


### Settings
CHANNEL = 1  # use only Y

ratio_small = 0.01
lr_ori = 1e-5

parser = argparse.ArgumentParser()
parser.add_argument('-hf', '--height', type=int, help="HEIGHT of frame", default=64)
parser.add_argument('-wf', '--width', type=int, help="WIDTH of frame", default=64)
parser.add_argument('-bs', '--batch_size', type=int, default=128)
# parser.add_argument('-g', '--gpu', type=str, help="GPU")
# parser.add_argument('-q',  '--qp', type=str, help="QP")
parser.add_argument('-es1', '--epoch_step1', type=int, default=1)
parser.add_argument('-es2', '--epoch_step2', type=int, default=1)
args = parser.parse_args()

# QP = args.qp
# GPU = args.gpu
# QP_base = 42
# QP_base = str(QP_base)

QP = 32
QP = str(QP)
epoch_step1 = args.epoch_step1
epoch_step2 = args.epoch_step2
res_index = str(60)

BATCH_SIZE = args.batch_size
WIDTH = args.width
HEIGHT = args.height

# net1_list = [12, 17, 22, 27, 32, 37, 42, 47]

net1_list = [37,42]

dir_stack = "D:/Desktop/IRC_Lab/test/code_training_NP/mini_stack_QP42"
dir_model = "./model_QP" + QP
record_FileName = "./record_train_QP" + QP + ".txt"

# dir_stack = "/media/chenzp/czp1/HUAWEI/Database/train_136_cbr/PQF_stack/QP" + QP
# dir_model = "/media/chenzp/MyPassport/MFQEv2.0/Models_game_New/PQF_enhancement_newnpy/model_QP" + QP
model_res_path = "D:/Desktop/IRC_Lab/test/MFQEv2.0_test_qp/Models/NP_enhancement/model_QP32/model_step2.ckpt-32"
# model_res_path = os.path.join("/media/chenzp/MyPassport/MFQEv2.0/Models/PQF_enhancement_Reset/model_QP"+ QP, "model_step2_FtSource.ckpt-" + res_index)
# record_FileName = "./train_recordNew/record_newnppy_train_PQFEnhancement_QP" + QP + "_ft.txt"
file_object = open(record_FileName, 'w')


# def load_stack(type_process, ite_stack):
#     """Load stack npy.
#
#     type_process: "tra" or "val".
#     ite_stack: start from 0."""
#     stack_name = "stack_" + type_process + "_pre_" + str(ite_stack) + ".npy"
#     pre_list = np.load(os.path.join(dir_stack, stack_name))
#     print("\rpre loaded.", end="")
#
#     stack_name = "stack_" + type_process + "_cmp_" + str(ite_stack) + ".npy"
#     cmp_list = np.load(os.path.join(dir_stack, stack_name))
#     print("\rcmp loaded.", end="")
#
#     stack_name = "stack_" + type_process + "_sub_" + str(ite_stack) + ".npy"
#     sub_list = np.load(os.path.join(dir_stack, stack_name))
#     print("\rsub loaded.", end="")
#
#     stack_name = "stack_" + type_process + "_raw_" + str(ite_stack) + ".npy"
#     raw_list = np.load(os.path.join(dir_stack, stack_name))
#     print("\rraw loaded.", end="")
#
#     ###   自己添加shuffle
#     data_num = cmp_list.shape[0]  # 共有多少张64x64x1的小图
#     num_examples = len(cmp_list)  # shuffle
#     per = np.arange(num_examples)
#     np.random.shuffle(per)
#     pre_list = pre_list[per[0:num_examples]]
#     cmp_list = cmp_list[per[0:num_examples]]
#     sub_list = sub_list[per[0:num_examples]]
#     raw_list = raw_list[per[0:num_examples]]
#     print('shuffle finished')
#
#     return pre_list, cmp_list, sub_list, raw_list

def load_stack(type_process, ite_stack):
    """Load stack npy.

    type_process: "tra" or "val".
    ite_stack: start from 0."""
    stack_name = "stack_" + type_process + "_pre_" + str(ite_stack) + ".hdf5"
    pre_list = h5py.File(os.path.join(dir_stack, stack_name), 'r')['stack_pre'][:]
    print("pre loaded.")

    stack_name = "stack_" + type_process + "_cmp_" + str(ite_stack) + ".hdf5"
    cmp_list = h5py.File(os.path.join(dir_stack, stack_name), 'r')['stack_cmp'][:]
    print("cmp loaded.")

    stack_name = "stack_" + type_process + "_sub_" + str(ite_stack) + ".hdf5"
    sub_list = h5py.File(os.path.join(dir_stack, stack_name), 'r')['stack_sub'][:]
    print("sub loaded.")

    stack_name = "stack_" + type_process + "_raw_" + str(ite_stack) + ".hdf5"
    raw_list = h5py.File(os.path.join(dir_stack, stack_name), 'r')['stack_raw'][:]
    print("raw loaded.")

    return pre_list, cmp_list, sub_list, raw_list


def cal_MSE(img1, img2):
    """Calculate MSE of two images.

    img: [0,1]."""
    MSE = tf.reduce_mean(tf.pow(tf.subtract(img1, img2), 2.0))
    return MSE


def cal_PSNR(img1, img2):
    """Calculate PSNR of two images.

    img: [0,1]."""
    MSE = cal_MSE(img1, img2)
    PSNR = 10.0 * tf.log(1.0 / MSE) / tf.log(10.0)
    return PSNR


def main_train():
    """Fine tune a model from step2 and continue training.

    Train and evaluate model."""
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # only show error and warning
    # os.environ['CUDA_VISIBLE_DEVICES'] = GPU
    os.environ['CUDA_VISIBLE_DEVICES'] = "2"

    ### Defind a session
    config = tf.ConfigProto(allow_soft_placement=True)  # if GPU is not usable, then turn to CPU automatically
    sess = tf.Session(config=config)

    ### Set placeholder
    x1 = tf.placeholder(tf.float32, [BATCH_SIZE, HEIGHT, WIDTH, CHANNEL])  # pre
    x2 = tf.placeholder(tf.float32, [BATCH_SIZE, HEIGHT, WIDTH, CHANNEL])  # cmp
    x3 = tf.placeholder(tf.float32, [BATCH_SIZE, HEIGHT, WIDTH, CHANNEL])  # sub
    x5 = tf.placeholder(tf.float32, [BATCH_SIZE, HEIGHT, WIDTH, CHANNEL])  # raw

    if int(QP) in net1_list:
        is_training = tf.placeholder_with_default(False, shape=())  # for BN training/testing. default testing.

    PSNR_0 = cal_PSNR(x2, x5)  # PSNR before enhancement (cmp and raw)

    ### Motion compensation
    # x1to2 = net_MFCNN.warp_img(tf.shape(x2)[0], x2, x1, False)
    # x3to2 = net_MFCNN.warp_img(tf.shape(x2)[0], x2, x3, True)

    x1to2 = net_MFCNN.warp_img(tf.shape(x2)[0], x2, x1, False)
    x3to2 = net_MFCNN.warp_img(tf.shape(x2)[0], x2, x3, True)

    ### Flow loss
    FlowLoss_1 = cal_MSE(x1to2, x2)
    FlowLoss_2 = cal_MSE(x3to2, x2)
    flow_loss = FlowLoss_1 + FlowLoss_2

    ### Enhance cmp frames
    if int(QP) in net1_list:
        x2_enhanced = net_MFCNN.network(x1to2, x2, x3to2, is_training)
    else:
        x2_enhanced = net_MFCNN.network2(x1to2, x2, x3to2)

    MSE = cal_MSE(x2_enhanced, x5)  # loss defination
    PSNR = cal_PSNR(x2_enhanced, x5)  # PSNR after enhancement (enhanced and raw)
    delta_PSNR = PSNR - PSNR_0

    ### 2 kinds of loss for 2-step training
    #######train loss of step 2
    OptimizeLoss_1 = flow_loss + ratio_small * MSE  # step1: the key is MC-subnet.
    OptimizeLoss_2 = ratio_small * flow_loss + MSE  # step2: the key is QE-subnet.

    ### Defind optimizer
    update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
    with tf.control_dependencies(update_ops):
        Training_step1 = tf.train.AdamOptimizer(lr_ori).minimize(OptimizeLoss_1)
        Training_step2 = tf.train.AdamOptimizer(lr_ori).minimize(OptimizeLoss_2)

    ### TensorBoard
    tf.summary.scalar('PSNR improvement', delta_PSNR)
    # tf.summary.scalar('PSNR before enhancement', PSNR_0)
    # tf.summary.scalar('PSNR after enhancement', PSNR)
    tf.summary.scalar('MSE loss of motion compensation', flow_loss)
    # tf.summary.scalar('MSE loss of final quality enhancement', MSE)
    tf.summary.scalar('MSE loss for training step1 (mainly MC-subnet)', OptimizeLoss_1)
    tf.summary.scalar('MSE loss for training step2 (mainly QE-subnet)', OptimizeLoss_2)

    tf.summary.image('cmp', x2)
    tf.summary.image('enhanced', x2_enhanced)
    tf.summary.image('raw', x5)
    tf.summary.image('x1to2', x1to2)
    tf.summary.image('x3to2', x3to2)

    summary_writer = tf.summary.FileWriter(dir_model, sess.graph)
    summary_op = tf.summary.merge_all()

    saver = tf.train.Saver(max_to_keep=None)  # define a saver

    sess.run(tf.global_variables_initializer())  # initialize network variables

    ### Calculate the num of parameters
    num_params = 0
    for variable in tf.trainable_variables():
        shape = variable.get_shape()
        num_params += reduce(mul, [dim.value for dim in shape], 1)
    print("# num of parameters: %d #" % num_params)
    file_object.write("# num of parameters: %d #\n" % num_params)
    file_object.flush()

    ### Find all stacks then cal their number
    stack_name = os.path.join(dir_stack, "stack_tra_pre_*")
    num_TrainingStack = len(glob.glob(stack_name))
    stack_name = os.path.join(dir_stack, "stack_val_pre_*")
    num_ValidationStack = len(glob.glob(stack_name))

    ### Restore      ###注释掉了finetune训练，调用训练好的模型的代码

    saver_res = tf.train.Saver()
    saver_res.restore(sess, model_res_path)
    print("successfully restore model %d!" % (int(res_index) + 1))
    file_object.write("successfully restore model %d!\n" % (int(res_index) + 1))
    file_object.flush()

    #查看一下各个变量，是否都对
    cconv1_w = tf.get_default_graph().get_tensor_by_name("netflow/cconv1/weights:0")
    # cconv2_w = tf.get_default_graph().get_tensor_by_name("netflow/cconv2/weights:0")
    # cconv3_w = tf.get_default_graph().get_tensor_by_name("netflow/cconv3/weights:0")
    # cconv4_w = tf.get_default_graph().get_tensor_by_name("netflow/cconv4/weights:0")
    # cconv5_w = tf.get_default_graph().get_tensor_by_name("netflow/cconv5/weights:0")

    print(sess.run(cconv1_w))



    print("##### Start running! #####")

    num_TrainingBatch_count = 0

    ### Step 1: converge MC-subnet; Step 2: converge QE-subnet
    # for ite_step in [1,2]:
    for ite_step in [2]:
        if ite_step == 1:
            num_epoch = epoch_step1
        else:
            num_epoch = epoch_step2

        ### Epoch by Epoch
        for ite_epoch in range(num_epoch):

            ### Train stack by stack
            for ite_stack in range(num_TrainingStack):

                # pre_list, cmp_list, sub_list, raw_list = [], [], [], []
                # gc.collect()
                # if ite_step == 1 and ite_epoch == 0 and ite_stack == 0:
                if ite_step == 2 and ite_epoch == 0 and ite_stack == 0:  #从2开始
                    pre_list, cmp_list, sub_list, raw_list = load_stack("tra", ite_stack)
                    gc.collect()
                num_batch = int(len(pre_list) / BATCH_SIZE)

                ### Batch by batch
                for ite_batch in range(num_batch):

                    print("\rstep %1d - epoch %2d/%2d - training stack %2d/%2d - batch %3d/%3d" % \
                          (ite_step, ite_epoch + 1, num_epoch, ite_stack + 1, num_TrainingStack, ite_batch + 1,
                           num_batch), end="")

                    start_index = ite_batch * BATCH_SIZE
                    next_start_index = (ite_batch + 1) * BATCH_SIZE

                    if ite_step == 1:
                        if int(QP) in net1_list:
                            Training_step1.run(session=sess, feed_dict={
                                x1: pre_list[start_index:next_start_index],
                                x2: cmp_list[start_index:next_start_index],
                                x3: sub_list[start_index:next_start_index],
                                x5: raw_list[start_index:next_start_index],
                                is_training: True})  # train
                        else:
                            Training_step1.run(session=sess, feed_dict={
                                x1: pre_list[start_index:next_start_index],
                                x2: cmp_list[start_index:next_start_index],
                                x3: sub_list[start_index:next_start_index],
                                x5: raw_list[start_index:next_start_index]})  # train
                    else:
                        if int(QP) in net1_list:
                            Training_step2.run(session=sess, feed_dict={
                                x1: pre_list[start_index:next_start_index],
                                x2: cmp_list[start_index:next_start_index],
                                x3: sub_list[start_index:next_start_index],
                                x5: raw_list[start_index:next_start_index],
                                is_training: True})
                        else:
                            Training_step2.run(session=sess, feed_dict={
                                x1: pre_list[start_index:next_start_index],
                                x2: cmp_list[start_index:next_start_index],
                                x3: sub_list[start_index:next_start_index],
                                x5: raw_list[start_index:next_start_index]})

                            # Update TensorBoard and print result
                    num_TrainingBatch_count += 1

                    if ((ite_batch + 1) == int(num_batch / 2)) or ((ite_batch + 1) == num_batch):

                        if int(QP) in net1_list:
                            summary, delta_PSNR_batch, PSNR_0_batch, FlowLoss_batch, MSE_batch = sess.run(
                                [summary_op, delta_PSNR, PSNR_0, flow_loss, MSE], feed_dict={
                                    x1: pre_list[start_index:next_start_index],
                                    x2: cmp_list[start_index:next_start_index],
                                    x3: sub_list[start_index:next_start_index],
                                    x5: raw_list[start_index:next_start_index],
                                    is_training: False})
                        else:
                            summary, delta_PSNR_batch, PSNR_0_batch, FlowLoss_batch, MSE_batch = sess.run(
                                [summary_op, delta_PSNR, PSNR_0, flow_loss, MSE], feed_dict={
                                    x1: pre_list[start_index:next_start_index],
                                    x2: cmp_list[start_index:next_start_index],
                                    x3: sub_list[start_index:next_start_index],
                                    x5: raw_list[start_index:next_start_index]})

                        summary_writer.add_summary(summary, num_TrainingBatch_count)
                        print("\rstep %1d - epoch %2d - imp PSNR: %.3f - ori PSNR: %.3f             " % \
                              (ite_step, ite_epoch + 1, delta_PSNR_batch, PSNR_0_batch))
                        file_object.write("step %1d - epoch %2d - imp PSNR: %.3f - ori PSNR: %.3f\n" % \
                                          (ite_step, ite_epoch + 1, delta_PSNR_batch, PSNR_0_batch))
                        file_object.flush()

            ### Store the model of this epoch
            if ite_step == 1:
                CheckPoint_path = os.path.join(dir_model, "model_step1.ckpt")
            else:
                CheckPoint_path = os.path.join(dir_model, "model_step2.ckpt")
            saver.save(sess, CheckPoint_path, global_step=ite_epoch)

            sum_improved_PSNR = 0
            num_patch_count = 0

            ### Eval stack by stack, and report together for this epoch
            for ite_stack in range(num_ValidationStack):

                pre_list, cmp_list, sub_list, raw_list = [], [], [], []
                gc.collect()
                pre_list, cmp_list, sub_list, raw_list = load_stack("val", ite_stack)
                gc.collect()

                num_batch = int(len(pre_list) / BATCH_SIZE)

                ### Batch by batch
                for ite_batch in range(num_batch):

                    print("\rstep %1d - epoch %2d/%2d - validation stack %2d/%2d                " % \
                          (ite_step, ite_epoch + 1, num_epoch, ite_stack + 1, num_ValidationStack), end="")

                    start_index = ite_batch * BATCH_SIZE
                    next_start_index = (ite_batch + 1) * BATCH_SIZE

                    if int(QP) in net1_list:
                        delta_PSNR_batch = sess.run(delta_PSNR, feed_dict={
                            x1: pre_list[start_index:next_start_index],
                            x2: cmp_list[start_index:next_start_index],
                            x3: sub_list[start_index:next_start_index],
                            x5: raw_list[start_index:next_start_index],
                            is_training: False})
                    else:
                        delta_PSNR_batch = sess.run(delta_PSNR, feed_dict={
                            x1: pre_list[start_index:next_start_index],
                            x2: cmp_list[start_index:next_start_index],
                            x3: sub_list[start_index:next_start_index],
                            x5: raw_list[start_index:next_start_index]})

                    sum_improved_PSNR += delta_PSNR_batch * BATCH_SIZE
                    num_patch_count += BATCH_SIZE

            if num_patch_count != 0:
                print("\n### imp PSNR by model after step %1d - epoch %2d/%2d: %.3f ###\n" % \
                      (ite_step, ite_epoch + 1, num_epoch, sum_improved_PSNR / num_patch_count))
                file_object.write("### imp PSNR by model after step %1d - epoch %2d/%2d: %.3f ###\n" % \
                                  (ite_step, ite_epoch + 1, num_epoch, sum_improved_PSNR / num_patch_count))
                file_object.flush()


if __name__ == '__main__':
    main_train()

    print("##### Training completes! #####")
    file_object.write("##### Training completes! #####")

    file_object.close()
