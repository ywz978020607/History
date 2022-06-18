# # from utils import *
# from mls_utils import *
# import cv2
#
#
# # y_batch, u_batch, v_batch = yuv_import("D:/data/Videos/cmp/BasketballPass_416x240_500.yuv",width_frame=416,height_frame=240, nfs=2, startfrm=1, opt_bar=True)
# y_batch, u_batch, v_batch = yuv_import("D:/data/Videos/cmp/BasketballPass_416x240_500.yuv", nfs=2, startfrm=1, opt_bar=True)
#
# cv2.namedWindow("test", 0)  # windows can be resize maunually
# cv2.imshow("test", v_batch[0])  # ICCP warning is due to the typing software. turn it off
# cv2.waitKey()
# cv2.destroyAllWindows()
#
#
#
#
#
# print("pass")



###########
#test for double_input
import os
from model.vespcn import VESPCN
from model.ltdvsr import LTDVSR
from model.mcresnet import MCRESNET
from model.drvsr import DRVSR
from model.frvsr import FRVSR
from model.dufvsr import DUFVSR
from model.pfnl import PFNL
import tensorflow as tf

model=PFNL()
LR, HR= model.double_input_producer()
sess = tf.Session()
coord = tf.train.Coordinator()
threads = tf.train.start_queue_runners(sess=sess, coord=coord)
sess.run(tf.global_variables_initializer())
lr1,hr=sess.run([LR,HR])


pass




