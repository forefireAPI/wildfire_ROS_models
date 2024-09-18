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
import numpy as np

   
var_properties = {
    "CODE": {"long_name": "Shortname - code", "range": None, "SI_unit": None},
    "INDEX": {"long_name": "Integer used as classification number", "range": None, "SI_unit": None},
    
    # Fuel Characteristic Parameters - do not vary in time
    "ftype": {"long_name": "S for static, D for dynamic, N for Non applicable", "range": None, "SI_unit": None},
    "SAV1h": {"long_name": "Surface-area-to-volume ratio for 1h fuel", "range": [5000.0, 7000.0], "SI_unit": "minv"},
    "SAV10h": {"long_name": "Surface-area-to-volume ratio for 10h fuel", "range": [4000.0, 6000.0], "SI_unit": "minv"},
    "SAV100h": {"long_name": "Surface-area-to-volume ratio for 100h fuel", "range": [4000.0, 6000.0], "SI_unit": "minv"},
    "SAVLDherb": {"long_name": "Surface-area-to-volume ratio for live and dead herbaceous", "range": [4000.0, 6000.0], "SI_unit": "minv"},
    "SAVLwood": {"long_name": "Surface-area-to-volume ratio for live woody", "range": [4000.0, 6000.0], "SI_unit": "minv"},
    "SAVcar_ftinv": {"long_name": "Characteristic SAV", "range": [1000.0, 1700.0], "SI_unit": "minv"},
    "fd_ft": {"long_name": "Fuel bed depth", "range": [0.5, 6.0], "SI_unit": "m"},
    "H": {"long_name": "Heat content", "range": [15000.0, 20000.0], "SI_unit": "kJkg"},
    "bulkDens": {"long_name": "Bulk density", "range": [0.5, 16.0], "SI_unit": "kgm3"},
    "packRatio": {"long_name": "Relative packing ratio", "range": [0.001,0.05], "SI_unit": "r"},
    "fuelDens": {"long_name": "Ovendry fuel particle density", "range": [400.0, 600.0], "SI_unit": "kgm3"},
    'Tau0': {"long_name": "Flame residence time", "range": [60000, 80000], "SI_unit": "spm"},
    
    # Fuel State parameter - vary in time
    "fl1h_tac": {"long_name": "Ovendry 1h fuel load", "range": [0.1, 5], "SI_unit": None},
    "fl10h": {"long_name": "Ovendry 10h fuel load", "range": [0.1, 5], "SI_unit": None},
    "fl100h": {"long_name": "Ovendry 100h fuel load", "range": [0.1, 5], "SI_unit": None},
    "flLherb": {"long_name": "Live herbaceous load", "range": [0.1, 5], "SI_unit": None},
    "flLwood": {"long_name": "Live woody load", "range": [0.1, 5], "SI_unit": None},
    "Dme_pc": {"long_name": "Dead fuel moisture of extinction", "range": [10, 50], "SI_unit": None},
    'Cpf': {"long_name": "Specific heat of fuel", "range": [1500, 2500], "SI_unit": None},
    "mdOnDry1h_r": {"long_name": "1 hour fuel moisture expressed as ratio on dry mass basis", "range": [0.0, 0.4], "SI_unit": None},
    "mdOnDry10h": {"long_name": "10 hour fuel moisture expressed as ratio on dry mass basis", "range": [0.0, 1], "SI_unit": None},
    "mdOnDry100h": {"long_name": "100 hour fuel moisture expressed as ratio on dry mass basis", "range": [0.0, 1], "SI_unit": None},
    "mdOnTotal1h": {"long_name": "1 hour fuel moisture expressed as ratio on total mass basis", "range": [0.0, 1], "SI_unit": None},
    "mdOnTotal10h": {"long_name": "10 hour fuel moisture expressed as ratio on total mass basis", "range": [0.0, 1], "SI_unit": None},
    "mdOnTotal100h": {"long_name": "100 hour fuel moisture expressed as ratio on total mass basis", "range": [0.0, 1], "SI_unit": None},
    "mdOnDryLHerb": {"long_name": "Live herbaceous fuel moisture expressed as ratio on total mass basis", "range": [0.0, 1], "SI_unit": None},
    "mdOnDryLWood": {"long_name": "Live woody fuel moisture expressed as ratio on total mass basis", "range": [0.0, 1], "SI_unit": None},
 
    # Environment parameters
    "wind": {"long_name": "Wind speed at midflame height", "range": [0, 10], "SI_unit": None},
    "slope_tan": {"long_name": "Slope angle", "range": [-1.7, 1.7], "SI_unit": None},
    'Ta': {"long_name": "Ambient temperature", "range": [280.0, 310.0], "SI_unit": None},
    'airDens': {"long_name": "Air density", "range": [0.825, 1.225], "SI_unit": None},

    
    # Model Parameters
    "totMineral_r": {"long_name": "Total fuel particle mineral relative content", "range": None, "SI_unit": None},
    "effectMineral_r": {"long_name": "Effective (silica-free) mineral relative content", "range": None, "SI_unit": None},
    'Ti': {"long_name": "Ignition temperature", "range": None, "SI_unit": None},
    'Tvap': {"long_name": "Vaporisation temperature", "range": None, "SI_unit": None},
    'hEvap': {"long_name": "Heat of latent evaporation", "range": None, "SI_unit": None},
    'Cpa': {"long_name": "Specific heat of air", "range": None, "SI_unit": None},
    'X0': {"long_name": "Radiative factor", "range": None, "SI_unit": None},
    'K1': {"long_name": "Drag coefficient", "range": None, "SI_unit": None},
    'st': {"long_name": "Air–pyrolysis gas mass ratio in the flame body", "range": None, "SI_unit": None},
    'r00': {"long_name": "Model coefficient", "range": None, "SI_unit": None},
    
    # Constants
    'B': {"long_name": "Stefan–Boltzmann constant", "range": None, "SI_unit": None},
    'g': {"long_name": "Acceleration due to gravity", "range": None, "SI_unit": None},
    
    ## Output Parameters
    "ROS": {"long_name": "Rate of Spread", "range": None, "SI_unit": "mps"},
    "FllH": {"long_name": "Flame height", "range": None, "SI_unit": "m"},
    "PR": {"long_name": "Propagating flux", "range": None, "SI_unit": None},
    "FI": {"long_name": "Reaction intensity", "range": None, "SI_unit": None}    
}

unit_representation = {
    'ft': 'ft',
    'ftinv': 'ft⁻¹',
    'ft2': 'ft²',
    'ft3': 'ft³',
    'lb': 'lb',
    'miph': 'mi/h',
    'ftmin': 'ft/min',
    'lbft3': 'lb/ft³',
    'lbft2': 'lb/ft²',
    'tac': 't/ac',
    'pc': '%',
    'BTUlb': 'BTU/lb',
    'BTUftmin': 'BTU/ft²/min',
    'kJms': 'kJ/m²/s',
    'deg': '°',
    'rad': 'rad',
    'tan': 'ratio',
    'degK': 'K',
    'm': 'm',
    'r': 'ratio',
    'minv': 'm⁻¹',
    'kg': 'kg',
    'kJkg': 'kJ/kg',
    'Jkg': 'J/kg',
    'mps': 'm/s',
    'spm': 's/m',
    'JkgK': 'J/kg·K',
    'kgm3': 'kg/m³',
    'kgm2': 'kg/m²',
    'm2': 'm²',
    'm3': 'm³'
}
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
    'degK': 1,            # temperature in Kelvin
    'm': 1,                 # meters 
    'r': 1,               # ratio
    'minv': 1,               # meters^-1 dimentionless surface area ration in m2/m3
    'kg': 1,               # kilogram
    'kJkg' : 1,           # kiloJoule per kilogram
    'Jkg' : 0.001,           # Joule per kilogram
    'mps': 1,               # meters per seconds
    'spm': 1,               # seconds per meter
    'JkgK': 1,
    'kgm3': 1,               # kg per cubic meters
    'kgm2': 1,               # kg per square meters
    'm2': 1,             # square meters to square meters (no conversion needed)
    'm3': 1             # cubic meters to cubic meters (no conversion needed)
}           


class model_parameters:
    """
    A class to handle and convert measurement units in model parameter data.
    Stores values in the metric system and allows for dynamic conversion and assignment.
    It is loose and do not check for coherence, you can actually (but you should not) convert meters into lb...
    
    Unit shortnames :
    
    Provided Units:
    - ftinv    : Surface to Volume ratio (ft^2/ft^3)
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
    - minv     : Surface to Volume ratio (m^2/m^3) 
    - m       : Length (meters)
    - kg      : Weight (kilograms)
    - kgm3   : Density (kilograms per cubic meter)
    - kgm2   : Load (kilograms per square meter)
    - mps     : Speed (meters per second)
    - mpm     : Speed (meters per minute)
    - r       : Ratio (dimensionless)
    - deg     : Angle (degrees, same in metric)
    - kJkg    : Heat content  Kj per kg
    
    Note: For units like 'r', and 'deg', no direct metric equivalent is needed as they are dimensionless or have the same representation in the metric system. 
    The 'pc' unit is also dimensionless and is handled as ratio in both systems.
    """
        
      
    def __init__(self, params=None):
        # Conversion factors
        self.to_metric = {unit: lambda x, factor=factor: np.multiply(x, factor) for unit, factor in convert_metric.items()}
        self.from_metric = {unit: lambda x, factor=factor: np.divide(x, factor) for unit, factor in convert_metric.items()}
        self.to_metric['tan'] = lambda x: math.atan(x) * 180 / math.pi
      
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
    def __repr__(self):
        """
        Returns a string representation of the object for lists and other collections.
        """
        return self.__str__()  # or format this string as you wish
    
    def __add__(self, other):
        """
        Adds two model_parameters instances, giving priority to the parameters in the first instance.
        Emits a warning if a parameter is redefined.
        """
        if not isinstance(other, model_parameters):
            raise TypeError(f"Cannot add 'model_parameters' with '{type(other)}'")
    
        result = model_parameters()
        # Add all parameters from the first instance (self)
        for key, value in self.metric_params.items():
            result.metric_params[key] = value
    
        # Add parameters from the second instance (other), with a warning if already defined
        for key, value in other.metric_params.items():
            if key in result.metric_params:
                print(f"Parameter '{key}' redefined. Keeping the first value.")
            else:
                result.metric_params[key] = value
    
        return result
    
    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)
    
    def __delitem__(self, key):
        del self.metric_params[key]
    
    def __iter__(self):
        return iter(self.metric_params)
    
    def __len__(self):
        return len(self.metric_params)
    
    def keys(self):
        return self.metric_params.keys()
    
    def values(self):
        return self.metric_params.values()
    
    def items(self):
        return self.metric_params.items()

    
    
    def get_set(self):
        return self.metric_params
    
    def load(self, params):
        if params is not None:
            for key, value in params.items():
                self.__setattr__(key, value)  
                
    def str_full_name(attr):
        param_name = ""
        unit = ""
        res = attr
        if '_' in attr:
            param_name, unit = attr.split('_', 1)
            
        if param_name in var_properties:
            res =  var_properties[param_name]["long_name"]
    
        if unit in unit_representation:
            res = res + " in "  + unit_representation[unit]
    
        return res
                
            

def test():

    A4 = {'load_tac': 5, 'weight_lb': 100, 'speed_pc': 10  , 'tata_ftinv' : 10}
    a4_params = model_parameters(A4)
   
    print("load", a4_params.load_lbft2, a4_params.load_kgm2, a4_params.load_tac)
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

    