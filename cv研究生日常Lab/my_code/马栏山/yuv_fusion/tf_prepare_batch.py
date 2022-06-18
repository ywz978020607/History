import tensorflow as tf
import numpy as np

# 样本个数
sample_num = 5
# 设置迭代次数
epoch_num = 2
# 设置一个批次中包含样本个数
batch_size = 3
# 计算每一轮epoch中含有的batch个数
batch_total = int(sample_num / batch_size) + 1


# 生成4个数据和标签
def generate_data(sample_num=sample_num):
    labels = np.asarray(range(0, sample_num))
    images = np.random.random([sample_num, 224, 224, 3])
    print('image size {},label size :{}'.format(images.shape, labels.shape))

    return images, labels


def get_batch_data(batch_size=batch_size):
    images, label = generate_data()
    # 数据类型转换为tf.float32
    images = tf.cast(images, tf.float32)
    label = tf.cast(label, tf.int32)

    # 从tensor列表中按顺序或随机抽取一个tensor
    input_queue = tf.train.slice_input_producer([images, label], shuffle=False)

    image_batch, label_batch = tf.train.batch(input_queue, batch_size=batch_size, num_threads=3, capacity=64)
    return image_batch, label_batch


image_batch, label_batch = get_batch_data(batch_size=batch_size)

with tf.Session() as sess:
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess, coord)
    #
    image_batch_v, label_batch_v = sess.run([image_batch, label_batch])
    print(image_batch_v, label_batch_v)
    image_batch_v, label_batch_v = sess.run([image_batch, label_batch])
    print(image_batch_v, label_batch_v)
    #

    # try:
    #     for i in range(epoch_num):  # 每一轮迭代
    #         print('************')
    #         for j in range(batch_total):  # 每一个batch
    #             print('--------')
    #             # 获取每一个batch中batch_size个样本和标签
    #             image_batch_v, label_batch_v = sess.run([image_batch, label_batch])
    #             # for k in
    #             print(image_batch_v.shape, label_batch_v)
    # except tf.errors.OutOfRangeError:
    #     print("done")
    # finally:
    #     coord.request_stop()
    # coord.join(threads)