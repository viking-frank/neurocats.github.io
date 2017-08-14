import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# initialize placeholder for data input
with tf.name_scope("Input"):
    x = tf.placeholder(dtype=tf.float32, shape=[None, 1], name="x")

# think about the dimensions of your neural net (trial & error)
layer = [1, 50, 50, 1]

# hidden layer in a loop
with tf.name_scope("Hidden"):
    out = x
    for i in range(len(layer) - 2):
        with tf.name_scope("Layer"):
            # random initialization of weight and bis
            W = tf.Variable(
                tf.random_normal([layer[i], layer[i + 1]], dtype=tf.float32),
                name="W")
            b = tf.Variable(
                tf.random_normal([1, layer[i + 1]], dtype=tf.float32),
                name="b")

            # matrix operation
            out = tf.matmul(out, W) + b
            # activation function
            out = tf.nn.relu(out)

            # summarize histogram
            tf.summary.histogram("W", W)
            tf.summary.histogram("b", b)

# output layer
with tf.name_scope("Output"):
    # random initialization of weight and bis
    W = tf.Variable(
        tf.random_normal([layer[-2], layer[-1]], dtype=tf.float32),
        name="W")
    b = tf.Variable(
        tf.random_normal([1, layer[-1]], dtype=tf.float32),
        name="b")

    # matrix operation
    out = tf.matmul(out, W) + b

    # no activation for the output

    # summarize histogram
    tf.summary.histogram("W", W)
    tf.summary.histogram("b", b)

# loss function
with tf.name_scope("Loss"):
    # supervised input labels
    with tf.name_scope("label"):
        y = tf.placeholder(dtype=tf.float32, shape=[None, 1], name="y")
    # euclidean distance as loss
    with tf.name_scope("distance"):
        loss = tf.subtract(out, y, name="difference")
        loss = tf.abs(loss, name="absolute")
        loss = tf.reduce_mean(loss)

    # summarise scalar
    tf.summary.scalar('loss', loss)

with tf.name_scope("trainer"):
    train_op = tf.train.AdamOptimizer().minimize(loss)

# for tensorboard usability just merge all summaries into one node
summary_op = tf.summary.merge_all()

# operation for initialize variables
init_op = tf.global_variables_initializer()

# determine training length and batch size
train_len = 5000
batch = 2000
with tf.Session() as sess:
    # run operation for variable initialization
    sess.run(init_op)
    # create a writer
    writer = tf.summary.FileWriter("./graphs", sess.graph)
    for i in range(train_len):
        # randomly train with trainingset
        x_data = np.float32(np.random.uniform(-1, 1, (1, batch))).T
        y_data = np.float32(np.sin(4 * x_data))

        # run training operation
        sess.run(train_op, feed_dict={x: x_data, y: y_data})

        # summarize
        summary = sess.run(summary_op, feed_dict={x: x_data, y: y_data})
        writer.add_summary(summary, i)

    # inference
    # check if everything worked out fine by visualizing equidistant testpoints
    samples = 1000
    x_data = np.float32(np.linspace(-1, 1, samples))[None, :].T
    y_data = np.float32(np.sin(4 * x_data))
    _out = sess.run(out, feed_dict={x: x_data})
writer.close()

# plot
fig = plt.figure(1)
ax1 = fig.add_subplot(111)
ax1.plot(y_data, 'g-')
ax1.plot(_out, 'y--')
ax1.plot(np.subtract(y_data, _out), 'r--')
ax1.set_title("Sinus")
ax1.grid(True)
plt.show()
