# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 11:45:55 2017

@author: dori
"""

# This line is requested at the beginning of the file for python2 python3 compatibility
from __future__ import print_function, division

# Ordinary imports
from netCDF4 import Dataset
import numpy as np

# Define path and filename
nc_folder = '/home/lpfitzen/Earthcare_test_scenes/'
nc_filename = 'CPR_Test_data_39316D2_2014120712_interpolated.nc'

# Open the netCDF file
nc_file = Dataset(nc_folder + nc_filename)

# Get tipical netCDF4 content
nc_dimensions = nc_file.dimensions
nc_variables = nc_file.variables

##### ACHTUNG ACHTUNG ACHTUNG ####
# We have been able to do that because the nc file does not have any group within
# If the file has groups, even if it has only one group, 
# you first have to select the group and then access the dimensions and variables

# Both dimensions and variables are python Ordered Dictionaries objects.
# This means you can access their "keys" and "values"

print(nc_dimensions.keys())
print(nc_variables.keys())


# Or you can just print the content of the variables to have a full list of full
# description of each varaible, including measuring units and dimensions
print(nc_variables)

# But you mostly be interested in one variable at a time, like, lets say temperature
print(nc_variables['temperature'])

# You can use the variable as it is, but you can always copy the values into a 
# multidimension numpy array
Temp = nc_variables['temperature'][:]
