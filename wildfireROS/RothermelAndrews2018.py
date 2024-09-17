#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wildfire ROS Model - Rothermel 

Description:
This module contains the implementation of the Balbi 2020 for predicting the Rate of Spread (ROS) of wildfires.
It is based on  https://www.fs.fed.us/rm/pubs_series/rmrs/gtr/rmrs_gtr371.pdf   
Rothermel, Richard C. 1972. A mathematical model for predicting fire spread in wildland fuels. Res. Pap. INT-115. Ogden, UT: U.S. Department of Agriculture, Intermountain Forest and Range Experiment Station- https://www.fs.usda.gov/treesearch/pubs/32533

equation set from :
Andrews, Patricia L. 2018. The Rothermel surface fire spread model and associated developments: A comprehensive explanation. Gen. Tech. Rep. RMRS-GTR-371. Fort Collins, CO: U.S. Department of Agriculture, Forest Service, Rocky Mountain Research Station


Author: Jean-Baptiste Filippi
Organization: CNRS
License: GPL

sources inspired from http://www.prairieprojectknowledgehub.org/books/fire/page/rothermels-simple-fire-model

Usage:
from models.[model_file_name] import [ModelClassName]

"""
import math
import numpy as np
import matplotlib.pyplot as plt

from .model_set import *

def Rothermel1972_valuesset():
    return {"identification":{'CODE': 'A4'},
            "typical": {'H': 18608.0,'SAVcar': 5705.380577427821, 'fd': 1.8, 'fuelDens': 512.592,'Dme': 0.2},
            "fuelstate": {'fl1h': 0.4},
            "environment":  {'wind':10,'slope':0,'mdOnDry1h':0.06},
            "model": {'totMineral': 0.0555, 'effectMineral': 0.01},
            "constants": {}
            }


def Rothermel1972(Z, print_calculus = False):
  
    
    sa_vol_ratio = Z.SAVcar_ftinv   # Fuel Particle surface area to volume ratio (1/ft)
    fuel_load = Z.fl1h_lbft2 # Ovendry fuel loading 
    bed_depth = Z.fd_ft # Fuel depth (ft)
    dead_extinction_moisture = Z.Dme_r  # Moisture content of extinction
    moisture_content = Z.mdOnDry1h_r   # Fuel particle moisture content
    wind = Z.wind_ftmin # wind velocity at mid flame
    slope  = math.radians(Z.slope_deg) # slope angle 
    heat_content = Z.H_BTUlb  # Fuel particle low heat content
    mineral_content = Z.totMineral_r  # Fuel Particle effective mineral content
    effective_mineral_content= Z.effectMineral_r  # Fuel Particle effective mineral content
    particle_density = Z.fuelDens_lbft3  # Ovendry particle density


    tan_slope = math.tan(slope) #  in radians
    preignition = 250 + 1116 * moisture_content

    heating_number = np.exp(-138 / sa_vol_ratio)

    bulk_density = fuel_load / bed_depth
    packing_ratio = bulk_density / particle_density
    optimal_packing = 3.348 * sa_vol_ratio ** -.8189

    slope_factor = 5.275 * packing_ratio ** -.3 * tan_slope**2

    C = 7.74 * np.exp(-.133 * sa_vol_ratio**.55)
    B = .02526 * sa_vol_ratio ** .54
    E = .715 * np.exp(sa_vol_ratio * -3.59e-4)
    wind_factor = C * wind**B * (packing_ratio / optimal_packing) ** E

    propagating_flux = (192 +.2595 * sa_vol_ratio) **-1 * np.exp((.792 + .681 * sa_vol_ratio ** .5) * (packing_ratio + .1))

    mineral_dampening = min(1.0, .174 * effective_mineral_content**-.19)

    rm = min(1.0, moisture_content / dead_extinction_moisture)
    moisture_dampening = 1 - 2.59 * rm + 5.11 * rm**2 - 3.52 * rm**3

    net_fuel_load = fuel_load * (1 - mineral_content)

    max_reaction = sa_vol_ratio ** 1.5 * (495 + .0594 * sa_vol_ratio**1.5)**-1

    A = 133 * sa_vol_ratio ** -.7913

    optimal_reaction = max_reaction * (packing_ratio / optimal_packing) ** A * np.exp(A * (1 - packing_ratio / optimal_packing))

    reaction_intensity = optimal_reaction * net_fuel_load * heat_content * moisture_dampening * mineral_dampening

    rate_of_spread = reaction_intensity * propagating_flux * (1 + wind_factor + slope_factor) / (bulk_density * heating_number * preignition)

    return {"ROS_ftmin":rate_of_spread, "PR_r":propagating_flux, "FI_BTUftmin":reaction_intensity}


def RothermelAndrews2018_valuesset():
    return {"identification":{'CODE': 'A4'},
            "typical": {'H': 18608.0,'SAVcar': 5705.380577427821, 'fd': 1.8, 'fuelDens': 512.592,'Dme_pc': 20,'bulkDens': 1.9222199999999998, 'packRatio': 0.52},
            "fuelstate": {'fl1h_tac': 0.4},
            "environment":  {'wind':10,'slope':0,'mdOnDry1h':0.06},
            "model": {'totMineral': 0.0555, 'effectMineral': 0.01},
            "constants": {}
            }


def RothermelAndrews2018(Z, print_calculus = False):
    
    # input requirements
    wo = Z.fl1h_lbft2 # Ovendry fuel loading 
    fd = Z.fd_ft # Fuel depth (ft)
    wv = Z.wind_ftmin   # Wind velocity at midflame height (ft/minute) 
    fpsa = Z.SAVcar_ftinv   # Fuel Particle surface area to volume ratio (1/ft)
    mf = Z.mdOnDry1h_r   # Fuel particle moisture content
    h = Z.H_BTUlb  # Fuel particle low heat content
    pp = Z.fuelDens_lbft3  # Ovendry particle density
    st = Z.totMineral_r  # Fuel particle mineral content
    se = Z.effectMineral_r  # Fuel Particle effective mineral content
    mois_ext = Z.Dme_r  # Moisture content of extinction
    wind = Z.wind_ftmin # wind velocity at mid flame
    slope_rad = math.radians(Z.slope_deg) # slope angle 
    
    
    if(print_calculus):
        print("Rothermel model such as Andrews and Rothermel 2017")
        print(f"Ovendry Fuel Loading (wo): {Z.fl1h_lbft2} lb/ft²")
        print(f"Fuel Depth (fd): {Z.fd_ft} ft")
        print(f"Wind Velocity at Midflame Height (wv): {Z.wind_ftmin} ft/min")
        print(f"Fuel Particle Surface Area to Volume Ratio (fpsa): {Z.SAVcar_ftinv} 1/ft")
        print(f"Fuel Particle Moisture Content (mf): {Z.mdOnDry1h_r} ratio")
        print(f"Fuel Particle Low Heat Content (h): {Z.H_BTUlb} BTU/lb")
        print(f"Ovendry Particle Density (pp): {Z.fuelDens_lbft3} lb/ft³")
        print(f"Fuel Particle Mineral Content (st): {Z.totMineral_r} ratio")
        print(f"Fuel Particle Effective Mineral Content (se): {Z.effectMineral_r} ratio")
        print(f"Moisture Content of Extinction (mois_ext): {Z.Dme_r} ratio ")
        print(f"Wind Velocity at Mid Flame (wind): {Z.wind_ftmin} ft/min")
        print(f"Slope Angle (slope_rad): {Z.slope_rad} radians")
    
    # Parameters
    maxval= 0
    
    if wo > 0:
                
        tan_slope = math.tan(slope_rad) #  in radians
        # Betas Packing ratio
        Beta_op = 3.348 * math.pow(fpsa, -0.8189)  # Optimum packing ratio
        ODBD = wo / fd  # Ovendry bulk density
        Beta = ODBD / pp #Packing ratio
        #Beta = 0.00158
        Beta_rel = Beta / Beta_op
        # Reaction Intensity
        WN = wo / (1 + st)  # Net fuel loading
        #A = 1 / (4.774 * pow(fpsa, 0.1) - 7.27)  # Unknown const
        A =  133.0 / math.pow(fpsa, 0.7913) #updated A
        T_max = math.pow(fpsa,1.5) * math.pow(495.0 + 0.0594 * math.pow(fpsa, 1.5),-1.0)  # Maximum reaction velocity
        #T_max = (fpsa*math.sqrt(fpsa)) / (495.0 + 0.0594 * fpsa * math.sqrt(fpsa))
        T = T_max * math.pow((Beta / Beta_op),A) * math.exp(A * (1 - Beta / Beta_op))  # Optimum reaction velocity
        # moisture dampning coefficient
        NM = 1. - 2.59 * (mf / mois_ext) + 5.11 * math.pow(mf / mois_ext, 2.) - 3.52 * math.pow(mf / mois_ext,3.)  # Moisture damping coeff.
        # mineral dampning
        NS = 0.174 * math.pow(se, -0.19)  # Mineral damping coefficient
        #print(T, WN, h, NM, NS)
        RI = T * WN * h * NM * NS
        #RI = 874
        # Propogating flux ratio
        PFR = math.pow(192.0 + 0.2595 * fpsa, -1) * math.exp(
            (0.792 + 0.681 * fpsa ** 0.5) * (Beta + 0.1))  # Propogating flux ratio
        ## Wind Coefficient
        B = 0.02526 * math.pow(fpsa, 0.54)
        C = 7.47 * math.exp(-0.1333 * math.pow(fpsa, 0.55))
        E = 0.715 * math.exp(-3.59 * 10**-4 * fpsa)
        #WC = C * wv**B * math.pow(Beta / Beta_op, -E) #wind coefficient
        if wv > (0.9 * RI): #important - don't know source. Matches BEHAVE
            wv = 0.9 * RI
        WC = (C * wv ** B) * math.pow((Beta / Beta_op), (-E))
        #WC= WC*0.74
        #Slope  coefficient
        SC = 5.275*(Beta**-0.3)*tan_slope**2
        #Heat sink

        EHN = math.exp(-138. / fpsa)  # Effective Heating Number = f(surface are volume ratio)
        QIG = 250. + 1116. * mf  # Heat of preignition= f(moisture content)
        # rate of spread (ft per minute)
        #RI = BTU/ft^2
        numerator = (RI * PFR * (1 + WC + SC))
        denominator = (ODBD * EHN * QIG)
        R = numerator / denominator #WC and SC will be zero at slope = wind = 0
        RT = 384.0/fpsa
        HA = RI*RT
        #fireline intensity as described by Albini via USDA Forest Service RMRS-GTR-371. 2018
        FI = (384.0/fpsa)*RI*(R) ##Uses Reaction Intensity in BTU / ft/ min
        #FI = HA*R
        if (RI <= 0):
            return {"ROS_ftmin":0, "PR_r":0, "FI_BTUftmin":0}
        return {"ROS_ftmin":R, "PR_r":RI, "FI_BTUftmin":FI}
    else:
        return {"ROS_ftmin":0, "PR_r":0, "FI_BTUftmin":0}


