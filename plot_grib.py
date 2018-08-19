# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 19:02:34 2016

@author: dori
"""

import pygrib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
import numpy as np
from glob import glob

folder = '/media/DATA/JWA/Lightning/Light_'
filend = ['.grb','_USA.grb']

months={'01':'January','02':'February','03':'March','04':'April','05':'May',
        '06':'June','07':'July','08':'August','09':'September','10':'October',
        '11':'November','12':'December'}
        
zones={'North America':[-5,70,-125,-35],
       'Europa':[ 5,70,-35,55],
       'Asia':[-5,70,55,145],
       'North Pacific':[-5,70,145,235],
       'South America':[-60,15,-110,-10],
       'Africa':[-60,15,-10,70],
       'Oceania':[-70,5,70,160],
       'South Pacific':[-70,5,160,250]}

year_maxvalue = {}
         
## Function to plot georeferenciated data, slicing portions, and setting maxvalue
def plot_map(data,lon,lat,corners,savename,titleplot,topvalue,colorlabel=None):
    llat,ulat,llon,rlon = corners
    plt.figure()
    m = Basemap(projection='mill',lat_ts=10,llcrnrlon=llon, urcrnrlon=rlon,
                  llcrnrlat=llat,urcrnrlat=ulat, resolution='i')
    x,y = m(lon,lat)
    
    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(-90.,120.,10.),labels=[1,0,0,0])
    m.drawmeridians(np.arange(-180.,180.,15.),labels=[0,0,0,1])
    m.drawcountries()
    m.drawstates()
    clevs = np.linspace(0,topvalue,200)
    
    cs = m.contourf(x,y,data,clevs,cmap=cm.s3pcpn)
    cbar = plt.colorbar(cs,orientation='vertical',
                        ticks=np.linspace(0,topvalue,11))
    if colorlabel is None:
        colorlabel = 'Flashes km$^{-2}$'
    cbar.set_label(colorlabel)
    plt.title(titleplot)
    plt.savefig(savename,dpi=150)
    plt.close()

# Function to extract local maximum in a sector
def find_local_max(data,lat,lon,corners):
    llat,ulat,llon,rlon = corners
    if rlon > 180.0:
        rlon = 180-rlon
    majour = lat>llat
    minor = lat<ulat
    if ulat>llat:
        dLat = np.logical_and(majour,minor)
    else:
        dLat = np.logical_or(majour,minor)
    majour = lon>llon
    minor = lon<rlon
    if rlon>llon:
        dLon = np.logical_and(majour,minor)
    else:
        dLon = np.logical_or(majour,minor)
    idx = np.logical_and(dLat,dLon)
    datar=data[idx]
    return datar.max()
    
def extract_grib_data(gribfile):
    grbs=pygrib.open(gribfile)
    grb = grbs.message(1)
    data = grb.data()[0]
    lat = grb.data()[1]
    lon = grb.data()[2]
    grbs.close()
    return data,lat,lon

## --- PLOT DATA YEARLY
fend=filend[0]
grib=folder[0:-1]+fend
data,lat,lon = extract_grib_data(grib)
print('year ',data.max())
for zone in zones.keys():
    figname='Yearly/'+zone+'.png'
    title='Lightning intensity year'
    #maxvalue = 80
    year_maxvalue[zone] = find_local_max(data,lat,lon,zones[zone])
    plot_map(data=data,lon=lon,lat=lat,corners=zones[zone],
             savename=figname,titleplot=title,topvalue=year_maxvalue[zone])
             
    #year_maxvalue[zone] = find_local_max(data,lat,lon,zones[zone])
    dataN = data/year_maxvalue[zone]
    plot_map(data=dataN,lon=lon,lat=lat,corners=zones[zone],
             savename='Yearly/'+zone+'NORM.png',
             titleplot=title,
             colorlabel='Relative frequency to year max',
             topvalue=1.0)
    

#%%

## --- PLOT DATA MONTHLY

file_list = glob(folder+'??'+fend)
for grib in file_list:

    cut1 = len(folder)
    cut2 = len(fend)
    mm = grib[cut1:-cut2]
    data,lat,lon = extract_grib_data(grib)
    print(mm,data.max())

    maxvalue = 16
    for zone in zones.keys():
        maxv = find_local_max(data,lat,lon,zones[zone])
        figname='Zones_monthly/'+mm+zone+'.png'
        title='Lightning intensity '+zone+' '+months[mm]
        plot_map(data=data,lon=lon,lat=lat,corners=zones[zone],
                 savename=figname,titleplot=title,topvalue=maxv)
                 
        data_norm = data/maxv
        plot_map(data=data_norm,lon=lon,lat=lat,corners=zones[zone],
                 savename='Zones_monthly/'+mm+zone+'NormMonth.png',
                 titleplot=title,
                 colorlabel='Relative frequency to month max',
                 topvalue=1.0)
             
        data_nory = data/year_maxvalue[zone]
        plot_map(data=data_nory,lon=lon,lat=lat,corners=zones[zone],
                 savename='Zones_monthly/'+mm+zone+'NormYear.png',
                 titleplot=title,
                 colorlabel='Relative frequency to year max',
                 topvalue=maxv/year_maxvalue[zone])
        

## --- PLOT DATA USA YEARLY
USA_corners=[15,55,-125,-60]

fend=filend[1]
grib=folder[0:-1]+fend[1:]
data,lat,lon = extract_grib_data(grib)
print('year ',data.max())

title='Lightning intensity USA yearly'
figname='Yearly/USAyearly.png'
maxvalue = 3000
maxUSA = find_local_max(data,lat,lon,USA_corners)
plot_map(data=data,lon=lon,lat=lat,corners=USA_corners,
         savename=figname,titleplot=title,topvalue=maxUSA)

dataN = data/maxUSA
plot_map(data=dataN,lon=lon,lat=lat,corners=USA_corners,
         savename='Yearly/USAyearlyNORM.png',
         titleplot='Normalized '+title,
         colorlabel='Relative frequency',
         topvalue=1.0)
         
## --- PLOT DATA USA MONTHLY

file_list = glob(folder+'??'+fend)
for grib in file_list:
    cut1 = len(folder)
    cut2 = len(fend)
    mm = grib[cut1:-cut2]
    print(mm)
    data,lat,lon = extract_grib_data(grib)
    
    figname='USA_monthly/USA'+mm+'.png'
    title='Lightning intensity USA '+months[mm]
    maxvalue = 900
    maxv = find_local_max(data,lat,lon,USA_corners)
    
    plot_map(data=data,lon=lon,lat=lat,corners=USA_corners,
             savename=figname,titleplot=title,topvalue=maxv)
    
    data_norm = data/maxv
    plot_map(data=data_norm,lon=lon,lat=lat,corners=USA_corners,
             savename='USA_monthly/USA'+mm+'NormMonth.png',
             titleplot='Norm Month'+title,
             colorlabel='Relative frequency',
             topvalue=1.0)

    data_nory = data/maxUSA
    plot_map(data=data_nory,lon=lon,lat=lat,corners=USA_corners,
             savename='USA_monthly/USA'+mm+'NormYear.png',
             titleplot='Norm Year '+title,
             colorlabel='Relative frequency',
             topvalue=maxv/maxUSA)






