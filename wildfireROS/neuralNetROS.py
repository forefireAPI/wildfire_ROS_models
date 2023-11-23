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


from .model_set import model_parameters, var_properties
from .sensitivity import generate_problem_set

def train_wildfire_speed_emulator(problem,model_path):
    # Extracting data
    X = problem['input']  # Feature matrix
    y = problem['results']  # Target values

    # Define a neural network model suitable for regression
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(32, activation='relu', input_shape=(problem['num_vars'],)),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1)  # Output layer for regression
    ])

    # Compile the model for regression
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(X, y, epochs=80, batch_size=32)  # Epochs and batch_size can be adjusted based on the dataset size

    model.save(model_path)  # Saving the model
    return model

def add_results_emulation(problem, model_path):
    # Load the trained model
    model = tf.keras.models.load_model(model_path)

    # Prepare input data - assuming 'input' is already in the correct format
    input_data = problem['input']

    # Check if input_data dimensions match num_vars
    if input_data.shape[1] != problem['num_vars']:
        raise ValueError("Input data dimensions do not match the number of variables")

    # Make predictions
    predictions = model.predict(input_data)

    # Update the problem dictionary with predictions
    problem['results_emulation'] = predictions.flatten()  # Flatten in case predictions are in 2D array

    return problem

def predict_single_output(model_path, input_dict):
    # Load the trained model
    model = tf.keras.models.load_model(model_path)

    # Prepare the input data in the correct order
    input_order = input_dict['names']
    input_values = np.array([input_dict['input'][name] for name in input_order])

    # Reshape input_values for a single prediction
    input_values = input_values.reshape(1, -1)

    # Make the prediction
    prediction = model.predict(input_values)

    # Return the scalar result
    return model_parameters({"ROS":prediction[0, 0]}) 