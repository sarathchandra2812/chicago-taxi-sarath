#!/usr/bin/env python
# coding: utf-8

# In[2]:


# This document follows Google's published example: 
# https://github.com/GoogleCloudPlatform/professional-services/tree/master/examples/cloudml-energy-price-forecasting
# ==============================================================================

"""
This file sets the parameters and runs the model.
"""

import sys; sys.argv=['']; del sys

import argparse
import json
import os
import numpy as np
import pandas as pd
import tensorflow as tf
import inputs
import model


def initialise_params():
    """
    Sets parameters
    """
    args_parser = argparse.ArgumentParser()

    args_parser.add_argument(
        '--training_path',
        help='Location to training data.',
        default='gs://taxi_fare_3/data/csv/train.csv' 
    )
    args_parser.add_argument(
        '--validation_path',
        help='Location to validation data.',
        default='gs://taxi_fare_3/data/csv/eval.csv'
    )
    args_parser.add_argument(
        '--hidden1',
        help='Hidden Units 1',
        default=128
    )
    args_parser.add_argument(
        '--hidden2',
        help='Hidden Units 2',
        default=96
    )
    args_parser.add_argument(
        '--hidden3',
        help='Hidden Units 3',
        default=16
    )
    args_parser.add_argument(
        '--learning_rate',
        help='Learning rate.',
        default=0.000001,
        type=float
    )
    args_parser.add_argument(
        '--batch_size',
        help='Training batch size.',
        default=64,
        type=int
    )
    args_parser.add_argument(
        '--hidden_units',
        help='Training batch size.',
        default=[128, 32, 4]
    )
    args_parser.add_argument(
        '--eval_batch_size',
        help='Evaluation batch size.',
        default=168,
        type=int
    )
    args_parser.add_argument(
        '--max_steps',
        help='Maximum steps for training.',
        default=25000,
        type=int
    )
    args_parser.add_argument(
        '--nbuckets',
        help='Number of buckets for bucketing latitude and longitude.',
        default=20,
        type=int
    )
    return args_parser.parse_args()



def run_experiment(run_config, parameters):
    """
    This funtion runs the tensorflow model.
    """
    estimator = model.create_regressor(
        config = run_config, parameters=parameters)
    train_spec = inputs.get_train_spec(
        parameters.training_path,
        parameters.batch_size,
        parameters.max_steps)
    eval_spec = inputs.get_eval_spec(
        parameters.validation_path,
        parameters.eval_batch_size)

    tf.estimator.train_and_evaluate(
        estimator,
        train_spec,
        eval_spec
    )


def main():
    """
    This main function executes the job.
    """
    parameters = initialise_params()
    tf.logging.set_verbosity(tf.logging.INFO)

    model_dir = 'gs://taxi_fare_3/log/'
        
    run_config = tf.estimator.RunConfig(
        log_step_count_steps=1000,
        save_checkpoints_secs=120,
        keep_checkpoint_max=3,
        model_dir=model_dir
    )
    run_experiment(run_config, parameters)


if __name__ == '__main__':
    main()
