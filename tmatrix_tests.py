# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 12:37:33 2017

@author: dori
"""

from pytmatrix import tmatrix, scatter, psd, tmatrix_aux, orientation, tmatrix_psd, refractive, radar
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

wl = tmatrix_aux.wl_Ku
sd = 0.2 # snow density
scatt = tmatrix.Scatterer(radius=10.0,
                          radius_type=2,
                          wavelength=wl,
                          axis_ratio=1.0/0.15,
                          m=refractive.mi(wl,sd),
                          thet0=90.0,
                          thet=90.0,
                          phi0=0.0,
                          phi=180.0)

radii = np.linspace(1.0,10,1000)
Zh = []
Zv = []
for r in radii:
    scatt.radius = r
    scatt.set_geometry(tmatrix_aux.geom_horiz_back)
    Zh.append(10.0*np.log10(radar.refl(scatt,h_pol=True)))
    Zv.append(10.0*np.log10(radar.refl(scatt,h_pol=False)))

plt.figure()
plt.plot(radii,Zh,label='Zh')
plt.plot(radii,Zv,label='Zv')
Zdr = np.array(Zh)-np.array(Zv)
plt.plot(radii,Zdr,label='Zdr')
plt.legend()
plt.grid()

thetas = np.linspace(0.0,90.0,200)
Zh = []
Zv = []
for th in thetas:
    scatt.radius = 10.0
    scatt.set_geometry((th,th,0.0,180.0,0.0,0.0))
    Zh.append(10.0*np.log10(radar.refl(scatt,h_pol=True)))
    Zv.append(10.0*np.log10(radar.refl(scatt,h_pol=False)))

plt.figure()
plt.plot(thetas,Zh,label='Zh')
plt.plot(thetas,Zv,label='Zv')
Zdr = np.array(Zh)-np.array(Zv)
plt.plot(thetas,Zdr,label='Zdr')
plt.legend()
plt.grid()