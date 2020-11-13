import tensorflow as tf
import tensorflow.contrib.slim as slim
import tflearn

def network(frame1, frame2, frame3, is_training, reuse=False, scope='netflow'): # design for QP37,42

    with tf.variable_scope(scope, reuse=reuse):

        # Define multi-scale feature extraction network

        c3_1_w = tf.get_variable("c3_1_w", shape=[3, 3, 1, 32],
                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        c3_1_b = tf.get_variable("c3_1_b", shape=[32],
                               initializer=tf.constant_initializer(0.0))

        c3_2_w = tf.get_variable("c3_2_w", shape=[3, 3, 1, 32],
                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        c3_2_b = tf.get_variable("c3_2_b", shape=[32],
                               initializer=tf.constant_initializer(0.0))

        c3_3_w = tf.get_variable("c3_3_w", shape=[3, 3, 1, 32],
                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        c3_3_b = tf.get_variable("c3_3_b", shape=[32],
                               initializer=tf.constant_initializer(0.0))

        c5_1_w = tf.get_variable("c5_1_w", shape=[5, 5, 1, 32],
                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        c5_1_b = tf.get_variable("c5_1_b", shape=[32],
                               initializer=tf.constant_initializer(0.0))

        c5_2_w = tf.get_variable("c5_2_w", shape=[5, 5, 1, 32],
                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        c5_2_b = tf.get_variable("c5_2_b", shape=[32],
                               initializer=tf.constant_initializer(0.0))

        c5_3_w = tf.get_variable("c5_3_w", shape=[5, 5, 1, 32],
                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        c5_3_b = tf.get_variable("c5_3_b", shape=[32],
                               initializer=tf.constant_initializer(0.0))

        c7_1_w = tf.get_variable("c7_1_w", shape=[7, 7, 1, 32],
                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        c7_1_b = tf.get_variable("c7_1_b", shape=[32],
                               initializer=tf.constant_initializer(0.0))

        c7_2_w = tf.get_variable("c7_2_w", shape=[7, 7, 1, 32],
                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        c7_2_b = tf.get_variable("c7_2_b", shape=[32],
                               initializer=tf.constant_initializer(0.0))

        c7_3_w = tf.get_variable("c7_3_w", shape=[7, 7, 1, 32],
                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        c7_3_b = tf.get_variable("c7_3_b", shape=[32],
                               initializer=tf.constant_initializer(0.0))

        # Define dense reconstruction network

        c1_w = tf.get_variable("c1_w", shape=[3, 3, 32*3*3, 32],
                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        c1_b = tf.get_variable("c1_b", shape=[32],
                               initializer=tf.constant_initializer(0.0))

        c2_w = tf.get_variable("c2_w", shape=[3, 3, 32, 32],
                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        c2_b = tf.get_variable("c2_b", shape=[32],
                               initializer=tf.constant_initializer(0.0))

        c3_w = tf.get_variable("c3_w", shape=[3, 3, 32*2, 32],
                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        c3_b = tf.get_variable("c3_b", shape=[32],
                               initializer=tf.constant_initializer(0.0))

        c4_w = tf.get_variable("c4_w", shape=[3, 3, 32*3, 32],
                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        c4_b = tf.get_variable("c4_b", shape=[32],
                               initializer=tf.constant_initializer(0.0))

        c5_w = tf.get_variable("c5_w", shape=[3, 3, 32*4, 32],
                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        c5_b = tf.get_variable("c5_b", shape=[32],
                               initializer=tf.constant_initializer(0.0))

        c6_w = tf.get_variable("c6_w", shape=[3, 3, 32, 1],
                               initializer=tf.contrib.layers.xavier_initializer(uniform=True))
        c6_b = tf.get_variable("c6_b", shape=[1],
                               initializer=tf.constant_initializer(0.0))


        # Multi-scale feature extraction

        c3_1 = tf.nn.conv2d(frame1, c3_1_w, strides=[1, 1, 1, 1], padding='SAME')
        c3_1 = tf.nn.bias_add(c3_1, c3_1_b)
        c3_1 = tflearn.activations.prelu(c3_1)

        c5_1 = tf.nn.conv2d(frame1, c5_1_w, strides=[1, 1, 1, 1], padding='SAME')
        c5_1 = tf.nn.bias_add(c5_1, c5_1_b)
        c5_1 = tflearn.activations.prelu(c5_1)

        c7_1 = tf.nn.conv2d(frame1, c7_1_w, strides=[1, 1, 1, 1], padding='SAME')
        c7_1 = tf.nn.bias_add(c7_1, c7_1_b)
        c7_1 = tflearn.activations.prelu(c7_1)

        cc_1 = tf.concat([c3_1, c5_1, c7_1], 3)

        c3_2 = tf.nn.conv2d(frame2, c3_2_w, strides=[1, 1, 1, 1], padding='SAME')
        c3_2 = tf.nn.bias_add(c3_2, c3_2_b)
        c3_2 = tflearn.activations.prelu(c3_2)

        c5_2 = tf.nn.conv2d(frame2, c5_2_w, strides=[1, 1, 1, 1], padding='SAME')
        c5_2 = tf.nn.bias_add(c5_2, c5_2_b)
        c5_2 = tflearn.activations.prelu(c5_2)

        c7_2 = tf.nn.conv2d(frame2, c7_2_w, strides=[1, 1, 1, 1], padding='SAME')
        c7_2 = tf.nn.bias_add(c7_2, c7_2_b)
        c7_2 = tflearn.activations.prelu(c7_2)

        cc_2 = tf.concat([c3_2, c5_2, c7_2], 3)

        c3_3 = tf.nn.conv2d(frame3, c3_3_w, strides=[1, 1, 1, 1], padding='SAME')
        c3_3 = tf.nn.bias_add(c3_3, c3_3_b)
        c3_3 = tflearn.activations.prelu(c3_3)

        c5_3 = tf.nn.conv2d(frame3, c5_3_w, strides=[1, 1, 1, 1], padding='SAME')
        c5_3 = tf.nn.bias_add(c5_3, c5_3_b)
        c5_3 = tflearn.activations.prelu(c5_3)

        c7_3 = tf.nn.conv2d(frame3, c7_3_w, strides=[1, 1, 1, 1], padding='SAME')
        c7_3 = tf.nn.bias_add(c7_3, c7_3_b)
        c7_3 = tflearn.activations.prelu(c7_3)

        cc_3 = tf.concat([c3_3, c5_3, c7_3], 3)

        # Merge
        c_concat = tf.concat([cc_1, cc_2, cc_3], 3)

        # Dense + BN reconstruction

        c1 = tf.nn.conv2d(c_concat, c1_w, strides=[1, 1, 1, 1], padding='SAME')
        c1 = tf.nn.bias_add(c1, c1_b)
        c1 = tf.layers.batch_normalization(c1,training=is_training)
        c1 = tflearn.activations.prelu(c1)

        c2 = tf.nn.conv2d(c1, c2_w, strides=[1, 1, 1, 1], padding='SAME')
        c2 = tf.nn.bias_add(c2, c2_b)
        c2 = tf.layers.batch_normalization(c2,training=is_training)
        c2 = tflearn.activations.prelu(c2)

        cc2 = tf.concat([c1, c2], 3)

        c3 = tf.nn.conv2d(cc2, c3_w, strides=[1, 1, 1, 1], padding='SAME')
        c3 = tf.nn.bias_add(c3, c3_b)
        c3 = tf.layers.batch_normalization(c3,training=is_training)
        c3 = tflearn.activations.prelu(c3)

        cc3 = tf.concat([c1, c2, c3], 3)

        c4 = tf.nn.conv2d(cc3, c4_w, strides=[1, 1, 1, 1], padding='SAME')
        c4 = tf.nn.bias_add(c4, c4_b)
        c4 = tf.layers.batch_normalization(c4,training=is_training)
        c4 = tflearn.activations.prelu(c4)

        cc4 = tf.concat([c1, c2, c3, c4], 3)

        c5 = tf.nn.conv2d(cc4, c5_w, strides=[1, 1, 1, 1], padding='SAME')
        c5 = tf.nn.bias_add(c5, c5_b)
        c5 = tf.layers.batch_normalization(c5,training=is_training)
        c5 = tflearn.activations.prelu(c5)

        c6 = tf.nn.conv2d(c5, c6_w, strides=[1, 1, 1, 1], padding='SAME')
        c6 = tf.nn.bias_add(c6, c6_b)
        c6 = tf.layers.batch_normalization(c6,training=is_training)
        c6 = tflearn.activations.prelu(c6)

        # Short connection

        output = tf.add(c6, frame2)

        return output


def network2(frame1, frame2, frame3, reuse=False, scope='netflow'): # design for QP22,27,32

    with tf.variable_scope(scope, reuse=reuse):
        with slim.arg_scope([slim.conv2d],  activation_fn=tflearn.activations.prelu,
                            weights_initializer=tf.contrib.layers.xavier_initializer(uniform=True),
                            biases_initializer=tf.constant_initializer(0.0)):

            # Multi-scale

            c3_1 = slim.conv2d(frame1, 32, [3, 3], scope='conv3_1')
            c5_1 = slim.conv2d(frame1, 32, [5, 5], scope='conv5_1')
            c7_1 = slim.conv2d(frame1, 32, [7, 7], scope='conv7_1')

            cc_1 = tf.concat([c3_1, c5_1, c7_1], 3, name='concat_1')  #增加通道数

            c3_2 = slim.conv2d(frame2, 32, [3, 3], scope='conv3_2')
            c5_2 = slim.conv2d(frame2, 32, [5, 5], scope='conv5_2')
            c7_2 = slim.conv2d(frame2, 32, [7, 7], scope='conv7_2')

            cc_2 = tf.concat([c3_2, c5_2, c7_2], 3, name='concat_2')

            c3_3 = slim.conv2d(frame3, 32, [3, 3], scope='conv3_3')
            c5_3 = slim.conv2d(frame3, 32, [5, 5], scope='conv5_3')
            c7_3 = slim.conv2d(frame3, 32, [7, 7], scope='conv7_3')

            cc_3 = tf.concat([c3_3, c5_3, c7_3], 3, name='concat_3')

            # Merge

            c_concat = tf.concat([cc_1, cc_2, cc_3], 3, name='c_concat')

            # General CNN

            cc1 = slim.conv2d(c_concat, 26, [3, 3], scope='cconv1')
            cc2 = slim.conv2d(cc1, 26, [3, 3], scope='cconv2')
            cc3 = slim.conv2d(cc2, 26, [3, 3], scope='cconv3')
            cc4 = slim.conv2d(cc3, 26, [3, 3], scope='cconv4')
            cc5 = slim.conv2d(cc4, 26, [3, 3], scope='cconv5')
            cc6 = slim.conv2d(cc5, 26, [3, 3], scope='cconv6')
            cc7 = slim.conv2d(cc6, 26, [3, 3], scope='cconv7')
            cc8 = slim.conv2d(cc7, 16, [3, 3], scope='cconv8')
            cout = slim.conv2d(cc8, 1, [3, 3], activation_fn=None, scope='cout') # 1 channel output

            output = tf.add(cout, frame2) # ResNet

        return output
