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


fuel_properties = {
    "CODE": "shortname - code",
    "INDEX": "integer used as classification number",
    "fl1h": "Ovendry 1h fuel load",
    "fl10h": "Ovendry 10h fuel load",
    "fl100h": "Ovendry 100h fuel load",
    "flLherb": "live herbaceous load",
    "flLwood": "live woody load",
    "ftype": "S for static, D for dynamic, N for Non applicable",
    "SAV1h": "Surface-area-to-volume ratio for 1h fuel",
    "SAV10h": "Surface-area-to-volume ratio for 10h fuel",
    "SAV100h": "Surface-area-to-volume ratio for 100h fuel",
    "SAVLDherb": "Surface-area-to-volume ratio for live and dead herbaceous",
    "SAVLwood": "Surface-area-to-volume ratio for live woody",
    "fd": "fuel bed depth",
    "SAVcar": "Characteristic SAV",
    "Dme": "dead fuel moisture of extinction",
    "H": "Heat content",
    "bulkDens": "bulk density",
    "packRatio": "relative packing ratio",
    "fuelDens": "Ovendry fuel particle density",
    "totMineral": "Total fuel particle mineral relative content",
    "effectMineral": "effective (silica-free) mineral relative content",
    "wind": "wind speed at midflame height",
    "slope": "slope angle",
    "mdOnDry1h": "1 hour fuel moisture expressed as ratio on dry mass basis",
    "mdOnDry10h": "10 hour fuel moisture expressed as ratio on dry mass basis",
    "mdOnDry100h": "100 hour fuel moisture expressed as ratio on dry mass basis",
    "mdOnTotal1h": "1 hour fuel moisture expressed as ratio on total mass basis",
    "mdOnTotal10h": "10 hour fuel moisture expressed as ratio on total mass basis",
    "mdOnTotal100h": "100 hour fuel moisture expressed as ratio on total mass basis",
    "mdOnDryLHerb": "live herbaceous fuel moisture expressed as ratio on total mass basis",
    "mdOnDryLWood": "live woody fuel moisture expressed as ratio on total mass basis",
    ## Parameters for Balbi models
    'Ta' : "Ambient temperature ",
    'Ti'  : "Ignition temperature ",
    'Tvap'  : "Vaporisation temperature",
    'Tau0'  : "Flame residence time parameter ",
    'hEvap'  : "Heat of latent evaporation",
    'Cpf'  : "Specific heat of fuel",
    'Cpa'  : "Specific heat of air ",
    'X0'  : "Radiative factor",
    'K1'  : "Drag coefficient",
    'st'  : "Air–pyrolysis gas mass ratio in the flame body",
    'r00'  : "Model coefficient",
    'B'  : "Stefan–Boltzmann constant",
    'g'  : "Acceleration due to gravity", 
    'airDens'  : "Air density ",
    
    ## Output Parameters
    "ROS"  :"Rate of Spread", 
    "FllH" :"Flame height", 
    "PR"   :"propagating flux", 
    "FI"   :"reaction_intensity"
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
    'rad': math.pi / 180 ,     # radians angle 
    'degK': 1,            # temperature in Kelvin
    'm': 1,                 # meters 
    'r': 1,               # ratio
    'minv': 1,               # meters^-1 dimentionless surface area ration in m2/m3
    'kg': 1,               # kilogram
    'kJkg' : 1,           # kiloJoule per kilogram
    'Jkg' : 1000,           # Joule per kilogram
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
                warnings.warn(f"Parameter '{key}' redefined. Keeping the first value.")
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
            
        if param_name in fuel_properties:
            res =  fuel_properties[param_name]
    
        if unit in unit_representation:
            res = res + " in "  + unit_representation[unit]
    
        return res
                
            

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

    