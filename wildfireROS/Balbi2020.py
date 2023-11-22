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

 
from .model_set import *
def Balbi2020(Z, print_calculus = False):
    # Constants
 
    PI = math.pi

    lh =  Z.fd_m
    lrhov = Z.fuelDens_kgm3
    lm = Z.mdOnDry1h_r
    ls = Z.SAV1h_minv
    lsigma = Z.fl1h_kgm2
    lrhoa = Z.airDens_kgm3
    lCp = Z.Cpf_JkgK
    lTa = Z.Ta_degK
    lTi = Z.Ti_degK
    lDeltah = Z.hEvap_Jkg
    lDeltaH = Z.H_Jkg
    lr00 = Z.r00
    ltau0 = Z.Tau0_spm
    Tvap = Z.Tvap_degK
    Cpa =  Z.Cpa_JkgK
    K1 = Z.K1_spm
    st = Z.st_r
    B = Z.B
    lg = Z.g
    lChi0 = Z.X0
    
    if lh <= 0:
        return 0
    
    lU = 0
    RU = Z.wind_mps
    if RU > 0:
        lU = RU

    lalpha = math.atan(Z.slope_rad)

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
	
    if (flag != 1):    
        print(f"no convergence in {N} steps for Balbi, error is {error}, returning ROS")
        
    return {"ROS_mps":Rnew, "FllH_m":H}

    
    