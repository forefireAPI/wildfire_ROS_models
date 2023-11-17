#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fuel Model Tables

Description:
This module contains values for parameters as of :
Scott, Joe H. and Robert E. Burgan. "Standard Fire Behavior Fuel Models: A Comprehensive Set for Use with Rothermel's Surface Fire Spread Model." USDA Forest Service. General Technical Report RMRS-GTR-153. 2005

Author: Jean-Baptiste Filippi
Organization: CNRS
License: GPL

"""

 
# 10-hr dead fuel SAV ratio is 109 1/ft, and 100-hr SAV ratio is 30 1/ft. Total fuel particle mineral content is 5.55 percent; effective (silica-free) mineral content is 1.00 percent. Ovendry fuel particle density is 32 lb/ft3.

# values as in table 7 but they differ from the text values
CB2005_t7_csv = """CODE,1h_tac,10h_tac,100h_tac,Lh_lbac,Lw_lbac,Ftype,SAVd1h_ft-1,SAVd10h_ft-1,SAVd100h_ft-1,depth_ft,Dme_pc,H_BTUlb
GR1,0.10,0.00,0.00,0.30,0.00,dynamic,2200,2000,9999,0.4,15,8000
GR2,0.10,0.00,0.00,1.00,0.00,dynamic,2000,1800,9999,1.0,15,8000
GR3,0.10,0.40,0.00,1.50,0.00,dynamic,1500,1300,9999,2.0,30,8000
GR4,0.25,0.00,0.00,1.90,0.00,dynamic,2000,1800,9999,2.0,15,8000
GR5,0.40,0.00,0.00,2.50,0.00,dynamic,1800,1600,9999,1.5,40,8000
GR6,0.10,0.00,0.00,3.40,0.00,dynamic,2200,2000,9999,1.5,40,9000
GR7,1.00,0.00,0.00,5.40,0.00,dynamic,2000,1800,9999,3.0,15,8000
GR8,0.50,1.00,0.00,7.30,0.00,dynamic,1500,1300,9999,4.0,30,8000
GR9,1.00,1.00,0.00,9.00,0.00,dynamic,1800,1600,9999,5.0,40,8000
GS1,0.20,0.00,0.00,0.50,0.65,dynamic,2000,1800,1800,0.9,15,8000
GS2,0.50,0.50,0.00,0.60,1.00,dynamic,2000,1800,1800,1.5,15,8000
GS3,0.30,0.25,0.00,1.45,1.25,dynamic,1800,1600,1600,1.8,40,8000
GS4,1.90,0.30,0.10,3.40,7.10,dynamic,1800,1600,1600,2.1,40,8000
SH1,0.25,0.25,0.00,0.15,1.30,dynamic,2000,1800,1600,1.0,15,8000
SH2,1.35,2.40,0.75,0.00,3.85,N/A,2000,9999,1600,1.0,15,8000
SH3,0.45,3.00,0.00,0.00,6.20,N/A,1600,9999,1400,2.4,40,8000
SH4,0.85,1.15,0.20,0.00,2.55,N/A,2000,1800,1600,3.0,30,8000
SH5,3.60,2.10,0.00,0.00,2.90,N/A,750,9999,1600,6.0,15,8000
SH6,2.90,1.45,0.00,0.00,1.40,N/A,750,9999,1600,2.0,30,8000
SH7,3.50,5.30,2.20,0.00,3.40,N/A,750,9999,1600,6.0,15,8000
SH8,2.05,3.40,0.85,0.00,4.35,N/A,750,9999,1600,3.0,40,8000
SH9,4.50,2.45,0.00,1.55,7.00,dynamic,750,1800,1500,4.4,40,8000
TU1,0.20,0.90,1.50,0.20,0.90,dynamic,2000,1800,1600,0.6,20,8000
TU2,0.95,1.80,1.25,0.00,0.20,N/A,2000,9999,1600,1.0,30,8000
TU3,1.10,0.15,0.25,0.65,1.10,dynamic,1800,1600,1400,1.3,30,8000
TU4,4.50,0.00,0.00,0.00,2.00,N/A,2300,9999,2000,0.5,12,8000
TU5,4.00,4.00,3.00,0.00,3.00,N/A,1500,9999,750,1.0,25,8000
TL1,1.00,2.20,3.60,0.00,0.00,N/A,2000,9999,9999,0.2,30,8000
TL2,1.40,2.30,2.20,0.00,0.00,N/A,2000,9999,9999,0.2,25,8000
TL3,0.50,2.20,2.80,0.00,0.00,N/A,2000,9999,9999,0.3,20,8000
TL4,0.50,1.50,4.20,0.00,0.00,N/A,2000,9999,9999,0.4,25,8000
TLS,1.15,2.50,4.40,0.00,0.00,N/A,2000,9999,1600,0.6,25,8000
TL6,2.40,1.20,1.20,0.00,0.00,N/A,2000,9999,9999,0.3,25,8000
TL7,0.30,1.40,8.10,0.00,0.00,N/A,2000,9999,9999,0.4,25,8000
TL8,5.80,1.40,1.10,0.00,0.00,N/A,1800,9999,9999,0.3,35,8000
TLO,6.65,3.30,4.15,0.00,0.00,N/A,1800,9999,1600,0.6,35,8000
SB1,1.50,3.00,11.00,0.00,0.00,N/A,2000,9999,9999,1.0,25,8000
SB2,4.50,4.25,4.00,0.00,0.00,N/A,2000,9999,9999,1.0,25,8000
SB3,5.50,2.75,3.00,0.00,0.00,N/A,2000,9999,9999,1.2,25,8000
SB4,5.25,3.50,5.25,0.00,0.00,N/A,2000,9999,9999,2.7,25,8000 """


def csv_string_to_dict(csv_str):
    # Split the string into lines and remove empty lines
    lines = [line for line in csv_str.strip().split('\n') if line]
    # Extract the header (first line) and split by comma
    header = lines[0].split(',')
    # Create a dictionary to hold the data
    fuel_dict = {}
    # Iterate over the remaining lines
    for line in lines[1:]:
        # Split each line by comma
        values = line.split(',')
        # The first value is the key (CODE)
        key = values[0]
        # The remaining values are the values, convert to float when possible
        values_dict = {header[i]: float(val) if val.replace('.', '', 1).isdigit() else val for i, val in enumerate(values[1:], 1)}
        # Assign the dictionary of values to the key in the main dictionary
        fuel_dict[key] = values_dict
    return fuel_dict


def convert_units_imperial_to_metric(data_dict):
    """
    Convert the units in the dictionary's keys from imperial to metric,
    changing the variable names as well.

    Parameters:
    - data_dict (dict): A dictionary with keys indicating imperial units.

    Returns:
    - dict: A dictionary with units converted to metric, and updated keys.
    """
    # Define conversion factors
    pounds_to_kilograms = 0.453592
    feet_to_meters = 0.3048
    btu_to_joules = 1055.06
    tons_per_acre_to_kg_per_hectare = 2241.7

    # Dictionary to hold the converted data
    metric_dict = {}

    for code, values in data_dict.items():
        # Initialize a new dictionary for this code
        metric_dict[code] = {}
        
        for key, value in values.items():
            # Check the unit in the key and convert the value accordingly
            if key.endswith("lb_ac"):
                # Convert from pounds per acre to kilograms per hectare
                new_key = key.replace("lb_ac", "kg_ha")
                metric_dict[code][new_key] = float(value) * pounds_to_kilograms * 2.47105 if value.replace('.', '', 1).isdigit() else value
            
            elif key.endswith("t_ac"):
                # Convert from tons per acre to kilograms per hectare
                new_key = key.replace("t_ac", "kg_ha")
                metric_dict[code][new_key] = float(value) * tons_per_acre_to_kg_per_hectare if value.replace('.', '', 1).isdigit() else value

            elif key.endswith("ft"):
                # Convert from feet to meters
                new_key = key.replace("ft", "m")
                metric_dict[code][new_key] = float(value) * feet_to_meters if value.replace('.', '', 1).isdigit() else value
            
            elif key.endswith("BTU_lb"):
                # Convert from BTU per pound to Joules per kilogram
                new_key = key.replace("BTU_lb", "J_kg")
                metric_dict[code][new_key] = float(value) * btu_to_joules / pounds_to_kilograms if value.replace('.', '', 1).isdigit() else value
            
            else:
                # No conversion needed, keep the key as is
                metric_dict[code][key] = value

    return metric_dict


def to_latex_table(data_dict):
    """
    Generate a LaTeX table from a fuel dictionary.
    
    Parameters:
    - data_dict (dict): A dictionary with the fuel data.
    
    Returns:
    - str: A string containing the LaTeX code for the table.
    """
    # Start the LaTeX table code with the longtable environment
    first_row_values = next(iter(data_dict.values()))
    num_columns = len(first_row_values) + 1  # Additional column for the code
    latex_table = "\\begin{longtable}{|" + "l|" + "c|" * (num_columns - 1) + "}\n\\hline\n"

    # Generate column headers from the keys of the first item in the dictionary and escape underscores for LaTeX
    headers = first_row_values.keys()
    escaped_headers = ["Code"] + [key.replace('_', ' ') for key in headers]
    latex_table += " & ".join(escaped_headers) + " \\\\\n\\hline\n\\endfirsthead\n\\hline\n"

    # Add the data rows
    for code, values in data_dict.items():
        row_data = [str(values[key]) for key in headers]
        escaped_row_data = [data.replace('_', '\\_') for data in row_data]
        latex_table += code + " & " + " & ".join(escaped_row_data) + " \\\\\n\\hline\n"

    # End the LaTeX table code
    latex_table += "\\end{longtable}"

    return latex_table

def to_latex_file(table_dict, latex_file_name):
    """
    Create a complete LaTeX document that can be compiled directly, containing the given table.

    Parameters:
    - table_dict (str):  A dictionary with the fuel data.
    - latex_file_name (str) : File path of latex output file

    Returns:
    - Nothing
    """
    # LaTeX document structure
    
    latex_document = (
        "\\documentclass{article}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage{longtable}\n"
        "\\usepackage{lscape}\n"  # Package for landscape orientation
        "\\begin{document}\n"
        "\\begin{landscape}\n"
        "\\tiny\n"  # Set the font size to small
        + to_latex_table(table_dict) +
        "\n\\end{landscape}\n"
        "\\end{document}"
    )
 
    
    with open(latex_file_name, 'w') as file:
        file.write(latex_document)

def testModel():
    return  """
    Table 3—Dead fuel moisture content values (percent) for the dead fuel moisture scenarios.
    D1 D2 D3 D4
    Very low Low Moderate High
    1-hr 3 6 9 12 10-hr 4 7 10 13 100-hr 5 8 11 14

    L1 L2 L3 L4
    Fully cured
    Very low
    Live herbaceous 30 Live woody 60
    Two-thirds cured
    Low
    60 90
    One-third cured
    Moderate
    90 120
    Fully green (uncured)
    High
    120 150
      """  
#SB2005 = csv_string_to_dict(CB2005_t7_csv)
#to_latex_file(SB2005, "SB2005.tex")

