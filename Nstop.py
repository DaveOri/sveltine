#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 17:15:23 2018

@author: dori
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(1.0e-6,1.0e6,1e6)

n1 = lambda x: (x+4.0*x**(1.0/3.0)+1).round()
n2 = lambda x: (x+4.05*x**(1.0/3.0)+2).round()
n3 = lambda x: (x+4.0*x**(1.0/3.0)+2).round()

plt.figure()
plt.plot(x,n1(x)-n2(x))
#plt.plot(x,)
plt.figure()
plt.plot(x,n1(x)-n3(x))