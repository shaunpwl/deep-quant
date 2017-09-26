# Copyright 2016 Euclidean Technologies Management LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
import os
import sys
import copy

import numpy as np
import tensorflow as tf
import regex as re

from tensorflow.python.platform import gfile
from batch_generator import BatchGenerator

import model_utils

def predict(config):

  path = model_utils.get_data_path(config.data_dir,config.datafile)

  config.batch_size = 1  
  batches = BatchGenerator(path,config)

  tf_config = tf.ConfigProto( allow_soft_placement=True  ,
                              log_device_placement=False )

  with tf.Graph().as_default(), tf.Session(config=tf_config) as session:

    model = model_utils.get_model(session, config, verbose=False)

    print("Num data points is %d"%batches.num_batches)
    
    for i in range(batches.num_batches):

      batch = batches.next_batch()

      (mse, preds) = model.step(session, batch)

      key     = batch.attribs[-1][0][0]
      date    = batch.attribs[-1][0][1]
      inputs  = batch.inputs[-1][0]
      targets = batch.targets[-1][0]
      outputs = preds[0]
      
      print("%s %s "%(key,date))
      print(inputs)
      print(targets)
      print(outputs)
      print("--------------------------------")