#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 10:35:52 2018

@author: dori
"""

import scipy as sc
import numpy as np
import pandas as pd
import netCDF4 as nc
from netCDF4 import Dataset
from datetime import datetime, timedelta

parsPath = '/data/obs/site/nya/parsivel/l1'

year = '2018'
month = '03'
day = '14'
datePath = ('/').join([year,  month, day])

date = '2018/03/14'

# Parsivel
strDate = ('').join([year,month,day])
fileName = 'parsivel_nya_'+strDate+'.nc'
parsFile = ('/').join([parsPath, datePath, fileName])

#print datePath
#print strDate 
#print fileName
#print parsFile

#Reading the NetCDF File from Parsivel 
parsNC = Dataset(parsFile, 'r')

zPar = parsNC.variables['Z'][:] # in [dB]
tPar = parsNC.variables['time'][:]
NPar = parsNC.variables['N'][:] # log_10(1/mÂ³ mm)

# Create a DataFrame to look at the Data and to prepare for plot
epoch = pd.datetime(1970, 1, 1)
timesPar = epoch + pd.to_timedelta(tPar,unit='s')
#timesPar = np.zeros(tPar.shape[0])

#trying a loop for saving times (but does not work yet either)
#for t in range(tPar.shape[0]):
#    timesPar[t] = timedelta(seconds=tPar[t]) 
#print timesPar

plt.bar(range(32),NPar[:,76])
plt.xlabel('size class')
plt.ylabel('N')
plt.title('Nya '+date)
plt.savefig('/home/dori/nya_psd.png')
