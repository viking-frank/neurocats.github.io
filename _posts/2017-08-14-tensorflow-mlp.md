---
layout: post
comments: true
title:  "Introduction to Tensorflow - 03 Neural Network"
excerpt: "While showing how to build to a simple neural network with 
tensorflow I want to give the reader a playful handling with namescopes and 
show how to make sense of your weight evolution with histograms."
date:   2017-08-14
mathjax: true
---

# Neural Network
## Introduction
I assume that the reader has a basic knowledge about neural networks. I 
will just explain how to build one with tensorflow. I will not explain what a 
neural network is.

We will approximate **sinus** as a toy example. Here we have every possible 
label provided.

Let's start right away.

## computation graph
First we obviously have to import tensorflow and numpy. Additionally we will
use matplotlib for see how well we approximated sinus by comparing the outcome
of the network with the original function visually.

```python
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
```

### Layer

We also need a placeholder for our input unit.
```python
# initialize placeholder for data input
with tf.name_scope("Input"):
    x = tf.placeholder(dtype=tf.float32, shape=[None, 1], name="x")
```
Notice that the first dimension of our placeholder assigns a `None`. This is
a practical trick to allow working with batches. This just means that we 
don't want to set fix how many data points we can put inside. So we can 
input a vector of size (100, 1) and get 100 calculated values from the network.

If you want to take a look what happens when you print x...
```
<tf.Tensor 'x:0' shape=(?, 1) dtype=float32>
```
... you can see that the internal representation of the None is a `?`.

To emphasize the computation graph representation of a calculation in the 
following I will create our layers in a loop. Our network is relatively 
small we could also do it by hand. However this can be as huge as you want 
it to be

```python
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
```
Our first look at the namescopes lets us assume that we build a graph like 
that:

![f](https://raw.githubusercontent.com/f37/f37.github.io/master/assets/mlp/mlp1.png)

The list `layer` represents the number of units in each layer of the network.
- 1 input,
- 2 x 50 hidden,
- and 1 output unit.

We create tensorflow variables that needs to be assigned with a initial 
value. `tf.matmul` obviously performs a matrix multiplication and `tf.nn.relu`
represents the **rectified linear unit** activation function.  
Note: We also could have taken sigmoid (`tf.nn.sigmoid`) or any other 
activation function. 

![f](https://raw.githubusercontent.com/f37/f37.github.io/master/assets/mlp/mlp_layer.png)

Each layer contains a summary operation (for 
histograms) and the output layer has no activation function for convenience.
Everything else is equal for every layer.

![f](https://raw.githubusercontent.com/f37/f37.github.io/master/assets/mlp/mlp_output.png)

The interested reader also may notice that the vertices of the graph contain
information about the dimension of the operations. Please ignore the nodes 
`loss` and `trainer` for. We will elaborate on that later in this tutorial. 
We just first have to be sure that tensorflow understood what we wanted in out 
loop.

![hidden](https://raw.githubusercontent.com/f37/f37.github.io/master/assets/mlp/mlp_hidden.png)

This looks just perfect. Lets proceed with creating a loss for our little 
network.

### Loss & Training
We have a beautiful computation right now, but in order to really 
approximate something we need a loss function that tells the network how 
he's done. We will make it easy for us and take the euclidean distance of 
label and output.

```python
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
```
Note that the shape of y (our labels) also contains a `None`. So we can 
take more then just one training data. The bigger the batch the faster you 
compute but also the slower you will learn. Figure out your hyperparameters 
by your own.  
Lets see what we have build

![hidden](https://raw.githubusercontent.com/f37/f37.github.io/master/assets/mlp/mlp_loss.png)

Looks nice, it compares the output with the label and calculates the 
euclidean distance. It also calculates a mean for two reasons. First we want
to have scalar values for the summary of the lossfunction. Second, remember
that our placeholder for `x` and `y` are very flexible and could evaluate 
multiple instances of the data set in one run.

The last operation is very easy for a user but a masterpiece of the 
developers of tensorflow. Look how I can command the network that it should 
learn with respect to the lossfunction and the architecture:

```python
with tf.name_scope("trainer"):
    train_op = tf.train.AdamOptimizer().minimize(loss)
```

That is also the explaination why `loss` and `trainer` sneaked inside the 
graph representation of the previous samples. We just decide what our 
lossfunction is that we want to minimize with the Adam Optimizer. Tensorflow
automatically adapts the variables that influence the outcome via 
backpropagation. In the last lesson we learned that tensorflow automatically
can calculate gradients. This is way more exciting.  
You can also decide which variables should be learnable and which not. This 
would be too much for this tutorial.

### Computation
  