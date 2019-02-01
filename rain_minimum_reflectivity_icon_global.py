#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 12:01:37 2019

@author: dori
"""

from scipy.special import gamma
import numpy as np

N0 = 8.0e6
q = 1e-7
ra = 1.0
rw = 1000.0

lam = (N0*rw*np.pi*gamma(4)/(q*ra*6.0))**0.25

Z = 10.0*np.log10(1.0e18*N0*gamma(7)/lam**7)