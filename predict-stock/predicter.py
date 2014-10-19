#!/usr/bin/python

import sys
import os
from pylearn2.utils import serial
from pylearn2.config import yaml_parse

from stock_data import load_data

try:
    model_path = sys.argv[1]
    test_path = sys.argv[2]
    out_path = sys.argv[3]
except IndexError:
    print "Usage: predict.py <model file> <test file> <output file>"
    quit()

try:
    model = serial.load( model_path )
except Exception, e:
    print model_path + "doesn't seem to be a valid model path, I got this error when trying to load it: "
    print e

#dataset = yaml_parse.load( model.dataset_yaml_src )
dataset = load_data(0, -1, test_path);

# use smallish batches to avoid running out of memory
batch_size = 1
model.set_batch_size(batch_size)

# dataset must be multiple of batch size of some batches will have
# different sizes. theano convolution requires a hard-coded batch size
m = dataset.X.shape[0]
extra = batch_size - m % batch_size
assert (m + extra) % batch_size == 0
import numpy as np
if extra > 0:
    dataset.X = np.concatenate((dataset.X, np.zeros((extra, dataset.X.shape[1]),
    dtype=dataset.X.dtype)), axis=0)

assert dataset.X.shape[0] % batch_size == 0


X = model.get_input_space().make_batch_theano()
Y = model.fprop(X)

from theano import tensor as T
from theano import function

f = function([X], Y)

y = []

for i in xrange(dataset.X.shape[0] / batch_size):
    x_arg = dataset.X[i*batch_size:(i+1)*batch_size,:]
    y.append(f(x_arg.astype(X.dtype)))

y = np.concatenate(y)
print dataset.X.shape
print y.shape

#assert y.ndim == 1
assert y.shape[0] == dataset.X.shape[0]
# discard any zero-padding that was used to give the batches uniform size
y = y[:m]

#exit(0);

out = open(out_path, 'w')
for i in xrange(y.shape[0]):
    out.write('%.6f %.6f\n' % ( dataset.y[i], y[i] ))
out.close()

