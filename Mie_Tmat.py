# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 18:30:35 2018

@author: dori
"""
import sys
sys.path.append('/work/DBs/scattnlay')
from scattnlay import scattnlay
from pytmatrix import tmatrix, scatter, radar

import numpy as np

r = 2.0
wl = 100.0
m = complex(1.5, 0.5)
x = 2.*np.pi*r/wl
k = 2.*np.pi/wl

scatterer = tmatrix.Scatterer(radius=r, wavelength=wl, m=m, axis_ratio=1.0)
S, Z = scatterer.get_SZ()
print(S[0,0], S[1,1])

Nc = 1
Nl = 1
xr = np.ndarray((Nc,Nl),dtype=np.float64)
mr= np.ndarray((Nc,Nl),dtype=np.complex128)
xr[:,0] = x
mr[:,0] = m
thetas = np.linspace(0.0,np.pi,180)
terms, Qe, Qs, Qa, Qb, Qp, g, ssa, S1, S2 = scattnlay(xr,mr,theta=thetas)
print(S1[0,-1]/k,S2[0,-1]/k)
s1 = S1[0,0]/k
s2 = S2[0,0]/k
SM = 0.0*S
SM[0,0] = -1.0j*s2
SM[1,1] = -1.0j*s1

print("Cext = ", scatter.ext_xsect(scatterer), Qe[0]*r*r*np.pi)
print("Csca = ", scatter.sca_xsect(scatterer), Qs[0]*r*r*np.pi)
print("Cbck = ", radar.radar_xsect(scatterer), Qb[0]*r*r*np.pi)

print(S[0,0].real/S1[0,0].real)
print(S[0,0].imag/S1[0,0].imag)

print(S[1,1].real/S2[0,0].real)
print(S[1,1].imag/S2[0,0].imag)


Z11 = 0.5*(abs(s1)**2+abs(s2)**2)
Z33 = 0.5*(s1*s2.conjugate()+s1.conjugate()*s2)

print(Z[0,0]/Z11)
print(Z[2,2]/Z33)