#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 08:01:29 2023

A sample of typical use of the code
Just read line by line what tit does and run the file

@author: filippi_j
"""





# all imports from code
from wildfireROS import RothermelAndrews2018 as Rothermel
from wildfireROS import Balbi2020 as Balbi
 
from wildfireROS import fuels_database as fdb
from wildfireROS.model_set import model_parameters

# calling function to test models
#Balbi.test_plot() 


environment = {'wind_miph':10,'slope_deg':0,'mdOnDry1h_r':0.06,'mdOnDry10h_r':0.07,'mdOnDry100h_r':0.08,'mdOnDryLHerb_r':0.6,'mdOnDryLWood_r':0.9}

SB2005 = fdb.load_csv(fdb.CB2005_t7_csv)
A2017 = fdb.load_csv(fdb.AR2017_table_csv)
A2017_any = fdb.load_csv(fdb.AR2017_anyfueltable_csv)

for element in A2017:
    element.load(A2017_any[0].get_set())
    element.load(environment)


import matplotlib.pyplot as plt
import numpy as np
	
# Create an array of wind speeds from 0 to 10 mph
wind_speeds = np.arange(0, 20, 0.1)  # 0 to 10 mph in steps of 1 mph

# Plotting
plt.figure(figsize=(10, 6))

for fm in A2017:
    ros_values = []
    for wind_speed in wind_speeds:
        fm.wind_miph = wind_speed
        rset = model_parameters(Rothermel.Rothermel1972(fm))
        ros_values.append(rset.ROS_ftmin)
        

    plt.plot(wind_speeds, ros_values, label=f'{fm.CODE}')

plt.xlabel('Wind Speed (miph)')
plt.ylabel('ROS (ft/min)')
plt.title('ROS vs Wind Speed for Different fm Objects')
plt.legend()
plt.grid(True)
plt.show()