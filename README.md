# Wildfire ROS Models Library

## Overview
This Python package provides a comprehensive library of models for simulating the Rate of Spread (ROS) of wildfires. Based on ROS models publications, this library serves as a  tool for researchers and practitioners in the field of wildfire management and simulation in order to help intercompare formulations. 

## Installation
```bash
pip install wildfire_ros_models
```

## Usage
To use this library, import the desired model from the `models` directory and provide the necessary parameters as per the model's documentation. Example usage can be found in the `test` directory.

## Directories

### `cases`
Contains various case studies and scenarios that demonstrate the application of the ROS models in different conditions and fuel types.

### `exporter`
A generator module that creates C++ code compatible with the ForeFire solver from the python file. This allows for the integration of the ROS models into larger wildfire simulation frameworks.

### `fuels`
This directory hosts data and configurations related to different types of fuels. Some are models specific, some are more generic.

### `models`
Includes a variety of ROS models, each with reference. 

### `test`
Contains test scripts and example applications of the ROS models and sample plots to compare them

## Contributing
Contributions to the library are welcome. Especially add models by copy pasting any of each model python file, and use exact same function names.

## License
GPL

## Contact
Jean-Baptiste Filippi - SPE - filippi_j@univ-corse.fr
