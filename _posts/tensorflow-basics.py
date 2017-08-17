import tensorflow as tf
import numpy as np


def ex_I():
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
    # create the first matrix
    npMatrix = np.zeros(shape=(3, 3), dtype=np.float32)
    tfMatrix = tf.constant(npMatrix, dtype=tf.float32, name="tfMatrix")

    # create the second matrix
    npMatrix2 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32)
    tfMatrix2 = tf.constant(npMatrix2, dtype=tf.float32, name="tfMatrix2")

    # add them up
    npResult = np.add(npMatrix, npMatrix2)
    tfResult = tf.add(tfMatrix, tfMatrix2, name="tfResult")

    # Print out the sum
    print("Numpy result:\n", npResult, "\n")
    print("Tensorflow result node:\n", tfResult, "\n")

    # or maybe in the right way for tensorflow
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        writer = tf.summary.FileWriter('./graphs', sess.graph)
        node = sess.run(tfResult)
        print("Tensorflow result:\n", node, "\n")

        # for deeper understanding
        sumand1, sumand2 = sess.run([tfMatrix, tfMatrix2])
        print("Summands:\n", "first:\n", sumand1, "second:\n", sumand2)
    writer.close()


if __name__ == "__main__":
    print("Welcome to my tutorial.")
    print("Look at my first example")
    ex_I()
    print("Look at my second example")
    ex_II()
