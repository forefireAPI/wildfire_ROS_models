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

def rothev2(valueOf):
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
    
    
    
    sa_vol_ratio, 
    fuel_load, 
    bed_depth, 
    dead_extinction_moisture, 
    moisture_content, 
    wind, 
    tan_slope,
    heat_content = 8000, 
    mineral_content = .0555,
    effective_mineral_content = .010, 
    particle_density = 32

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

    propegating_flux = (192 +.2595 * sa_vol_ratio) **-1 * np.exp((.792 + .681 * sa_vol_ratio ** .5) * (packing_ratio + .1))

    mineral_dampening = min(1.0, .174 * effective_mineral_content**-.19)

    rm = min(1.0, moisture_content / dead_extinction_moisture)
    moisture_dampening = 1 - 2.59 * rm + 5.11 * rm**2 - 3.52 * rm**3

    net_fuel_load = fuel_load * (1 - mineral_content)

    max_reaction = sa_vol_ratio ** 1.5 * (495 + .0594 * sa_vol_ratio**1.5)**-1

    A = 133 * sa_vol_ratio ** -.7913

    optimal_reaction = max_reaction * (packing_ratio / optimal_packing) ** A * np.exp(A * (1 - packing_ratio / optimal_packing))

    reaction_intensity = optimal_reaction * net_fuel_load * heat_content * moisture_dampening * mineral_dampening

    rate_of_spread = reaction_intensity * propegating_flux * (1 + wind_factor + slope_factor) / (bulk_density * heating_number * preignition)

    return rate_of_spread


def RothermelAndrews2018(valueOf,fuelload, fueldepth, windspeed, slope, fuelmoisture, fuelsav):
    # Parameters
    maxval= 0
    if fuelload > 0:
        
        
        anyFuel= {'SAVd10h_ft-1':109,'SAVd100h_ft-1':30, 'H_BTUlb':8000,'p_dens_lbft-3':32, 'tminer':0.0555,  'eminer':0.010}
        F4  = {'CODE': 4, 'SorD': 'S', '1h_tac': 5.0, '10h_tac': 4.0, '100h_tac': 2.0, 'Lh_tac': 0, 'Lw_tbac': 5.0, 'SAVd1h_ft-1': 2, 'SAVldh_ft-1': 0, 'SAVlw_ft-1': '--', 'depth_ft': 1, 'dme_pc': 500, 'SAVcar_ft-1': 6.0, 'bulk_lbft3': 20, 'packratio': 1},
        SH5 = {'CODE': 'SH5', 'SorD': 'S', '1h_tac': 3.6, '10h_tac': 2.1, '100h_tac': 0, 'Lh_tac': 0, 'Lw_tbac': 2.9, 'SAVd1h_ft-1': 750, 'SAVldh_ft-1': '--', 'SAVlw_ft-1': 1, 'depth_ft': 600, 'dme_pc': 6.0, 'SAVcar_ft-1': 15, 'bulk_lbft3': 1, 'packratio': 252},
        SH7 = {'CODE': 'SH7', 'SorD': 'S', '1h_tac': 3.5, '10h_tac': 5.3, '100h_tac': 2.2, 'Lh_tac': 0, 'Lw_tbac': 3.4, 'SAVd1h_ft-1': 750, 'SAVldh_ft-1': 0, 'SAVlw_ft-1': 1, 'depth_ft': 600, 'dme_pc': 6.0, 'SAVcar_ft-1': 15, 'bulk_lbft3': 1.233, 'packratio': 0.11},
        SH9 = {'CODE': 'SH9', 'SorD': 'D', '1h_tac': 4.5, '10h_tac': 2.45, '100h_tac': 0, 'Lh_tac': 1.55, 'Lw_tbac': 7.0, 'SAVd1h_ft-1': 750, 'SAVldh_ft-1': 1, 'SAVlw_ft-1': 800, 'depth_ft': 1, 'dme_pc': 500, 'SAVcar_ft-1': 4.4, 'bulk_lbft3': 40, 'packratio': 1}
        #Figure 9—fuel moisture 1-hr 6 percent, 10-hr 7 percent, 100-hr 8 percent, live herbaceous 60 percent, and live woody 90 percent.
        environment = {'wind_mph':0,'slope_deg':0,'md1h_r':0.06,'md10h_r':0.07,'md100h_r':0.08,'mdlh_r':0.6,'mdlw_r':0.9}
         
        
        
        wo = valueOf["1h_tac"] * 0.0459 # Ovendry fuel loading in (lb/ft^2). data in ton/ac
        fd = valueOf["depth_ft"] # Fuel depth (ft)
        wv = valueOf["wind_mph"] * 88# Wind velocity at midflame height (ft/minute) = 88 * mph
        fpsa = valueOf["SAVcar_ft-1'"]  # Fuel Particle surface area to volume ratio (1/ft)
        mf = valueOf["fuelmoisture_ratio"]  # Fuel particle moisture content
        
        # CODE , 1h_tac, 10h_tac,100h_tac,Lh_lbac,Lw_lbac,Ftype,SAVd1h_ft-1,SAVd10h_ft-1,SAVd100h_ft-1,depth_ft,Dme_pc,H_BTUlb
        
        h = 8000  # Fuel particle low heat content
        pp = 32.  # Ovendry particle density
        st = 0.0555  # Fuel particle mineral content
        se = 0.010  # Fuel Particle effective mineral content
        mois_ext = 0.12  # Moisture content of extinction or 0.3 if dead
        
        #calculate slope as degrees
        slope_rad = math.atan(slope)
        slope_degrees = slope_rad / 0.0174533 #radians
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
            return (maxval, maxval, maxval)
        return (R, RI, FI)
    else:
        return (maxval, maxval, maxval)


# Plot as to reproduce figure 9 in the paper Andrews 2018, fuels as tables page 31-35
def test_plot():
    
     
    anyFuel= {'SAVd10h_ft-1':109,'SAVd100h_ft-1':30, 'H_BTUlb':8000,'p_dens_lbft-3':32, 'tminer':0.0555,  'eminer':0.010}
    F4  = {'CODE': 4, 'SorD': 'S', '1h_tac': 5.0, '10h_tac': 4.0, '100h_tac': 2.0, 'Lh_tac': 0, 'Lw_tbac': 5.0, 'SAVd1h_ft-1': 2, 'SAVldh_ft-1': 0, 'SAVlw_ft-1': '--', 'depth_ft': 1, 'dme_pc': 500, 'SAVcar_ft-1': 6.0, 'bulk_lbft3': 20, 'packratio': 1},
    SH5 = {'CODE': 'SH5', 'SorD': 'S', '1h_tac': 3.6, '10h_tac': 2.1, '100h_tac': 0, 'Lh_tac': 0, 'Lw_tbac': 2.9, 'SAVd1h_ft-1': 750, 'SAVldh_ft-1': '--', 'SAVlw_ft-1': 1, 'depth_ft': 600, 'dme_pc': 6.0, 'SAVcar_ft-1': 15, 'bulk_lbft3': 1, 'packratio': 252},
    SH7 = {'CODE': 'SH7', 'SorD': 'S', '1h_tac': 3.5, '10h_tac': 5.3, '100h_tac': 2.2, 'Lh_tac': 0, 'Lw_tbac': 3.4, 'SAVd1h_ft-1': 750, 'SAVldh_ft-1': 0, 'SAVlw_ft-1': 1, 'depth_ft': 600, 'dme_pc': 6.0, 'SAVcar_ft-1': 15, 'bulk_lbft3': 1.233, 'packratio': 0.11},
    SH9 = {'CODE': 'SH9', 'SorD': 'D', '1h_tac': 4.5, '10h_tac': 2.45, '100h_tac': 0, 'Lh_tac': 1.55, 'Lw_tbac': 7.0, 'SAVd1h_ft-1': 750, 'SAVldh_ft-1': 1, 'SAVlw_ft-1': 800, 'depth_ft': 1, 'dme_pc': 500, 'SAVcar_ft-1': 4.4, 'bulk_lbft3': 40, 'packratio': 1}
    #Figure 9—fuel moisture 1-hr 6 percent, 10-hr 7 percent, 100-hr 8 percent, live herbaceous 60 percent, and live woody 90 percent.
    
    environment = {'wind_mph':0,'slope_deg':0,'md1h_r':0.06,'md10h_r':0.07,'md100h_r':0.08,'mdlh_r':0.6,'mdlw_r':0.9}
     
    windInput = np.linspace(0, 20, 100) 
        
    
    for i,val in enumerate(windInput):
        pineNeedle["wind"]    = val
        pineNeedle2["wind"]    = val
        pineNeedle3["wind"]    = val
        
        wros01[i] =  Balbi2020(pineNeedle)
        wros03[i] =  Balbi2020(pineNeedle2)
        wros08[i] =  Balbi2020(pineNeedle3)
     
        
     
    fig, (ax1) = plt.subplots(1, 1, sharey=True)
    ax1.grid(True)
     
    
    line1 = ax1.plot(windInput,wros01, 'o',markersize=1, label=f'load {pineNeedle["Sigmad"]}')
    line2 = ax1.plot(windInput,wros03,'o',markersize=1, label=f'load {pineNeedle2["Sigmad"]}')
    line3 = ax1.plot(windInput,wros08, 'o',markersize=1,label=f'load {pineNeedle3["Sigmad"]}')
     
     
     
    ax1.set_ylabel('ROS')
    fig.suptitle('Rothermel Andrews 2018 - ROS like fig. 9)
    
    ax1.legend()
    plt.show()
    
test_plot()