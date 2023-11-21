#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wildfire ROS Model - Balbi2020

Description:
This module contains the implementation of the Balbi 2020 for predicting the Rate of Spread (ROS) of wildfires.
It is based on Balbi et. al. IJWF 2020 A convective–radiative propagation model for wildland fires 10.1071/WF19103

Author: Jean-Baptiste Filippi
Organization: CNRS
License: GPL

Usage:
from models.[model_file_name] import [ModelClassName]

"""
import math
import numpy as np
import matplotlib.pyplot as plt

def Balbi2020(valueOf):
    # Constants
 
    PI = math.pi

   # Fuel Specific
    lh = valueOf['e']
    if lh <= 0:
        return 0
    lrhov = valueOf['Rhod']
    lm = valueOf['Md']
    ls = valueOf['sd']
    lsigma = valueOf['Sigmad']
    lrhoa = valueOf['RhoA']
    lCp = valueOf['Cpv']
    lTa = valueOf['Ta']
    lTi = valueOf['Ti']
    lDeltah = valueOf['Deltah']
    lDeltaH = valueOf['DeltaH']
    lr00 = valueOf['r00']
    ltau0 = valueOf['Tau0']
    Tvap = valueOf["Tvap"] = 373 # nomenclature
    Cpa =  valueOf["Cpa"] = 1150 # nomenclature
    K1 = valueOf["K1"] = 130 # nomenclature
    st = valueOf["st"] = 17 # nomenclature
    B = valueOf["B"] = 5.6e-8 # nomenclature
    lg = valueOf["g"] = 9.81 # nomenclature
    lChi0 = valueOf['X0']
    
    
    lU = 0
    RU = valueOf['wind']
    if RU > 0:
        lU = RU

    lalpha = math.atan(valueOf['slope'])

    R = 0.1  # first guess in iteration
    Rnew = 0
    maxEps = 0.001
    N = 400
    step = 1
    stopcondition = True
     
    flag = 1
    error = 0;
       
    # Packing ratio
    Beta = lsigma / (lh * lrhov)
    #Leaf Area ratio just before eq. 13 S is the total fuel surface area per horizontal area unit of fuel bed and denotes the double of the leaf area index (LAI)
    S = ls * Beta * lh
    #Ignition energy (J/kg) # eq. 9
    q = lCp * (lTi - lTa) + lm * (lDeltah + lCp * (Tvap - lTa))
    # scaling factor eq. 17
    ar = min(S / (2 * PI), 1.)
    # Radiative factor # eq. 16
    A = ar * ((lChi0 * lDeltaH) / (4 * q))
    # coefficient p required for T derived from expression between C7 and C8 
    p = (2 / lr00) / ltau0
    
    while stopcondition:

        # Radiant fractor eq. C7 
        Chi = lChi0 / (1 + p * ((R * ltau0 * math.cos(lalpha)) / (2 * ls)))
        # Mean Flame Temperature eq. B11
        T = lTa + lDeltaH * ((1 - Chi) / (Cpa * (st + 1)))
        # reference vertical velocity eq. B9
        u0 = 2 * (st + 1) / ltau0 * T / lTa * lrhov / lrhoa * min(S, 2 * PI)
        # flame angle
        gamma = math.atan(math.tan(lalpha) + (lU / u0))
        #Flame Height
        H = (u0 ** 2) / (lg * (T / lTa - 1.))
        
        Rb = min((S / PI), 1.) * ((B * (T ** 4)) / (Beta * lrhov * q))
        Rc1 = ls * (lDeltaH /(q*ltau0)) * min(lh, (2*PI)/(ls*Beta));
        Rc2 = (lh/(2*lh+H))  *  math.tan(lalpha)  + ( (lU*math.exp(-K1*pow(Beta,0.5)*R)) / u0);
        Rc = Rc1*Rc2    # eq. 27

        Rr = A*R*((1+math.sin(gamma)-math.cos(gamma))/( 1+ ( (R*math.cos(gamma)) / (ls*lr00) )) )# eq. 15

        Rnew = Rb+Rc+Rr
        
        error = R-Rnew

        R = Rnew
        if (step > N):
            flag=0
            break
        step=step+1
			
        stopcondition = (abs(error) > maxEps);
	
    if (flag==1):        
        return Rnew
    
    print(f"no convergence in {N} steps, error is {error}")
    return Rnew

# Plot as to reproduce figure 3 an 4 in the paper Balbi 2020
def test_plot():
    anyFuel = {}
    
    anyFuel["Ta"]  = 300 # nomenclature
    anyFuel["Ti"]  = 600 # nomenclature
    anyFuel["Tvap"] = 373 # nomenclature
    anyFuel["Tau0"]  = 75591 # nomenclature
    anyFuel["Deltah"]   = 2.3e6 # nomenclature
    anyFuel["DeltaH"] = 1.74e7 # nomenclature
    anyFuel["Cpv"] = 4180 # nomenclature
    anyFuel["Cpa"] = 1150 # nomenclature
    anyFuel["X0"] = 0.3 # nomenclature
    anyFuel["K1"] = 130 # nomenclature
    anyFuel["st"] = 17 # nomenclature
    anyFuel["r00"] = 2.5e-5 # nomenclature
    anyFuel["B"] = 5.6e-8 # nomenclature
    anyFuel["g"] = 9.81 # nomenclature
    
    
    
    pineNeedle = dict(anyFuel)
    pineNeedle["Sigmad"] = 0.078 #0.05 in table. 2.. but no convergence
    pineNeedle["sd"]  = 6000 #table. 2
    pineNeedle["e"]   = 0.1 #table. 2
    pineNeedle["Md"]  = 0.1 #table. 2 but in ratio as in table 4 
    pineNeedle["Rhod"]  =  500 # in kg/m3 Fuel density pine needle as table. 2
    pineNeedle["RhoA"]  = 1.225 # air density sea level
    pineNeedle["Cpv"]    = 2030 # pine needles top left page 8
    
    pineNeedle["wind"]    = 0
    pineNeedle["slope"]    = 0
        
    pineNeedle2 = dict(pineNeedle)
    pineNeedle2["Sigmad"] = 0.3 #table. 2
    pineNeedle3 = dict(pineNeedle)
    pineNeedle3["Sigmad"] = 0.8 #table. 2
    
    windInput = np.linspace(0, 10, int(10/0.4)+1) 
    fmcInput = np.linspace(0.05, 0.9, int((0.9-0.05)/0.05)+1) 
    
    wros01 = np.ones(np.shape(windInput))
    wros03 = np.ones(np.shape(windInput))
    wros08 = np.ones(np.shape(windInput))
    
    
    fmcW02 = np.ones(np.shape(fmcInput))
    fmcW8 = np.ones(np.shape(fmcInput))
    
    for i,val in enumerate(windInput):
        pineNeedle["wind"]    = val
        pineNeedle2["wind"]    = val
        pineNeedle3["wind"]    = val
        
        wros01[i] =  Balbi2020(pineNeedle)
        wros03[i] =  Balbi2020(pineNeedle2)
        wros08[i] =  Balbi2020(pineNeedle3)
    
    
    pineNeedleW = dict(pineNeedle)
    pineNeedleW2 = dict(pineNeedleW) 
    
    pineNeedleW["wind"]    = 0.2
    pineNeedleW2["wind"]    = 8

    #varying fmc
    pineNeedleW["Sigmad"] = 0.9 #table. 2
    pineNeedleW2["Sigmad"] = 0.9 #table. 2
    
    pineNeedleW["Md"]    = 0
    pineNeedleW2["Md"]    = 0  
    fmc0RosW02 = Balbi2020(pineNeedleW)
    fmc0RosW8 = Balbi2020(pineNeedleW2)
    

    for i,val in enumerate(fmcInput):
        pineNeedleW["Md"]    = val
        pineNeedleW2["Md"]    = val 
        fmcW02[i] =  Balbi2020(pineNeedleW)/fmc0RosW02
        fmcW8[i] =  Balbi2020(pineNeedleW2)/fmc0RosW8
        
     
    fig, (ax1,ax2) = plt.subplots(2, 1, sharey=False)
    ax1.grid(True)
    ax2.grid(True)
    
    line1 = ax1.plot(windInput,wros01, 'bs',markersize=4, label=f'load {pineNeedle["Sigmad"]}')
    line2 = ax1.plot(windInput,wros03,'ro',markersize=4, label=f'load {pineNeedle2["Sigmad"]}')
    line3 = ax1.plot(windInput,wros08, 'gv',markersize=4,label=f'load {pineNeedle3["Sigmad"]}')
    
    line4 = ax2.plot(fmcInput,fmcW02, 'rv',markersize=4 )
    line5 = ax2.plot(fmcInput,fmcW8,'bo',markersize=4 )
  
     
     
    ax1.set_ylabel('ROS')
    
    fig.suptitle('Balbi 2020 - like fig. 3 and 4')
   
    ax2.set_ylabel('ROS')
    
   
    
    ax1.legend()
    plt.show()
    
    
    
    
    
    
    
#test_plot()