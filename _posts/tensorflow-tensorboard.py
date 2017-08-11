import tensorflow as tf
import numpy as np

# initialize a placeholder. It can be feed with values in a session
x = tf.placeholder(dtype=tf.float32, shape=[1], name="x")

# create a graph representation of x^2+1
with tf.name_scope("xPow2Plus1"):
    # square x to get x^2
    xPow2 = tf.square(x, name="xPow2")

    # create a 1 by initializing a constant feed with a numpy array
    npOne = np.array([1], dtype=np.float32)
    tfOne = tf.constant(npOne, dtype=tf.float32, name="one")

    # add both up to create x^2 + 1
    xPow2Plus1 = tf.add(xPow2, tfOne, name="xPow2Plus1")

    # establish the possibility of summarising
    with tf.name_scope("summary"):
        # reduce to scalar
        xPow2Plus1 = tf.reduce_mean(xPow2Plus1)
        # summarise scalar
        tf.summary.scalar('f', xPow2Plus1)

# create a  graph representation that is wished to be 2x
with tf.name_scope("2x"):
    # let tensorflow compute to figure our the gradient computation grahp
    grad = tf.gradients(xPow2Plus1, x, name="2x")

    # establish possibility of summarizing
    with tf.name_scope("summary"):
        # reduce to scalar
        grad = tf.reduce_mean(grad[0])
        # summarise scalar
        tf.summary.scalar('dfdx', grad)

# for tensorboard usability just merge all summaries into one node
merged = tf.summary.merge_all()

# create a tensorflow session
with tf.Session() as sess:
    # create a writer for tensorboard
    writer = tf.summary.FileWriter('./graphs', sess.graph)
    # loop through a set of points to draw a graph
    for i in np.arange(-7, 7, 0.001).tolist():
        # allocate values to the graph nodes
        summary, node1, node2 = sess.run(
            [merged, xPow2Plus1, grad],
            feed_dict={
                # feed x with your points from testset
                x: np.array([i])
            })
        # writer takes summary and integer for scalar input
        writer.add_summary(summary, i * 1000)
# don't forget to close your poor busy writer
writer.close()
