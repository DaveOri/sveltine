# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 15:03:19 2017

@author: dori
"""

import numpy as np
from pytmatrix.tmatrix import Scatterer
from pytmatrix import scatter
from pytmatrix import tmatrix_aux
from pytmatrix import refractive
from pytmatrix import orientation
from pytmatrix import radar
import pandas as pd
import os.path
import time
from multiprocessing import Pool

from sys import argv

script, freq_str = argv
#freq_str = '85.5'

sizes = np.linspace(0.01,40,2000)
freq = np.array([float(freq_str)])

ghz2mm = lambda x : 299.792458/x
#md = lambda D : 8.9e-2*D**2.1  # g/cm3 == mg/mm3
md = lambda D : 2.4114e-2*D**1.9

six_pi = 6.0/np.pi
ar = 0.6 # axis ratio
rho = lambda D : min(six_pi*md(D)/(ar*D**3),0.917) # limit to pure ice density

cols = ['f','wl','rho','mr','mi','Dmax','Csca','Cbk','sigmabk','Cext','g']

savename = '/home/dori/public_html/BF95/'+freq_str+'TM_rndori_BF95.csv'
if os.path.isfile(savename):
    res = pd.read_csv(savename,sep=',')
    res.drop('Unnamed: 0',axis=1,inplace=True)
else:
    res = pd.DataFrame(index=np.arange(0,len(sizes)*len(freq)),
                       columns=cols,dtype=np.float64)
    res.Dmax = sizes
    for s in sizes:
        res.loc[res.Dmax == s, 'rho'] = rho(s)

#%%
f = float(freq_str)
wl = ghz2mm(f)

def compute(i):
    s = res.loc[i,'Dmax']
    start = time.time()
    print(res.loc[i])
    if res.loc[i].hasnans():
        print('computing')
        density = rho(s) 
        m = refractive.mi(wl,density)
        scatterer = Scatterer(radius=0.5*s,
                              wavelength=wl,
                              m=m,axis_ratio=1.0/ar,
                              radius_type=Scatterer.RADIUS_MAXIMUM)
        scatterer.set_geometry(tmatrix_aux.geom_vert_back)
        scatterer.orient = orientation.orient_averaged_fixed
        scatterer.or_pdf = orientation.uniform_pdf()
        res.loc[i,'f'] = f
        res.loc[i,'wl'] = wl
        res.loc[i,'rho'] = density
        res.loc[i,'mr'] = m.real
        res.loc[i,'mi'] = m.imag
        res.loc[i,'Dmax'] = s
        res.loc[i,'Csca'] = scatter.sca_xsect(scatterer)
        res.loc[i,'Cbk'] = scatter.sca_intensity(scatterer)
        res.loc[i,'sigmabk'] = radar.radar_xsect(scatterer)
        res.loc[i,'Cext'] = scatter.ext_xsect(scatterer)
        res.loc[i,'g'] = scatter.asym(scatterer)
        res.to_csv(savename)
    end = time.time()
    print(s,end-start)

## DO THE JOB ##

#for s in sizes:
#    compute(s)
for idx in res.index:
    compute(idx)
#pool = Pool(8)
#pool.map(compute,sizes)
