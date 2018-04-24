#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 15:29:23 2018

@author: dori
"""
import numpy as np
import pandas as pd

from pytmatrix.tmatrix import Scatterer 
from pytmatrix import tmatrix_aux, orientation, radar, scatter
from refractiveIndex import water
from refractiveIndex import utilities as ref_utils

from sys import argv

script, temperatures, frequencies = argv

#frequencies = np.array([24.1e9,35.5e9,94.0e9])
frequencies = np.array([float(frequencies)])
c = 299792458.
wl_m = c/frequencies
wl_mm = wl_m*1000.0

sizes = np.arange(0.01,8.5,0.01)
#temperatures = np.array([273.15,283.15,293.15])
temperatures = np.array([float(temperatures)])

for T in temperatures:
    for wl,f in zip(wl_mm,frequencies):
        table = pd.DataFrame(index=sizes, columns=['T[k]','wavelength[mm]','K2','radarsx[mm2]','extxs[mm2]'])
        table.index.name = 'diameter[mm]'
        m = water.n(T,f)
        K2 = ref_utils.K2(m**2)
        print(T,wl,K2)
        for d in sizes:
            rain = Scatterer(radius=0.5*d,
                             wavelength=wl,
                             m=m,
                             axis_ratio=1.0/tmatrix_aux.dsr_thurai_2007(d))
            rain.Kw_sqr = K2
            rain.or_pdf = orientation.gaussian_pdf(std=20.0)
            rain.orient = orientation.orient_averaged_adaptive
            rain.set_geometry(tmatrix_aux.geom_vert_back)
            rxs = radar.radar_xsect(rain)
            rain.set_geometry(tmatrix_aux.geom_vert_forw)
            ext = scatter.ext_xsect(rain)
            print(d,rxs,ext,T,f)
            table.loc[d] = T,wl,K2,rxs,ext
        table.to_csv(str(T-273.15)[:2]+'C_'+str(f*1e-9)+'GHz.csv')
