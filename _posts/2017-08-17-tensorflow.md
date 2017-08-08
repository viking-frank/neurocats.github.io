---
layout: post
comments: true
title:  "Tensorflow 101"
excerpt: "Introduction to tensorflow"
date:   2017-08-17
mathjax: true
---

# Tensorflow 101

## Introduction
We will elaborate the different approaches on programming python, numpy and 
tensorflow. We won't be a beginner tutorial that talks about variable 
initialization, loops, function, classes, library calls and hello world.

I want to give a framework on how to think about the approaches such that 
everybody can use the provides tools on their own.

Please learn how to read documentations and finding tools by your own. Think
about your problems and search for the tools that are needed and not the 
other way round. Please refer to the following documentations:
- [python docs](https://docs.python.org/3/)
- [numpy docs](https://docs.scipy.org/doc/)
- [tensorflow docs](https://www.tensorflow.org/api_docs/python/)

## Why are we doing what we are doing?

### What is python?
> Python is a programming language that lets you **work quickly** and 
**integrate systems** more effectively. 
**- python.org**

This just means **python** is
- multi-purpose, especially cross-platform and
- can easily combine different systems.

In short: It can do everything but nothing right. On the contrary it is slow 
and hard to parallelize, because it doesn't live deep inside the system like
c++ etc.
### What is numpy?
> NumPy is the fundamental **package** for scientific computing with Python. 
**- numpy.org**

Python is loved by the scientific community because of the variety of 
scientific computing packages i.e. **numpy**, scipy. This gives the 
developer the beauty of python syntax by easily providing scientific 
tools i.e. matrix computation, sparse computation.
 

### What is tensorflow?
> An open-source software **library** for Machine Intelligence.
**- tensorflow.org**

Tensorflow is a c++ library. In detail think of tensorflow as an API. It is 
fast, can comunicate with the GPU and can therefore parallelize computations.
Furthermore tensorflow has a deeper understanding of your computation. It
is able to compute a symbolical derivative of a mathematical function and 
knows which part of the computation can work in parallel.  
We will elaborate on that in more detail in this tutorial.

### What the fuck?
What we are doing basically is using pythons power of integrating systems 
with the tensorflow library. We are communicating with the GPU over 
tensorflow controlled by python and therefore illuminating pythons bad habits.

### Similarities

#### arrays and tensors
We will begin with the basic tools you need. **Tensors/Arrays**.

We will create a numpy array of dimension 2 and a tensor of rank 2
```python
import tensorflow as tf
import numpy as np

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
```
Outputs:
```
Numpy Matrix:
 [[ 0.  0.  0.]
  [ 0.  0.  0.]
  [ 0.  0.  0.]] 
  
Tensorflow node:
 Tensor("zeros_1:0", shape=(3, 3), dtype=float32)
 
Tensorflow node value:
 [[ 0.  0.  0.]
  [ 0.  0.  0.]
  [ 0.  0.  0.]] 
```

# Notes
we still work in python, but we are using tensorflow (C++) library (schneller
als python) Python ist eher eine elegante multi-purpose language tensorflow 
ein hochspezialisiertes hochgeschwindigkeits modul f?r graph computation.


disadvantages tensorflow: schleifen "unm?glich" man will auf der GPU ebene
flown: beispiel SeqMDN training und inferenz (GPU/CPU)