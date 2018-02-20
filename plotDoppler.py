# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 11:35:50 2017

@author: dori
"""

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import pandas as pd

from microphysics import vSEDIVEL_ICON

plt.close('all')

# Define some paths and filenames

icon_folder = '/data/inscape/icon/experiments/'

mid_lat_filename   = icon_folder + 'tripex_220km/newicon/METEOGRAM_patch001_joyce.nc'
mid_lat_res_filename = 'ICON/newICON5f20151124_dfNEW.nc'
mid_lat_dop_filename = 'ICON/test_spectrum.nc'
mid_lat_dop_powLname = 'ICON/test_spectrum_powLaw.nc'

mix_phase_filename = icon_folder + 'acloud/RF06-2705/postproc/rf06_sat_all.nc'
mix_phase_res_filename = 'ICON4vera/mixed_phase_5f.nc'
nya_filename = icon_folder + 'nyalesund/newicon-2017-06-23-albedo/METEOGRAM_patch004_awipev.nc'
nya_res_filename = 'ICON4vera/nyalesund_patch004_5f.nc'

frt_filename = icon_folder + 'fronts_postproc/METEOGRAM_patch004_joyce_26only.nc'
frt_res_filename = 'ICON4vera/fronts26only.nc'


# Open the netcdf files

mid_lat_data = Dataset(mid_lat_filename)
mid_lat_res = Dataset(mid_lat_res_filename)
mid_lat_dop = Dataset(mid_lat_dop_filename)
mid_lat_pwL = Dataset(mid_lat_dop_powLname)


mix_phase_data = Dataset(mix_phase_filename)
mix_phase_res = Dataset(mix_phase_res_filename)
nya_data = Dataset(nya_filename)
nya_res = Dataset(nya_res_filename)
frt_data = Dataset(frt_filename)
frt_res = Dataset(frt_res_filename)

# Extract Variables and Dimensions

ml_dt_dim = mid_lat_data.dimensions
ml_dt_var = mid_lat_data.variables
ml_rs_dim = mid_lat_res.dimensions
ml_rs_var = mid_lat_res.variables
ml_dp_dim = mid_lat_dop.dimensions
ml_dp_var = mid_lat_dop.variables
ml_pw_dim = mid_lat_pwL.dimensions
ml_pw_var = mid_lat_pwL.variables


ny_dt_dim = nya_data.dimensions
ny_dt_var = nya_data.variables
ny_rs_dim = nya_res.dimensions
ny_rs_var = nya_res.variables

fr_dt_dim = frt_data.dimensions
fr_dt_var = frt_data.variables
fr_rs_dim = frt_res.dimensions
fr_rs_var = frt_res.variables

mp_dt_dim = mix_phase_data.dimensions
mp_dt_var = mix_phase_data.variables
mp_rs_dim = mix_phase_res.dimensions
mp_rs_var = mix_phase_res.variables

# Define Plotting Function

def plot_variable(x,y,v,axes,
                  xlab=None,ylab=None,vlab=None,title=None,
                  vmin=None,vmax=None,xlim=None,ylim=None):
    mesh = axes.pcolormesh(x,y,v,vmin=vmin,vmax=vmax,cmap='jet')
    axes.set_title(title)
    plt.colorbar(mesh,label=vlab,ax=axes)
    if xlab is not None:
        axes.set_xlabel(xlab)
    if ylab is not None:
        axes.set_ylabel(ylab)
    axes.set_xlim(xlim)
    axes.set_ylim(ylim)

H = ml_rs_var['height'][:,0,:]*0.001
times   = ml_dt_var['time'] # seconds since 2015-11-24 02:00:03 proplectic gregorian
units=times.units.split('since')[0]
basetime=pd.to_datetime(times.units.split('since')[-1])
dtimes = pd.to_timedelta(times[:],unit=str(units)[0])
tt=np.tile((basetime + dtimes),(H.shape[1],1)).T

f,((ax1,ax2,ax3,ax4)) = plt.subplots(4,1,sharex=True)
ylim=(0,15)
xfmt = md.DateFormatter('%H:%M')
Zx = ml_rs_var['Ze'][:,0,:,0,0,0]
Zu = ml_rs_var['Ze'][:,0,:,1,0,0]
Za = ml_rs_var['Ze'][:,0,:,2,0,0]
Zw = ml_rs_var['Ze'][:,0,:,3,0,0]
Zg = ml_rs_var['Ze'][:,0,:,4,0,0]
plot_variable(tt,H,Zu,ax1,None,'height [km]','dBZ','Ku-band Ze',-20,20,ylim=ylim)
plot_variable(tt,H,Za,ax2,None,'height [km]','dBZ','Ka-band Ze',-20,20,ylim=ylim)
plot_variable(tt,H,Zw,ax3,None,'height [km]','dBZ', 'W-band Ze',-20,20,ylim=ylim)
plot_variable(tt,H,Zg,ax4,'time','height [km]','dBZ', 'G-band Ze',-20,20,ylim=ylim)

f,((ax1,ax2,ax3,ax4)) = plt.subplots(4,1,sharex=True)
ylim=(0,15)
xfmt = md.DateFormatter('%H:%M')
Vx = ml_dp_var['Radar_MeanDopplerVel'][:,0,:,0,0,0]
Vu = ml_dp_var['Radar_MeanDopplerVel'][:,0,:,1,0,0]
Va = ml_dp_var['Radar_MeanDopplerVel'][:,0,:,2,0,0]
Vw = ml_dp_var['Radar_MeanDopplerVel'][:,0,:,3,0,0]
Vg = ml_dp_var['Radar_MeanDopplerVel'][:,0,:,4,0,0]
plot_variable(tt,H,Vu,ax1,None,  'height [km]','m/s','Ku-band MDV',0,2,ylim=ylim)
plot_variable(tt,H,Va,ax2,None,  'height [km]','m/s','Ka-band MDV',0,2,ylim=ylim)
plot_variable(tt,H,Vw,ax3,None,  'height [km]','m/s', 'W-band MDV',0,2,ylim=ylim)
plot_variable(tt,H,Vg,ax4,'time','height [km]','m/s', 'G-band MDV',0,2,ylim=ylim)


what=7500
plt.figure()
plt.plot(Vx[what],H[what,:],label='X')
plt.plot(Vu[what],H[what,:],label='Ku')
plt.plot(Va[what],H[what,:],label='Ka')
plt.plot(Vw[what],H[what,:],label='W')
plt.plot(Vg[what],H[what,:],label='G')
plt.legend()
plt.grid()
plt.title('Mean doppler velocity profile... 24.11.2015 at sometime')
plt.xlabel('MDV    [m/s]')
plt.ylabel('height    [km]')

QNI = np.ma.masked_less(np.flip(ml_dt_var['QNI'][:],1),0.1)#.filled(fill_value=np.nan)
QI  = np.ma.masked_less(np.flip(ml_dt_var['QI' ][:],1),0.1)#.filled(fill_value=np.nan)
QNS = np.ma.masked_less(np.flip(ml_dt_var['QNS'][:],1),0.1)#.filled(fill_value=np.nan)
QS  = np.ma.masked_less(np.flip(ml_dt_var['QS' ][:],1),0.1)#.filled(fill_value=np.nan)

Vpw = ml_pw_var['Radar_MeanDopplerVel'][:,0,:,0,0,0]
sedVI = vSEDIVEL_ICON(QI,QNI,2,'ice_cosmo5')
sedVS = vSEDIVEL_ICON(QS,QNS,2,'snowSBB')

f,((ax1,ax2,ax3)) = plt.subplots(3,1,sharex=True)
ylim=(0,15)
xfmt = md.DateFormatter('%H:%M')
plot_variable(tt,H,Vx        ,ax1,  None,'height [km]','m/s', 'X-band MDV pamtra Heymsfield',0,2,ylim=ylim)
plot_variable(tt,H,Vpw,ax2,  None,'height [km]','m/s', 'X-band MDV pamtra powLaw',0,2,ylim=ylim)
plot_variable(tt,H,sedVS.data,ax3,'time','height [km]','m/s', 'Sed Vel Zweight Snow',0,2,ylim=ylim)



f,((ax1,ay1),(ax2,ay2),(ax3,ay3),(ax4,ay4),(ax6,ay6)) = plt.subplots(5,2,sharex=True,sharey=True)
var = ml_dt_var['QNI']
vval = np.ma.masked_less(np.flip(var[:],1),0.1)
var_dim_labels = var.dimensions
xvar = ml_dt_var[var_dim_labels[0]]
yvar = ml_dt_var[var_dim_labels[1]]
xval, yval = np.meshgrid(xvar[:], 0.001*yvar[:])
plot_variable(tt,H,vval,ax1,None,'height [Km]',var.name+'  '+var.unit,var.long_name,ylim=ylim)
var = ml_dt_var['QNS']
vval = np.ma.masked_less(np.flip(var[:],1),0.1)
plot_variable(tt,H,vval,ax2,None,'height [Km]',var.name+'  '+var.unit,var.long_name,ylim=ylim)
var = ml_dt_var['QNC']
vval = np.ma.masked_less(np.flip(var[:],1),0.1)
plot_variable(tt,H,vval,ax3,None,'height [Km]',var.name+'  '+var.unit,var.long_name,ylim=ylim)
var = ml_dt_var['QNR']
vval = np.ma.masked_less(np.flip(var[:],1),0.1)
plot_variable(tt,H,vval,ax4,None,'height [Km]',var.name+'  '+var.unit,var.long_name,ylim=ylim)
var = ml_dt_var['QNG']
vval = np.ma.masked_less(np.flip(var[:],1),0.1)
#plot_variable(tt,H,vval,ax5,None,'height [Km]',var.name+'  '+var.unit,var.long_name,ylim=ylim)
#var = ml_dt_var['QNH']
#vval = np.ma.masked_less(np.flip(var[:],1),0.1)
plot_variable(tt,H,vval,ax6,'time','height [Km]',var.name+'  '+var.unit,var.long_name,ylim=ylim)

var = ml_dt_var['QI']
vval = np.ma.masked_less(np.flip(var[:],1),1e-7)
plot_variable(tt,H,vval,ay1,None,None,var.name+'  '+var.unit,var.long_name,ylim=ylim)
var = ml_dt_var['QS']
vval = np.ma.masked_less(np.flip(var[:],1),1e-7)
plot_variable(tt,H,vval,ay2,None,None,var.name+'  '+var.unit,var.long_name,ylim=ylim)
var = ml_dt_var['QC']
vval = np.ma.masked_less(np.flip(var[:],1),1e-7)
plot_variable(tt,H,vval,ay3,None,None,var.name+'  '+var.unit,var.long_name,ylim=ylim)
var = ml_dt_var['QR']
vval = np.ma.masked_less(np.flip(var[:],1),1e-7)
plot_variable(tt,H,vval,ay4,None,None,var.name+'  '+var.unit,var.long_name,ylim=ylim)
var = ml_dt_var['QG']
vval = np.ma.masked_less(np.flip(var[:],1),1e-7)
#plot_variable(tt,H,vval,ay5,None,None,var.name+'  '+var.unit,var.long_name,ylim=ylim)
#var = ml_dt_var['QH']
#vval = np.ma.masked_less(np.flip(var[:],1),1e-7)
plot_variable(tt,H,vval,ay6,'time',None,var.name+'  '+var.unit,var.long_name,ylim=ylim)
ax4.xaxis.set_major_formatter(xfmt)