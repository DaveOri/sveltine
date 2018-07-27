#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 10:56:02 2018

@author: dori
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

beta = np.linspace(1.5,3.25,100)
delta = np.array([0.2,0.4,0.6])
mu = np.array([-1.0,0.0,1.0])
markers=['h',',','+']


def DZ(b,d,m):
  return gamma(7.0+m)*gamma(b+d+1.0+m)**2.0/(gamma(2.0*b+1.0+m)*gamma(4.0+d+m)**2.0)

def bin_cen(arr):
  return arr[:-1]+0.5*np.diff(arr)

f,ax=plt.subplots(1,1,figsize=(12,12))

for m,mk in zip(mu,markers):
  for d in delta:
    dz = []
    for b in beta:
      dz.append(10.0*np.log10(DZ(b,d,m)))
    #plt.plot(beta,dz,label='$\mu$='+str(m)+' $\delta$='+str(d),marker=mk)
    plt.plot(bin_cen(beta),np.diff(beta)/np.diff(dz),label='$\mu$='+str(m)+' $\delta$='+str(d),marker=mk)
ax.grid()
ax.legend()