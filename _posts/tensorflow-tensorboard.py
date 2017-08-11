import tensorflow as tf
import numpy as np

# initialize a placeholder. It can be feed with values in a session
x = tf.placeholder(dtype=tf.float32, shape=[1], name="x")

with tf.name_scope("xPow2Plus1"):
    xPow2 = tf.square(x, name="xPow2")
    npOne = np.array([1], dtype=np.float32)
    tfOne = tf.constant(npOne, dtype=tf.float32, name="one")
    xPow2Plus1 = tf.add(xPow2, tfOne, name="xPow2Plus1")
    with tf.name_scope("summary"):
        xPow2Plus1 = tf.reduce_mean(xPow2Plus1)
        tf.summary.scalar('f', xPow2Plus1)

with tf.name_scope("2x"):
    grad = tf.gradients(xPow2Plus1, x, name="2x")
    with tf.name_scope("summary"):
        grad = tf.reduce_mean(grad[0])
        tf.summary.scalar('dfdx', grad)

merged = tf.summary.merge_all()

# or maybe in the right way for tensorflow
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter('./graphs', sess.graph)
    for i in np.arange(-7, 7, 0.1).tolist():
        summary, node1, node2 = sess.run([merged, xPow2Plus1, grad],
                                     feed_dict={
                                         x: np.array([i])
                                     })
        writer.add_summary(summary, i*1000)
writer.close()
