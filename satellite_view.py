#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 09:57:58 2018

@author: dori
"""

import matplotlib.pyplot as plt
import numpy as np

R = 6.371e6 # Earth mean radius, assume sphere
H = 1.8 # height of a mean tall man

Se = 4.*np.pi*R**2 # Earth surface extent

def satview(h):
  a = np.pi*0.5 - np.arcsin(R/(R+h))
  o = 4*np.pi*np.sin(a*0.5)**2
  return o*R**2

mansee = satview(H) # ca 72 km**2

Hiss = 370.0e3 # ISS, Hubble
Hsun = 800.0e3 # sun-syncro satellites, science obs, Iridium satellites (flares in the sky)
Hmeo = 20.2e6 # GNSS
Hgeo = 35.786e6 #

Hbm = 29.0e6 # distance for Blue marble
Hma = 405.4e6 # Moon apogee
Hl1 = 1.4811e11 # Lagrangian point L1 Earth-Sun system
H = np.logspace(np.log10(1000),np.log10(Hbm),1000)

plt.figure()
plt.plot(H,satview(H)/Se)
plt.vlines([Hiss,Hsun,Hmeo,Hbm],ymin=0.0,ymax=0.5)
plt.grid()

H = np.logspace(np.log10(10000),np.log10(Hl1),1000)

plt.figure()
plt.semilogx(H,satview(H)/Se)
plt.vlines([Hiss,Hsun,Hmeo,Hgeo,Hbm,Hma,Hl1],ymin=0.0,ymax=0.5)
plt.grid()