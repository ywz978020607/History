import tensorflow as tf

images = ['img1', 'img2', 'img3', 'img4', 'img5']
labels = [1, 2, 3, 4, 5]

epoch_num = 8

f = tf.train.slice_input_producer([images, labels], num_epochs=None, shuffle=True)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    for i in range(epoch_num):
        k = sess.run(f)
        print(i, k)

    coord.request_stop()
    coord.join(threads)

