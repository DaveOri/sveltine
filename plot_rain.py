# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 17:37:28 2018

@author: dori
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dbfolder = '/data/optimice/scattering_databases/rain/'

mrr = pd.read_csv(dbfolder+'0.C_24.1GHz.csv')
Ka = pd.read_csv(dbfolder+'0.C_35.5GHz.csv')
mirac = pd.read_csv(dbfolder+'0.C_94.0GHz.csv')

def refl(df):
    return 10.0*np.log10(df['wavelength[mm]']**4*df['radarsx[mm2]']/(np.pi**5*df['K2']))

fig,ax=plt.subplots()
ax.plot(mrr['diameter[mm]'],refl(mrr),label='MRR 24.4')
ax.plot(Ka['diameter[mm]'],refl(Ka),label='Ka 35.5')
ax.plot(mirac['diameter[mm]'],refl(mirac),label='mirac 94')
ax.plot(mirac['diameter[mm]'],10.0*np.log10(mirac['diameter[mm]']**6),label='Rayleigh')
ax.set_xlabel('equivalent volume diameter [mm]')
ax.set_ylabel('equvalent reflectivity [dbZ]')
ax.legend()
#ax.set_yscale('log')
#ax.set_xscale('log')
ax.grid()
fig.savefig('rain_reflectivity.png',dpi=300)
print(refl(mrr)[0],refl(Ka)[0],refl(mirac)[0],(mirac['diameter[mm]']**6)[0])