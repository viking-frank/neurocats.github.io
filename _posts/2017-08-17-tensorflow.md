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

## Basic tools

### arrays/tensors
You will always need **Tensors/Arrays**. So let's start with the smalles 
non-trivial example of rank 2. Or: A Matrix.

```python
import numpy as np
import tensorflow as tf

# create a matrix
npMatrix = np.zeros(shape=(3, 3), dtype=np.float32)
tfMatrix = tf.zeros(shape=(3, 3), dtype=tf.float32, name="tfMatrix")

# print out results
print("Numpy Matrix:\n", npMatrix, "\n")
print("Tensorflow node:\n", tfMatrix, "\n")

# or maybe in the right way for tensorflow
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

As Watson would perceive the Tensorflow node is completely different to its 
value. How can that make sense?

To make that clear please analyse the outcome of the next example. We will 
now add up 2 matrices.

```python
import numpy as np
import tensorflow as tf

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
    print("Summands:\n", "first:\n", sumand1, "second:\n", summand2)
writer.close()
```
Output:

```
Numpy result:
 [[ 1.  0.  0.]
  [ 0.  1.  0.]
  [ 0.  0.  1.]] 

Tensorflow result node:
 Tensor("tfResult:0", shape=(3, 3), dtype=float32) 

Tensorflow result:
 [[ 1.  0.  0.]
  [ 0.  1.  0.]
  [ 0.  0.  1.]] 
  
Summands:
 first:
  [[ 0.  0.  0.]
   [ 0.  0.  0.]
   [ 0.  0.  0.]] 
 second:
  [[ 1.  0.  0.]
   [ 0.  1.  0.]
   [ 0.  0.  1.]]

```

#### What happened?
We understood that numpy is just able to print out any result while tensorflow
needs some special treatment. So we need to understand why tensorflow does 
what tensorflow does and why it is practicable.

Tensorflow has two workflows.
1. Building the computation graph.
```python
# Summand
tfMatrix = tf.constant(npMatrix, dtype=tf.float32, name="tfMatrix")
# Summand
tfMatrix2 = tf.constant(npMatrix2, dtype=tf.float32, name="tfMatrix2")
# Sum
tfResult = tf.add(tfMatrix, tfMatrix2, name="tfResult")
```
Computation graph:  
![ex_II](https://github.com/f37/f37.github.io/blob/master/assets/tensorflow/ex_II.png?raw=true)

2. Execute the actual computation in a tensorflow session.
```python
# Starting the session
with tf.Session() as sess:
    # Initialize all variables
    sess.run(tf.global_variables_initializer())
    # Providing the results in tensorboard (a visualization tool)
    writer = tf.summary.FileWriter('./graphs', sess.graph)
    # Calculate the value of a certain node
    node = sess.run(tfResult)
    
    # calculate the value of any node of the computation graph
    sumand1, sumand2 = sess.run([tfMatrix, tfMatrix2])
writer.close()
```

As seen in the picture of the computation graph. You have 3 nodes in 
the computation graph. We can ask for the value in any step of the 
calculation with a tensorflow session. Tensorflow will calculate it over a 
C++ API, not with python like in numpy case. What features that brings we 
will see in the next section.

### Advanced Features
#### Derivation
#### GPU contact
Image with and without, maybe time comparison.
#### Building neural net
#### Visual debugging
Give example.

# Notes
we still work in python, but we are using tensorflow (C++) library (schneller
als python) Python ist eher eine elegante multi-purpose language tensorflow 
ein hochspezialisiertes hochgeschwindigkeits modul f?r graph computation.


disadvantages tensorflow: schleifen "unm?glich" man will auf der GPU ebene
flown: beispiel SeqMDN training und inferenz (GPU/CPU)