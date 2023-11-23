#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 12:25:51 2023

Wildfire ROS Model - Machine learning emulator

Description:
This module contains a class to use a multilayered interpolator of a model,
and methods to generate data and train it

Author: Jean-Baptiste Filippi
Organization: CNRS
License: GPL

"""

import numpy as np
import tensorflow as tf
import sobol_seq
from sklearn.model_selection import train_test_split

def data_generation(problem, ROS_models, model_name, num_samples=1000):
    import sobol_seq as sobolsample
    param_values = sobolsample.i4_sobol_generate(problem['num_vars'], num_samples)
    model_results = []

    for params in param_values:
        fm = {name: value for name, value in zip(problem['names'], params)}
        result = model_parameters(ROS_models[model_name](fm))
        model_results.append(result.ROS)

    return param_values, model_results


def train(X_train, Y_train, X_val, Y_val, model_path):
    import tensorflow as tf

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, Y_train, epochs=100, validation_data=(X_val, Y_val))

    model.save(model_path)  # Saving the model
    return model


class ModelPrediction:
    def __init__(self, model_path, look_at):
        import tensorflow as tf
        self.model = tf.keras.models.load_model(model_path)
        self.look_at = look_at
        self.feature_order = list(look_at.keys())  # Extracting the order of features

    def align_features(self, input_data):
        # Reorder the input_data to match the order in self.feature_order
        aligned_data = []
        for feature in self.feature_order:
            if feature in input_data:
                aligned_data.append(input_data[feature])
            else:
                raise ValueError(f"Feature {feature} missing in input data")
        return aligned_data

    def predict(self, input_data):
        aligned_data = self.align_features(input_data)
        predictions = self.model.predict([aligned_data])
        return predictions