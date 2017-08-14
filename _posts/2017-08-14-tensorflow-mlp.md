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

## Code
First we obviously have to import tensorflow and numpy. Additionally we will
use matplotlib for see how well we approximated sinus by comparing the outcome
of the network with the original function visually.

```python
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
```

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
The list `layer` represents the number of units in each layer of the network.
- 1 input,
- 2 x 50 hidden,
- and 1 output unit.

We create tensorflow variables that needs to be assigned with a initial 
value. `tf.matmul` obviously performs a matrix multiplication and `tf.nn.relu`
represents the **rectified linear unit** activation function.  
Note: We also could have taken sigmoid (`tf.nn.sigmoid`) or any other 
activation function. Each layer contains a summary operation (for 
histograms) and the output layer has no activation function for convenience.
Everything else is equal for every layer. Let's have a look what we created:

![f](https://raw.githubusercontent.com/f37/f37.github.io/master/assets/mlp/mlp1.png)