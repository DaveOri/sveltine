#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 25 19:43:31 2019

@author: dori
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma

from pytmatrix import tmatrix
from pytmatrix import tmatrix_aux
from pytmatrix import radar
from pytmatrix import refractive
from pytmatrix import orientation
from pytmatrix import psd

def genGamma(Nl, D0, mu):
    Lambda = (3.67+mu)/D0
    def gam(D):
        return Nl*0.03*D0**4*Lambda**(mu+4.0)*np.exp(-Lambda*D)/gamma(mu+4.0)

#Lambda = (3.67+mu)/D0
D0s = np.linspace(0.75, 2.2, 10)
Zhh = 0.0*D0s
Ai = 0.0*D0s

wl = tmatrix_aux.wl_W
el = 0.

scatterer = tmatrix.Scatterer(wavelength=wl,
                              m=refractive.m_w_10C[wl],
                              #kw_sqr=tmatrix_aux.K_w_sqr[wl],
                              radius_type=tmatrix.Scatterer.RADIUS_MAXIMUM,
                              #or_pdf=orientation.gaussian_pdf(std=1.0),
                              #orient=orientation.orient_averaged_fixed,
                              thet0=90.0-el, thet=90.0+el)
Nw = 8000.0 # mm-2 m-3
mu = 5
scatterer.psd_integrator = psd.PSDIntegrator(D_max=8.0,
                                             geometries=(tmatrix_aux.geom_horiz_back,
                                                         tmatrix_aux.geom_horiz_forw))
scatterer.psd_integrator.init_scatter_table(scatterer)
for i, D0 in enumerate(D0s):
    scatterer.psd = genGamma(Nw, D0, mu)#psd.GammaPSD(D0=D0, mu=mu, Nw=Nw)
    scatterer.set_geometry(tmatrix_aux.geom_horiz_back)
    Zhh[i] = 10.0*np.log10(radar.refl(scatterer))
    scatterer.set_geometry(tmatrix_aux.geom_horiz_forw)
    Ai[i] = radar.Ai(scatterer)

plt.plot(D0s, Zhh)
plt.plot(D0s, Zhh-2.0*Ai*0.25)
plt.ylim([11, 26])
plt.grid()