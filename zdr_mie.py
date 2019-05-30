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

# Reference Mie calculation

wl = tmatrix_aux.wl_W
el = 0.
m = refractive.m_w_10C[wl]
scatterer = tmatrix.Scatterer(wavelength=wl,
                              m=m,
                              axis_ratio=1.0,
                              radius_type=tmatrix.Scatterer.RADIUS_MAXIMUM,
                              thet0=90.0-el, thet=90.0+el)

Dmax = np.linspace(0.1, 2.7, 100)
Zhh = 0.0*Dmax
Zvv = 0.0*Dmax
Zdr = 0.0*Dmax
for i, D in enumerate(Dmax):
    scatterer.radius = 0.5*D
    Zdr[i] = 10.0*np.log10(radar.Zdr(scatterer))
    Zhh[i] = 10.0*np.log10(radar.refl(scatterer, h_pol=True))
    Zvv[i] = 10.0*np.log10(radar.refl(scatterer, h_pol=False))

plt.figure()
ax0=plt.gca()
ax0.plot(Dmax, Zhh, label='Zhh')
ax0.plot(Dmax, Zvv, label='Zvv')
ax0.vlines(wl*0.5, ymin=-14, ymax=0)
ax0.legend()
ax0.grid()
ax0.set_ylabel('Z  [dbZ]')
ax0.set_xlabel('Dmax   [mm]')
ax1 = ax0.twinx()
ax1.plot(Dmax, Zdr, c='C3', label='Zdr')
ax1.legend()
ax1.set_ylabel('Zdr [dB]')
ax1.set_ylim([-1, 1])

# Experiment 2mm Dmax change ar from

scatterer = tmatrix.Scatterer(wavelength=wl,
                              m=m,
                              radius=2.0,
                              radius_type=tmatrix.Scatterer.RADIUS_MAXIMUM,
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
ax0.plot(ar, Zhh, label='Zhh')
ax0.plot(ar, Zvv, label='Zvv')
ax0.legend(loc=1)
ax0.grid()
ax0.set_ylabel('Z  [dbZ]')
ax0.set_xlabel('aspect ratio')
ax1 = ax0.twinx()
ax1.plot(ar, Zdr, c='C3', label='Zdr')
ax1.set_ylabel('Zdr [dB]')
ax1.legend(loc=3)

# Vertical prolate at horizontal incidence increase size and ar such that
# horizontal length (electric length) is kept constant

scatterer = tmatrix.Scatterer(wavelength=wl,
                              m=m,
                              radius=2.0,
                              radius_type=tmatrix.Scatterer.RADIUS_MAXIMUM,
                              thet0=90.0-el, thet=90.0+el)

Dh = 1.0 # mm horizontal length fixed
Dv = np.linspace(1.0, 2.7, 100) # horizontal length
ar = Dh/Dv # horizontal to vertical (rotational) ratio
Zhh = 0.0*ar
Zvv = 0.0*ar
Zdr = 0.0*ar
for i, [D, a] in enumerate(zip(Dv, ar)):
    scatterer.radius = 0.5*D
    scatterer.axis_ratio = a
    scatterer.ndgs = 4
    Zdr[i] = 10.0*np.log10(radar.Zdr(scatterer))
    Zhh[i] = 10.0*np.log10(radar.refl(scatterer, h_pol=True))
    Zvv[i] = 10.0*np.log10(radar.refl(scatterer, h_pol=False))

plt.figure()
ax0=plt.gca()
ax0.plot(Dv, Zhh, label='Zhh')
ax0.plot(Dv, Zvv, label='Zvv')
ax0.legend(loc=1)
ax0.grid()
ax0.set_ylabel('Z  [dbZ]')
ax0.set_xlabel('vertical length [mm]')
ax1 = ax0.twinx()
ax1.plot(Dv, Zdr, c='C3', label='Zdr')
ax1.set_ylabel('Zdr [dB]')
ax1.legend(loc=3)
ax0.set_title('Dh=1 prolate never resonate')

# Vertical oblate at horizontal incidence increase size and ar such that
# vertical is kept constant

wl = tmatrix_aux.wl_W
el = 0.
scatterer = tmatrix.Scatterer(wavelength=wl,
                              m=m,
                              radius=2.0,
                              radius_type=tmatrix.Scatterer.RADIUS_MAXIMUM,
                              thet0=90.0-el, thet=90.0+el)

Dv = 1.4 # mm horizontal length fixed
Dh = np.linspace(1.0, 2.7, 100) # horizontal length
ar = Dh/Dv # horizontal to vertical (rotational) ratio
Zhh = 0.0*ar
Zvv = 0.0*ar
Zdr = 0.0*ar
for i, [D, a] in enumerate(zip(Dh, ar)):
    scatterer.radius = 0.5*D
    scatterer.axis_ratio = a
    scatterer.ndgs = 4
    Zdr[i] = 10.0*np.log10(radar.Zdr(scatterer))
    Zhh[i] = 10.0*np.log10(radar.refl(scatterer, h_pol=True))
    Zvv[i] = 10.0*np.log10(radar.refl(scatterer, h_pol=False))

plt.figure()
ax0=plt.gca()
ax0.plot(Dh, Zhh, label='Zhh')
ax0.plot(Dh, Zvv, label='Zvv')
ax0.legend(loc=1)
ax0.grid()
ax0.set_ylabel('Z  [dbZ]')
ax0.set_xlabel('horizontal length [mm]')
ax1 = ax0.twinx()
ax1.plot(Dh, Zdr, c='C3', label='Zdr')
ax1.set_ylabel('Zdr [dB]')
ax1.legend(loc=3)
ax0.set_title('Dv=1 oblate resonate both vv and hh')