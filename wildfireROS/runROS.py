#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 16:19:43 2023

helper functions to run and plot models

@author: filippi_j
"""

import matplotlib.pyplot as plt
import numpy as np
 
from .model_set import model_parameters
from .RothermelAndrews2018 import Rothermel1972, RothermelAndrews2018
from .Balbi2020 import Balbi2020

ROS_models = {
    "Rothermel1972": Rothermel1972,
    "AndrewsRothermel2017": RothermelAndrews2018,
    "Balbi2020": Balbi2020
}

def run_model(ROS_model_name, fuel_model, param_name, values_range):
    
    out_values = []
    initial_value =  getattr(fuel_model, param_name)
    model_function = ROS_models[ROS_model_name]
    
    for value in values_range:
        setattr(fuel_model, param_name, value)
        rset = model_parameters(model_function(fuel_model))
        setattr(rset, param_name, value)
        out_values.append(rset)
        
    # retrun to initial value
    setattr(fuel_model, param_name, initial_value)
    
    if len(out_values) == 0:
        return {}
    
    keys = out_values[0].keys()
    
    for item in out_values:
        keys = out_values[0].keys()
    
    result_arrays = {}
    
    for key in keys:
        result_arrays[key] = []

    for result in out_values:
        for key in keys:
            result_arrays[key].append(result[key])

    

    return {"Model" :ROS_model_name,
            "FUELCODE" : fuel_model.CODE,
            "results" : model_parameters({key: np.array(result_arrays[key]) for key in keys})
            }

def plot_results(resultSets, keyX, keyY):    
    plt.figure(figsize=(10, 6))
     
    for entry in resultSets:
        plt.plot(entry['results'][keyX],entry['results'][keyY], label=f"{entry['Model']} {entry['FUELCODE']}")
    
    plt.xlabel(model_parameters.str_full_name(keyX))
    plt.ylabel(model_parameters.str_full_name(keyY))
    
    plt.legend()
    plt.grid(True)


