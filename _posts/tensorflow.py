import tensorflow as tf
import numpy as np


def ex_I():
    print("Testlauf I", "\n\n")

    # create a matrix
    npMatrix = np.zeros(shape=(3, 3), dtype=np.float32)
    tfMatrix = tf.zeros(shape=(3, 3), dtype=tf.float32)

    # print out results
    print("Numpy Matrix:\n", npMatrix, "\n")
    print("Tensorflow node:\n", tfMatrix, "\n")

    # or maybe in the right way
    with tf.Session() as sess:
        node = sess.run(tfMatrix)
        print("Tensorflow node value:\n", node, "\n")


def ex_II():
    print("Testlauf II", "\n\n")

    # create a matrix
    npMatrix = np.zeros(shape=(3, 3), dtype=np.float32)
    tfMatrix = tf.constant(npMatrix, dtype=tf.float32, name="tfMatrix")

    npMatrix2 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32)
    tfMatrix2 = tf.constant(npMatrix2, dtype=tf.float32, name="tfMatrix2")

    npResult = np.add(npMatrix, npMatrix2)
    tfResult = tf.add(tfMatrix, tfMatrix2, name="tfResult")

    # print out results
    print("Numpy result:\n", npResult, "\n")
    print("Tensorflow result node:\n", tfResult, "\n")

    # or maybe in the right way
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        writer = tf.summary.FileWriter('./graphs', sess.graph)
        node = sess.run(tfResult)
        print("Tensorflow result:\n", node, "\n")
    writer.close()


if __name__ == "__main__":
    pass
