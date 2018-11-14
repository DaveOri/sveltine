#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 17:20:09 2018

@author: dori
"""

import pandas as pd
from scipy.interpolate import interp2d, LinearNDInterpolator

# Here I just read the .csv table with pandas, because... pandas is great for that
names=['model','ELWP','mkg','Dmax','Rgyr','ar','riming','Xh','Xv','Kuh','Kuv','Kah','Kav','Wh','Wv']
LUT = pd.read_csv('/work/SnowCases_BAECC/density_Jussi/DATA/lut.dat', # ofcourse your path and name will be different
                  #sep=r'\s*',
                  delim_whitespace=True, # Comment this line and uncomment the one above if you have an old version of pandas
                  header=None,
                  index_col=False,
                  names=names)

# Eventually I slice the LUT according to some condition
myLUT = LUT[LUT.model != 'C'] # Here for example I exclude model C

#Now we create an interpolator for each frequency we need
interpX=interp2d(x=myLUT.mkg,
                 y=myLUT.Dmax,
                 z=myLUT.Xv, # It is gonna take a little bit
                 kind='linear')


interpKa=interp2d(x=myLUT.mkg,
                  y=myLUT.Dmax,
                  z=myLUT.Kav,
                  kind='linear')

interpW=interp2d(x=myLUT.mkg,
                 y=myLUT.Dmax,
                 z=myLUT.Wv,
                 kind='linear')

# Let's create better interpolators with LinearNDInterpolator since I am not satisfied with interp2d
intKa = LinearNDInterpolator(points=myLUT[['mkg','Dmax']],
                             values=myLUT.Kav)

intX = LinearNDInterpolator(points=myLUT[['mkg','Dmax']],
                            values=myLUT.Xv)

intW = LinearNDInterpolator(points=myLUT[['mkg','Dmax']],
                            values=myLUT.Wv)


#%% Lets do some testing
import numpy as np

# Create input D and mass
md = lambda D : 0.021*D**2.05 # some m-D relation
Dmax = np.linspace(1.e-4,2.e-2,100)
masses = md(Dmax)

# Calculate interpolated data
sigmaX = interpX(masses,Dmax).diagonal() # I need the diagonal of the matrix because this function returns the 2D mesh for each possible combination of mass and size
sigmaKa = interpKa(masses,Dmax).diagonal()
sigmaW = interpW(masses,Dmax).diagonal()

# Calculate interpolated data with another method
sigX = intX(masses,Dmax)
sigKa= intKa(masses,Dmax)
sigW = intW(masses,Dmax)

import matplotlib.pyplot as plt

#Check if my input data are on the m-D span
plt.figure()
plt.scatter(myLUT.Dmax,myLUT.mkg)
plt.plot(Dmax,masses,'r')
plt.yscale('log')
plt.title('mass - size')

plt.figure()
plt.scatter(myLUT.Dmax,myLUT.Xv)
plt.plot(Dmax,sigmaX,'r')
plt.plot(Dmax,sigX,'k')
plt.yscale('log')
plt.xlim([0,0.02])
plt.ylim([1e-14,1e-6])
plt.title('Xband - size')

plt.figure()
plt.scatter(myLUT.Dmax,myLUT.Kav)
plt.plot(Dmax,sigmaKa,'r')
plt.plot(Dmax,sigKa,'k')
plt.yscale('log')
plt.xlim([0,0.02])
plt.ylim([1e-14,1e-6])
plt.title('Kaband - size')

plt.figure()
plt.scatter(myLUT.Dmax,myLUT.Wv)
plt.plot(Dmax,sigmaW,'r')
plt.plot(Dmax,sigW,'k')
plt.yscale('log')
plt.xlim([0,0.02])
plt.ylim([1e-14,1e-6])
plt.title('Wband - size')