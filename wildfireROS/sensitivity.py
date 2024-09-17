#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 12:14:58 2023

helper functions to perform and plot sensitivity analysis

@author: filippi_j
"""

from SALib.analyze import sobol
from SALib.sample import sobol as sobolsample

from .runROS import ROS_models
from .model_set import model_parameters, var_properties

import matplotlib.pyplot as plt
import numpy as np
import math

    
def generate_problem_set(model_key, kind_of_parameter = ["environment","typical","fuelstate"], result_var="ROS", N = 10000):

    modelVSet  =  ROS_models[model_key]["get_set"]()
    
    fm = {}
    for key in modelVSet.keys():
        for var_key in modelVSet[key]:
            fm[var_key] = modelVSet[key][var_key]
    
    fm_var_set = {}
    for key in kind_of_parameter:
        for var_key in modelVSet[key]:
            fm_var_set[var_key] = modelVSet[key][var_key]
        
    problem = {
        'model_name':model_key,
        'num_vars': len(fm_var_set.keys()),
        'names': list(fm_var_set.keys()),
        'bounds': [var_properties[name]["range"] for name in fm_var_set.keys()]
    }
    
    param_values = sobolsample.sample(problem, N)
    problem["input"] = param_values

    model_results = []    
    for params in param_values:
        for i, param_name in enumerate(problem['names']):
            fm[param_name] = params[i]
        fm = model_parameters(fm)
        result = model_parameters(ROS_models[model_key]["get_values"](fm))
    
        model_results.append(result[result_var])
        
    problem["result_var"] = result_var
    problem["results"] = np.array(model_results)
    
    return problem



def verify_error(problem_set, lookat="results"):
    model_key = problem_set["model_name"]
    modelVSet  =  ROS_models[model_key]["get_set"]()
    fm = model_parameters()
    diff = 0
    numSamples = len(problem_set[lookat])
    for key in modelVSet.keys():
        fm = fm+modelVSet[key]
    for I in range(numSamples):
        input_values = problem_set["input"][I]
        for i, param_name in enumerate(problem_set['names']):
            fm[param_name] = input_values[i]
            
        result = model_parameters(ROS_models[model_key]["get_values"](fm))
        diff = diff + abs(result[problem_set["result_var"]] - problem_set[lookat][I])
         
    return diff/numSamples
            
def plot_sobol_indices(problem_set, lookat="results"):
    
    Si = sobol.analyze(problem_set, problem_set[lookat])
    params = problem_set['names']
    indices = Si['S1']
    total_indices = Si['ST']
    
    model_name = problem_set["model_name"]
    
    y_pos = np.arange(len(params))

    plt.figure(figsize=(10, 5))

    # Plotting first-order indices
    plt.subplot(1, 2, 1)
    plt.barh(y_pos, indices, align='center', color='skyblue')
    plt.yticks(y_pos, params)
    plt.xlabel('First-order Sobol Index')
    plt.title(f"First-order {model_name}")

    # Plotting total-effect indices
    plt.subplot(1, 2, 2)
    plt.barh(y_pos, total_indices, align='center', color='salmon')
    plt.yticks(y_pos, params)
   
    plt.xlabel("Total-effect Sobol Index")
    plt.title(f"Total-effect {model_name}")

    plt.tight_layout()
    plt.show()


    
