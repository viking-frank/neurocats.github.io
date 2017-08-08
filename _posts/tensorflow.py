import tensorflow as tf
import numpy as np

# create a matrix
npMatrix = np.zeros(shape=(3, 3), dtype=np.float32)
tfMatrix = tf.zeros(shape=(3, 3), dtype=tf.float32)

# print out results
print(npMatrix)
print(tfMatrix)

# or maybe in the right way
with tf.Session() as sess:
    node = sess.run(tfMatrix)
    print(node)
