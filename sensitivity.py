#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 12:14:58 2023

helper functions to perform and plot sensitivity analysis

@author: filippi_j
"""

from SALib.sample import saltelli
from SALib.analyze import sobol
from wildfireROS import fuels_database as fdb
from wildfireROS.runROS import *
from wildfireROS.model_set import model_parameters
from wildfireROS.Balbi2020 import *
import numpy as np




# Define the model inputs for SALib



fm = fdb.load_csv(fdb.pineNeedlesBalbi2020_csv)[0] + model_parameters({'wind_mps':2,'slope_deg':10 })

def is_number_tryexcept(s):
    """ Returns True if string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def generate_look_at(fmset, percentage):
    look_at = {}

    for param, value in fmset.items():
        if is_number_tryexcept(str(value)):  # Check if the value is numeric
            delta = value * percentage
            look_at[param] = [max(value - delta, 0), value + delta]  # Ensuring non-negative lower bounds
        else:
            print(param, " not a number")

    return look_at

look_at = generate_look_at(fm, 0.02)

look_at = {'Ta': [294.0, 306.0],
         'Ti': [588.0, 612.0],
         'Tvap': [365.54, 380.46],
         'Tau0': [74079.18, 77102.82],
         'hEvap': [2254.0, 2346.0],
         'H': [17052.0, 17748.0],
         'Cpf': [1989.4, 2070.6],
         'Cpa': [1127.0, 1173.0],
         'X0': [0.294, 0.306],
         'st': [16.66, 17.34],
         'fl1h': [0.392, 0.40800000000000003],
         'SAV1h': [5880.0, 6120.0],
         'fd': [0.098, 0.10200000000000001],
         'mdOnDry1h': [0.098, 0.10200000000000001],
         'fuelDens': [490.0, 510.0],
         'airDens': [1.2005000000000001, 1.2495],
         'wind': [1.96, 2.04],
         'slope_deg': [0, 0.001]
    }



problem = {
    'num_vars': len(look_at),
    'names': list(look_at.keys()),
    'bounds': [look_at[name] for name in look_at.keys()]
}


model_name = "Balbi2020"
# Generate samples



param_values = saltelli.sample(problem, 1000)


# Empty list to hold model results
model_results = []

# Run model for each set of parameters
for params in param_values:
    # Update the fm with the new parameters
    for i, param_name in enumerate(problem['names']):
        fm[param_name] = params[i]
    # Run the model
    result = model_parameters(ROS_models[model_name](fm))

    # Append the result (e.g., ROS) to the list
    model_results.append(result.ROS)

# Convert results to a NumPy array
Y = np.array(model_results)

# Perform the sensitivity analysis
Si = sobol.analyze(problem, Y)

# Print the results
def plot_sobol_indices(Si, problem):
    params = problem['names']
    indices = Si['S1']
    total_indices = Si['ST']
    
    y_pos = np.arange(len(params))

    plt.figure(figsize=(10, 5))

    # Plotting first-order indices
    plt.subplot(1, 2, 1)
    plt.barh(y_pos, indices, align='center', color='skyblue')
    plt.yticks(y_pos, params)
    plt.xlabel('First-order Sobol Index')
    plt.title('First-order Sensitivity Indices')

    # Plotting total-effect indices
    plt.subplot(1, 2, 2)
    plt.barh(y_pos, total_indices, align='center', color='salmon')
    plt.yticks(y_pos, params)
    plt.xlabel('Total-effect Sobol Index')
    plt.title('Total-effect Sensitivity Indices')

    plt.tight_layout()
    plt.show()

# Call the function with your Sobol indices and problem definition
plot_sobol_indices(Si, problem)