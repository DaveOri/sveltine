#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 09:16:03 2019

@author: dori
"""

####### CREATE DATASET #################
import numpy as np
N = 1000
X = np.linspace(0,1,N)
Y = 0.2*X**2.1 + np.random.randn(N)*0.01

#######################################



from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def powLaw(x,a,b):
  return a*x**b

def quadratic(x,a):
  return a*x**2

paramsPL, covarsPL = curve_fit(powLaw, X, Y)
paramsQ, covarsQ = curve_fit(quadratic, X, Y)


#plt.figure()
plt.scatter(X,Y)
plt.plot(X, powLaw(X, *paramsPL))

#plt.figure()
#plt.scatter(X,Y)
plt.plot(X, quadratic(X, *paramsQ))
