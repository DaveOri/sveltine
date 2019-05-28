#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 13:52:37 2019

@author: dori
"""

import numpy as np
import matplotlib.pyplot as plt

from pytmatrix import tmatrix
from pytmatrix import tmatrix_aux
from pytmatrix import radar
from pytmatrix import refractive
from pytmatrix import orientation

wl = tmatrix_aux.wl_W
el = 0.

scatterer = tmatrix.Scatterer(wavelength=wl,
                              m=refractive.m_w_10C[wl],
                              radius=2.0,
                              radius_type=tmatrix.Scatterer.RADIUS_MAXIMUM,
                              or_pdf=orientation.gaussian_pdf(std=1.0),
                              orient=orientation.orient_averaged_fixed,
                              thet0=90.0-el, thet=90.0+el)

ar = np.linspace(0.5, 1.5, 100)
Zhh = 0.0*ar
Zvv = 0.0*ar
Zdr = 0.0*ar
for i, a in enumerate(ar):
    scatterer.axis_ratio = a
    Zdr[i] = 10.0*np.log10(radar.Zdr(scatterer))
    Zhh[i] = 10.0*np.log10(radar.refl(scatterer, h_pol=True))
    Zvv[i] = 10.0*np.log10(radar.refl(scatterer, h_pol=False))

plt.figure()
ax0=plt.gca()
ax0.plot(ar, Zhh)
ax0.plot(ar, Zvv)
ax1 = ax0.twinx()
ax1.plot(ar, Zdr, c='C3')



#scatterer = tmatrix.Scatterer(wavelength=wl,
#                              m=refractive.m_w_10C[wl],
#                              radius_type=tmatrix.Scatterer.RADIUS_MAXIMUM,
#                              #axis_ratio=1.0/0.4,
#                              axis_ratio=0.4,
#                              or_pdf=orientation.gaussian_pdf(std=1.0),
#                              orient=orientation.orient_averaged_fixed,
#                              thet0=90.0-el, thet=90.0+el)
#
#sizes = np.linspace(0.2, 2.0, 100)
#Zhh = 0.0*sizes
#Zvv = 0.0*sizes
#Zdr = 0.0*sizes
#for i, d in enumerate(sizes):
#    scatterer.radius = 0.5*d
#    Zdr[i] = 10.0*np.log10(radar.Zdr(scatterer))
#    Zhh[i] = 10.0*np.log10(radar.refl(scatterer, h_pol=True))
#    Zvv[i] = 10.0*np.log10(radar.refl(scatterer, h_pol=False))
#
#plt.figure()
#ax0=plt.gca()
#ax0.plot(sizes, Zhh)
#ax0.plot(sizes, Zvv)
#ax1 = ax0.twinx()
#ax1.plot(sizes, Zdr, c='C3')
#
#    