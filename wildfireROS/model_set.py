#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model parameter set

Description:
This module contains a clas to handle parameters in various unit systems

Author: Jean-Baptiste Filippi
Organization: CNRS
License: GPL

"""
import math
class model_parameters:
    """
    A class to handle and convert measurement units in model parameter data.
    Stores values in the metric system and allows for dynamic conversion and assignment.
    It is loose and do not check for coherence, you can actually (but you should not) convert meters into lb...
    
    Unit shortnames :
    
    Provided Units:
    - ftft2    : Surface to Volume ratio (ft^2/ft^3)
    - ft      : Length (feet)
    - lb      : Weight (pounds)
    - tac     : Load (tons per acre)
    - lbft2   : Pressure or Load per Area (pounds per square feet)
    - lbft3  : Density (pounds per cubic feet)
    - miph     : Speed (miles per hour)
    - ftmin     : Speed (feet per minute)
    - r       : Ratio (dimensionless)
    - pc      : Percentage (ratio * 100)
    - deg     : Angle (degrees)
    - BTUlb    : Heat content BTU per pound
    
    Metric System Equivalents:
    - mm1     : Surface to Volume ratio (m^2/m^3) 
    - m       : Length (meters)
    - kg      : Weight (kilograms)
    - kgm3   : Density (kilograms per cubic meter)
    - kgm2   : Load (kilograms per square meter)
    - mps     : Speed (meters per second)
    - mpm     : Speed (meters per minute)
    - r       : Ratio (dimensionless)
    - deg     : Angle (degrees, same in metric)
    - rad     : Angle (radian, same in metric)
    - kJkg    : Heat content  Kj per kg
    
    Note: For units like 'r', and 'deg', no direct metric equivalent is needed as they are dimensionless or have the same representation in the metric system. 
    The 'pc' unit is also dimensionless and is handled as ratio in both systems.
    """
 
    def __init__(self, params=None):
        # Conversion factors
        convert_metric = {
            'ft': 0.3048,          # feet to meters
            'ftinv': 1/0.3048,        # feet^-1 dimentionless surface area ratio of ft2/ft3 to m2/m3       
            'ft2': 0.3048 ** 2,  # square feet to square meters
            'ft3': 0.3048 ** 3,  # cubic feet to cubic meters
            'lb': 0.453592,       # pounds to kilograms
            'miph': 0.44704,      # miles per hour to meters per second
            'ftmin': 0.3048 / 60,  # feet per minute to meters per second
            'lbft3': 16.0185,   # pounds per cubic foot to kilograms per cubic meter
            'lbft2': 4.88243,   # pounds per square foot to kilograms per square meter
            'tac': 0.224,      # US short tons per acre to kilograms per square meter
            'pc': 0.01,            # percentage to ratio
            'BTUlb' : 2.326,      # energy density BTU/lb to kJ/kg.
            'BTUftmin' : 0.189,         #  BTU/ft²/min  to  kJ/m²/s, 
            'kJms' : 1,
            'deg': 1,                 # degrees angle 
            'rad': math.pi / 180 ,     # radians angle 
            'degC': 1,            # temperature degrees
            'm': 1,                 # meters 
            'r': 1,               # ratio
            'minv': 1,               # meters^-1 dimentionless surface area ration in m2/m3
            'kg': 1,               # kilogram
            'kJkg' : 1,           # kiloJoule per kilogram
            'mps': 1,               # meters per seconds
            'kgm3': 1,               # kg per cubic meters
            'kgm2': 1,               # kg per square meters
            'm2': 1,             # square meters to square meters (no conversion needed)
            'm3': 1             # cubic meters to cubic meters (no conversion needed)
        }                   
        
        self.to_metric = {unit: lambda x, factor=factor: x * factor for unit, factor in convert_metric.items()}
        self.from_metric = {unit: lambda x, factor=factor: x / factor for unit, factor in convert_metric.items()}
        self.metric_params = {}
        self.load(params)

 
    def __getattr__(self, attr):
        """
        Provides dynamic access to parameters, converting them from metric units to requested units.
        """
        if '_' in attr:
            param_name, unit = attr.split('_', 1)
            if param_name in self.metric_params:
                if unit in self.from_metric:
                    return self.from_metric[unit](self.metric_params[param_name])
                else:
                    raise AttributeError(f"Conversion to '{unit}' not supported.")
            else:
                raise AttributeError(f"Parameter '{param_name}' not found.")
        else:
            if attr in self.metric_params:
                return self.metric_params[attr]
            else:
                raise AttributeError(f"Attribute '{attr}' not found.")
                
    def __setattr__(self, attr, value):
        """
        Allows setting parameter values, converting them to metric units as necessary.
        """
        if attr in ['metric_params', 'to_metric', 'from_metric'] or attr.startswith('_'):
            # Directly set internal attributes
            object.__setattr__(self, attr, value)
        else:
            param_name, unit = attr.split('_', 1) if '_' in attr else (attr, None)
            if unit:
                if unit in self.to_metric:
                    metric_value = self.to_metric[unit](value)
                    self.metric_params[param_name] = metric_value
                else:
                    raise AttributeError(f"Conversion from '{unit}' not supported.")
            else:
                # If no unit is specified, assume it's already in metric
                self.metric_params[param_name] = value

    def __str__(self):
        """
        Returns a string representation of the metric parameters in dictionary format.
        """
        return str(self.metric_params)

    def get_set(self):
        return self.metric_params
    
    def load(self, params):
        if params is not None:
            for key, value in params.items():
                self.__setattr__(key, value)  

def test():

    A4 = {'load_tac': 5, 'weight_lb': 100, 'speed_pc': 10  , 'tata_ftinv' : 10}

    a4_params = model_parameters(A4)
   
    a4_params.ma = 5
    a4_params.mb = 50
    
    a4_params.ia_ft3 = a4_params.ma_ft3
    a4_params.ib_ft2 = a4_params.mb_ft2
    
    a4_params.pc_minv = a4_params.mb_m2/a4_params.ma_m3
    a4_params.ic_ftinv = a4_params.ib_ft2/a4_params.ia_ft3

    
    # Accessing values in different units
    print("testing ratios",a4_params.pc_minv,a4_params.ic_minv) 
    print("testing ratios",a4_params.pc_ftinv,a4_params.ic_ftinv) 
    print("load", a4_params.load_lbft2, a4_params.load_kgm2, a4_params.load_tac)

    