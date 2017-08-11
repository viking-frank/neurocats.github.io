---
layout: post
comments: true
title:  "Introduction to Tensorflow - 01 Basics"
excerpt: "While giving an overview for python, numpy and tensorflow I want 
to create a basic understanding of tensorflows graph representation for the 
reader."
date:   2017-08-17
mathjax: true
---

# Tensorflow basics

## Introduction
We will explore the different approaches on programming python, numpy and 
tensorflow. This won't be a beginner tutorial that talks about variable 
initialization, loops, function, classes, library calls and saying hello to a
world.

I want to give you a framework on how to think about the different approaches 
such that you can use the provided tools on your own.

Please learn how to read documentations and finding all tools needed. Think
about your problems and search for the gadgets that are needed for 
solving the problem. Don't think about your known tools and try to figure 
out a solution with static knowledge. You may be successful upto a certain 
point. But your code can never be efficient and most importantly - beautiful. 
**Own your code!**  
Please refer to the following documentations:
- [python docs](https://docs.python.org/3/)
- [numpy docs](https://docs.scipy.org/doc/)
- [tensorflow docs](https://www.tensorflow.org/api_docs/python/)

## Python, Numpy, Tensorflow?
![python](https://raw.githubusercontent.com/f37/f37.github.io/master/assets/tensorflow/python-logo.png)
![python](https://raw.githubusercontent.com/f37/f37.github.io/master/assets/tensorflow/numpy.jpg)
![python](https://raw.githubusercontent.com/f37/f37.github.io/master/assets/tensorflow/tensorflow.png)

We first have to make clear, what is there for mathematical programming. 
What is used for which purpose? Which Problems are more efficiently solved 
with which tool?

### What is python?
> Python is a programming language that lets you **work quickly** and 
**integrate systems** more effectively. 
**- python.org**

This just means **python** is
- multi-purpose, (especially cross-platform) and
- can easily combine different systems.

In short: It can do everything everywhere but nothing right or in the most 
efficient way. It is slow and hard to parallelize, because it doesn't live 
deep inside the system like C++ etc. However it is elegant and easy to use.

### What is numpy?
> NumPy is the fundamental **package** for scientific computing with Python. 
**- numpy.org**

Python is loved by the scientific community because of the variety of 
scientific computing packages e.g. **numpy**, scipy. This gives the 
developer the beauty of using python syntax by easily providing mathematical 
tools e.g. matrix computation.
 

### What is tensorflow?
> An open-source software **library** for Machine Intelligence.
**- tensorflow.org**

Tensorflow is a C++ library. In detail think of tensorflow as an API. With a
python interface. It is fast, can communicate with the GPU and can therefore
parallelize computations. Furthermore tensorflow has a more general 
respresentation of a computation. It is able to compute a symbolical 
derivative of a mathematical function and knows which part of the 
computation can work in parallel.  
We will elaborate on that in more detail in this tutorial.

### What the fuck?
What we are doing basically is using pythons power of elegantly integrating 
systems with the tensorflow library (via python API). We are communicating 
with the GPU over tensorflow controlled by python. We are combining easy to 
use python with fast but complicated C++ and taking the best properties 
respectively.

## Tensorflow philosophy
I will give an overview how tensorflow calculates and give a practical 
example of the concrete difference to pure python in the next section.

### It's all about computation graphs
One field in theoretical computer science represents mathematical 
operations in a graph. Tensorflow is a tool where you can build computation 
graphs and provides functions like derivation that makes the use of an 
formula easier. Tensorflow provides nodes that you can feed with numpy 
values and gives the possibility to ask for each nodes value given the input
(or constant).

Never forget. You are building a graph. When you want to evaluate a variable
(graph node) you can only do it in a so called 'tensorflow session'. Outside
such a session you will just see an abstract graph build in your desired 
architecture.

## Basic tools
We will take a look at the basic calculating units and operations. Always 
trying to find out why numpy isn't sufficient for 
> letting tensors flow.

### arrays/tensors
You will always need **Tensors/Arrays**. So let's start with the smallest 
non-trivial example: A tensor of rank 2; Or: A Matrix.

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
value. Like I mentioned tensorflow creates a abstract graph object. We can 
build it over python and can evaluate it in a tensorflow session. 
- The first printout `Tensorflow node` is a representation of the abstract 
node of the computation graph that was build at the initialization.  
- The second printout `Tensorflow node value` is the value of the node that 
was assigned with that computation. It was evaluated in a tensorflow session.

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
Notice that every seemingly variable initialization step is a birth of a 
node in the computation graph. You feed it with the properties/parameter, 
even a name.

2. Execute the actual computation in a tensorflow session.
```python
# Starting the session
with tf.Session() as sess:
    # initialize all variables
    sess.run(tf.global_variables_initializer())
    # provide the results for tensorboard (a visualization tool)
    writer = tf.summary.FileWriter('./graphs', sess.graph)
    # evaluate the value of a certain node
    node = sess.run(tfResult)
    
    # evaluate the value of any node of the computation graph
    sumand1, sumand2 = sess.run([tfMatrix, tfMatrix2])
writer.close()
```
Computation graph:  
![ex_II](https://raw.githubusercontent.com/f37/f37.github.io/master/assets/tensorflow/ex_II.png)

As seen in the picture of the computation graph you have created 3 nodes 
(summand, summand, sum). We can ask for every assigned value for that given 
computation in every node. Tensorflow will calculate it via C++ API, not 
with native python like in the numpy case.

I created that graph with tensorboard. Its a tool that converts
so called tensorflow summaries into a visualization. With that there arises 
namescoping, building summaries etc. I will elaborate on that in the next 
section while I show you how tensorflow can compute symbolic derivations, 
impossible for pure python.
