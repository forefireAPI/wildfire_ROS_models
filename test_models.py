#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 08:01:29 2023

A sample of typical use of the code
Just read line by line what tit does and run the file

@author: filippi_j
"""



 
from wildfireROS import fuels_database as fdb
from wildfireROS.runROS import run_model,  plot_results
from wildfireROS.model_set import model_parameters

from wildfireROS.sensitivity import plot_sobol_indices, generate_problem_set, verify_error
from wildfireROS.neuralNetROS import *

import numpy as np


def figure_9_AndrewsRothermel2017():
    A2017 = fdb.load_csv(fdb.AR2017_table_csv)
    A2017_any = fdb.load_csv(fdb.AR2017_anyfueltable_csv)
    
    environment = model_parameters({'wind_miph':10,'slope_deg':0,'mdOnDry1h_r':0.06,'mdOnDry10h_r':0.07,'mdOnDry100h_r':0.08,'mdOnDryLHerb_r':0.6,'mdOnDryLWood_r':0.9}) 
    
    plot_results([run_model("RothermelAndrews2018", fm + A2017_any[0] + environment, "wind_miph", np.arange(0, 20, 0.1)) for fm in A2017], 'wind_miph','ROS_ftmin')




def figure_3_4_Balbi2020():
    pn = fdb.load_csv(fdb.pineNeedlesBalbi2020_csv)[0] + model_parameters({'wind_mps':0,'slope_deg':0 })
    
    p_set = []
    for value in [0.08, 0.3, 0.8]:
        new_pn = model_parameters(pn.get_set())
        new_pn.fl1h_kgm2 = value
        new_pn.CODE = f"Pine Needles load {value}"
        p_set.append(new_pn)
    
    plot_results([run_model("Balbi2020", fm , "wind_mps", np.arange(0, 12, 1)) for fm in p_set], 'wind_mps','ROS_mps')
    
    p_set = []
    for value in [0.2, 8]:
        new_pn = model_parameters(pn.get_set())
        new_pn.fl1h_kgm2 = 0.9 #table. 2
        new_pn.wind_mps = value
        new_pn.CODE = f"Pine Needles wind {value}"
        p_set.append(new_pn)
    
    W02,W03 = [run_model("Balbi2020", fm , "mdOnDry1h_kgm2", np.arange(0.00, 0.9, 0.05) ) for fm in p_set]
    
    W02["results"].RelativeRos = W02["results"].ROS / W02["results"].ROS[0]
    W03["results"].RelativeRos = W03["results"].ROS / W03["results"].ROS[0]
    
    plot_results([W02,W03], 'mdOnDry1h_kgm2','RelativeRos_r')

    
import matplotlib.pyplot as plt
figure_9_AndrewsRothermel2017()
plt.show()
# figure_3_4_Balbi2020()

# plot_sobol_indices(generate_problem_set("AndrewsRothermel2017",  N= 1000))
# plot_sobol_indices(generate_problem_set("Rothermel1972",  N= 100))
# plot_sobol_indices(generate_problem_set("Balbi2020",  N= 100))

# model_path = "Rothermel1972ANNs"

# pset = generate_problem_set("Rothermel1972",  N= 200)
# train_wildfire_speed_emulator(pset,model_path)
# pset2 = add_results_emulation(pset, model_path)
# pset3 = add_results_emulation(generate_problem_set("Rothermel1972",  N= 100), model_path)

# print("Initial error ",verify_error(pset))
# print("Learn set error ",verify_error(pset2,lookat='results_emulation'))
# print("Other set error ",verify_error(pset3,lookat='results_emulation'))

# plot_sobol_indices(generate_problem_set("Rothermel1972",  N= 100))
# plot_sobol_indices(pset2,lookat='results_emulation')
# plot_sobol_indices(pset3,lookat='results_emulation')


