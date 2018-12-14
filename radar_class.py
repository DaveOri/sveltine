#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 13:57:54 2018

@author: dori
"""

class radar(object): # I declare a class which inherits from a generic object

  def __init__(self, Z_sensitivity, doppler_range, radar_name='joyrad35'):
    # __init__ is a special function that is called every time you want to initialize a "radar"
    # you can perform more intelligent operations, but here I just copy the input into radar attributes
    # If you want to be able to copy data into your object, the first argument of __init__ MUST be 'self'
    self.Z_sensitivity = Z_sensitivity
    self.radar_name = radar_name
    self.doppler_range = doppler_range

rad0 = radar(-30.3, [-80.4, 80.1], 'Joyrad10')
rad1 = radar(-50.7, [-20.0, 20.0]) # Here I create a radar using the default name joyrad35

# BE CAREFUL python does not check type consistency
# The following is a perfectly legitimate line, data is copied but it is of an inconsistent type
rad2 = radar('sensitivity string', {'doppler':-34}, 12)

radar_list = [rad0, rad1, rad2]

for rad in radar_list:
  print(rad.radar_name, ' Zsensitivity=',rad.Z_sensitivity, ' Doppler_range=',rad.doppler_range )


