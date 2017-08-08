---
layout: post
comments: true
title:  "Tensorflow 101"
excerpt: "Introduction to tensorflow"
date:   2017-08-17
mathjax: true
---

# Tensorflow 101

## tensorflow vs. numpy
Explanation of the different of the programming approach.
We will skip variable initialization, loops, functions and library calls. I 
want to give the bridge what we are doing and how we are doing it. The tools
you have to find yourself. We have infinite possibilities thats why I never 
can cover the whole tensorflow, because of that it is important that you know 
the documentation and how to use it
LINK TO NUMPY DOC
LINK TO TENSORFLOW DOC
BEISPIELANWENDUNG IMMER VON BENUTZUNG!

### similarities

#### arrays and tensors
We will begin with the basic tools you need. Tensors/Arrays

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