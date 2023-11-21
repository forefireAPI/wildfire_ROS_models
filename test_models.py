#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 08:01:29 2023

A sample of typical use of the code
Just read line by line what tit does and run the file

@author: filippi_j
"""





# all imports from code

 
from wildfireROS import fuels_database as fdb
from wildfireROS.runROS import run_model, plot_results
from wildfireROS.model_set import model_parameters

import numpy as np




#SB2005 = fdb.load_csv(fdb.CB2005_t7_csv)

A2017 = fdb.load_csv(fdb.AR2017_table_csv)
A2017_any = fdb.load_csv(fdb.AR2017_anyfueltable_csv)



environment = model_parameters({'wind_miph':10,'slope_deg':0,'mdOnDry1h_r':0.06,'mdOnDry10h_r':0.07,'mdOnDry100h_r':0.08,'mdOnDryLHerb_r':0.6,'mdOnDryLWood_r':0.9})

plot_results([run_model("Rothermel1972", fm + A2017_any[0] + environment, "wind_miph", np.arange(0, 20, 0.1)) for fm in A2017], 'wind_miph','ROS_ftmin')

pineNeedlesBalbi2020 = fdb.load_csv(fdb.pineNeedlesBalbi2020_csv)

environment = model_parameters({'wind_miph':10,'slope_deg':0 })


plot_results([run_model("Balbi2020", fm +environment , "wind_mps", np.arange(0, 20, 0.1)) for fm in pineNeedlesBalbi2020], 'wind_mps','ROS_mps')




