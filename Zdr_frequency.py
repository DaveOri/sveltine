# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 11:52:19 2018

@author: dori
"""

from pytmatrix import scatter, tmatrix_aux, refractive, orientation, radar, psd, tmatrix
import numpy as np
#import pandas as pd
#import os.path
#import time
import matplotlib.pyplot as plt

#sizes = np.linspace(0.01,40,2000)
wavelengths = [tmatrix_aux.wl_X,tmatrix_aux.wl_Ka,tmatrix_aux.wl_W]

six_pi = 6.0/np.pi
ar = 0.6

#md = lambda D : 8.9e-2*D**2.1  # g/cm3 == mg/mm3
mD = lambda D : 2.4114e-2*D**1.9
rhoD = lambda D : min(six_pi*mD(D)/(D**3),0.917) # limit to pure ice density
#rhoD = lambda D : min(0.9,0.917) # limit to pure ice density

def m_rho_func(wl):
    w = wl
    def m_func(D):
        den = rhoD(D)        
        return refractive.mi(w,den)
    return m_func

lambdas = np.linspace(1,10,20)
D0s = 3.67/lambdas

fig, (ax1,ax2,ax3) = plt.subplots(3,1)#,sharex=True)

Zdr_array = []
Z_array = []
for wl in wavelengths:
    ref_func = m_rho_func(wl)
    for lamb in lambdas:
        scatterer = tmatrix.Scatterer(wavelength=wl,
                              axis_ratio=1.0/ar,
                              Kw_sqr=tmatrix_aux.K_w_sqr[wl])
        scatterer.psd_integrator = psd.PSDIntegrator()
        scatterer.psd_integrator.m_func = ref_func
        scatterer.psd_integrator.geometries=[tmatrix_aux.geom_horiz_back,tmatrix_aux.geom_horiz_forw,]
        scatterer.set_geometry(tmatrix_aux.geom_horiz_back)
        scatterer.psd = psd.ExponentialPSD(N0=1.0,Lambda=lamb,D_max=20.0)
        scatterer.psd_integrator.D_max = 20.0
        scatterer.psd_integrator.init_scatter_table(scatterer)
        Zdr = 10.0*np.log10(radar.Zdr(scatterer))
        scatterer.set_geometry(tmatrix_aux.geom_horiz_forw)
        W = np.pi*1e3*(1.0/lamb)**4
        Kdp = 1.0e6*radar.Kdp(scatterer)/W
        Zdr_array.append(Zdr)
        Z_array.append(Kdp)
    ax1.plot(D0s,Zdr_array,label=wl)
    ax2.plot(D0s,Z_array,label=wl)
    Zdr_array = []
    Z_array = []
ax1.legend()
ax1.grid()
ax2.grid()

ax2.set_xlabel('D0   [mm]')
ax1.set_ylabel('Zdr  [dB]')
ax2.set_ylabel('Kdp  [deg]')
ax1.set_title('m-D Brown and Francis 95 --- constant ar = 0.6')

diams=np.linspace(0.01,10.0,100)
rhos=0.0*diams
for i in range(len(diams)):
    rhos[i]=rhoD(diams[i])
ax3.plot(diams,rhos)
ax3.set_xlabel('Diameter')
ax3.set_ylabel('density')
