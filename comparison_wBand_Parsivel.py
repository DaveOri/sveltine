# -*- coding: utf-8 -*-
#%matplotlib inline

import matplotlib.pyplot as plt
import itertools
from matplotlib.ticker import MultipleLocator
from matplotlib.offsetbox import AnchoredText
from matplotlib.legend import Legend
import matplotlib.gridspec as gridspec
import netCDF4 as nc
from netCDF4 import Dataset
import numpy as np
import math
import pandas as pd
from datetime import datetime, timedelta
import os
import gzip
import csv
from collections import defaultdict
from csv import DictReader
import scipy.integrate as integrate


from copy import deepcopy
import string 

def calcPosition(val, xMin, xMax):
    decVal = (val - xMin)/(xMax - xMin)
    return decVal

def plot_W_Band(data, plotId, figTitle, plot):

    data=data[start:end]
    epoch = pd.datetime(2001, 1, 1, 0, 0, 0)
    newTimes = np.array(data.index, np.float64)
    legend = np.arange(1,11) * (newTimes[-1] - newTimes[0])/10
    legend = legend+newTimes[0]
    legendDate = epoch + pd.to_timedelta(legend)
    date=legendDate[0].date().strftime('%Y.%m.%d')

    X,Y = np.meshgrid(newTimes, data.columns)
    dataToPlot = np.array(data[start:end])
    dataToPlot = np.ma.masked_invalid(dataToPlot)

    plt.figure(figsize=(15,6))
    plt.pcolormesh(X,Y,dataToPlot.T,vmin=-15, vmax=30, cmap='jet')
    plt.ylim(height[0], height[1])
    plt.xticks(legend,legendDate.strftime('%H:%M:%S'), rotation=0)
    plt.ylabel('height [$m$]',fontsize=18)
    plt.title(figTitle+' '+strDate, fontsize=18)
    plt.colorbar().set_label('[dBZ]', fontsize=18)
    plt.grid()

    if plot == True: 
        out = plotId+'_'
        plt.savefig(out+figTitle+'.png', format='png', dpi=200,bbox_inches='tight')
        print out+figTitle+'.png'

    plt.show()

def plotPARS(data, plotId,figTitle, plot): 
    # add after plot to run anywhere besides jupyter: ,start, end):

    #data=data[start:end] #figure out how to implement different start and end times!! 
    epoch = pd.datetime(1970, 1, 1)
    newTimes = np.array(data.index, np.float64)
    legend = np.arange(1,11) * (newTimes[-1] - newTimes[0])/10
    legend = legend+newTimes[0]
    legendDate = epoch + pd.to_timedelta(legend)
    date=legendDate[0].date().strftime('%Y.%m.%d')

    plt.figure(figsize=(15,8))
    plt.plot(newTimes, data.Ze) #actually data[start:end]
    plt.ylabel('Ze [dBZ]', fontsize=18)
    plt.xticks(legend,legendDate.strftime('%H:%M:%S'), rotation=0)
    plt.xlim(newTimes[0], newTimes[-1])
    plt.title(figTitle+' '+strDate, fontsize=18)
    plt.legend()
    plt.grid()


    if plot == True: 
        out = plotId+'_'
        plt.savefig(out+figTitle+'.png', format='png', dpi=200,bbox_inches='tight')
        print out+figTitle+'.png'
    plt.show()

#class from Davide Ori
class BinnedPSD():
    """Binned gamma particle size distribution (PSD).

    Callable class to provide a binned PSD with the given bin edges and PSD
    values.

    Args (constructor):
        The first argument to the constructor should specify n+1 bin edges,
        and the second should specify n bin_psd values.

    Args (call):
        D: the particle diameter.

    Returns (call):
        The PSD value for the given diameter.
        Returns 0 for all diameters outside the bins.
    """

    def __init__(self, bin_edges, bin_psd):
        if len(bin_edges) != len(bin_psd)+1:
            raise ValueError("There must be n+1 bin edges for n bins.")

        self.bin_edges = bin_edges
        self.bin_psd = bin_psd

    def psd_for_D(self, D):
        if not (self.bin_edges[0] < D <= self.bin_edges[-1]):
            return 0.0

        # binary search for the right bin
        start = 0
        end = len(self.bin_edges)
        while end-start > 1:
            half = (start+end)//2
            if self.bin_edges[start] < D <= self.bin_edges[half]:
                end = half
            else:
                start = half

        return self.bin_psd[start]

    def __call__(self, D):
        if np.shape(D) == (): # D is a scalar
            return self.psd_for_D(D)
        else:
            return np.array([self.psd_for_D(d) for d in D])

    def __eq__(self, other):
        if other is None:
            return False
        return len(self.bin_edges) == len(other.bin_edges) and \
            (self.bin_edges == other.bin_edges).all() and \
            (self.bin_psd == other.bin_psd).all() 
            
            
            
# Creation of Parsivel class boundaries (class center and class width) and bin edges for PSD calculation
pars_class = np.zeros(shape=(32,2))
bin_edges = np.zeros(shape=(33,1))

#pars_class[:,0] : Center of Class [mm]
#pars_class[:,1] : Width of Class [mm]
pars_class[0:10,1] = 0.125
pars_class[10:15,1] = 0.250
pars_class[15:20,1] = 0.500
pars_class[20:25,1] = 1.
pars_class[25:30,1] = 2.
pars_class[30:32,1] = 3.

j = 0
pars_class[0,0] = 0.062
for i in range(1,32):
    if i < 10 or (i > 10 and i < 15) or (i > 15 and i < 20) or (i > 20 and i < 25) or (i > 25 and i < 30) or (i > 30):
        pars_class[i,0] = pars_class[i-1,0] + pars_class[i,1]

    const = [0.188, 0.375, 0.75, 1.5, 2.5]
    if i == 10 or i == 15 or i == 20 or i == 25 or i == 30:
        pars_class[i,0] = pars_class[i-1,0] + const[j]
        j = j + 1

    #print pars_class[i,0]
    bin_edges[i+1,0] = pars_class[i,0] + pars_class[i,1]/2


bin_edges[0,0] = 0.
bin_edges[1,0] = pars_class[0,0] + pars_class[0,1]/2 



filepath_events = '/home/sschoger/whk/acloud_campaign/absolute_calibration/'

#filename = filepath_events + 'joyrad_rainevents.csv'
filename = filepath_events + 'mirac_rainevents.csv'

events = pd.read_csv(filename)
events

for ii, val in enumerate(events.day):
    #print(ii)
    #-Height definition
    height_bot = 150
    #meheight_top = 400
    height_top = 900

    #-Time definition
    year = str(events.year[ii])
    
    if events.month[ii] < 10:
        month = '0'+str(events.month[ii])
    else:
        month = str(events.month[ii])
    
    if events.day[ii] < 10:
        day = '0'+str(events.day[ii])
    else:
        day = str(events.day[ii])
    
    if events.hour_begin[ii] < 10:
        hourBegin = '0'+str(events.hour_begin[ii])
    else:
        hourBegin = str(events.hour_begin[ii])
    
    if events.hour_end[ii] < 10:
        hourEnd = '0'+str(events.hour_end[ii]-1)
    else:
        hourEnd = str(events.hour_end[ii]-1)
        
    #print(year, month, day, hourBegin, hourEnd)

    #year = '2017' 
    #month = '07'
    #day = '13'

    #hourBegin = '00'
    #hourEnd =  '19'

    minBegin = '00'
    minEnd =  '59'

    secBegin = '00'
    secEnd = '59'

    millisecBegin = '00'
    millisecEnd = '59'

    #-----------------
    strDate = ('').join([year,month,day])

    timeStart = ('').join([hourBegin, minBegin])
    timeEnd = ('').join([hourEnd, minEnd])

    start = pd.datetime(int(year), int(month), int(day),
                        int(hourBegin), int(minBegin),
                        int(secBegin))

    end = pd.datetime(int(year), int(month), int(day),
                      int(hourEnd), int(minEnd), int(secEnd))

    #- Definition of height range to extract the data
    height = (height_bot, height_top)

    fileDate = ('').join([year, month, day])

    heightBot = str(height[0])
    heightTop = str(height[1])
    new_Pars = 'new_Pars'
    plotId = ('_').join([fileDate, timeStart, timeEnd, heightBot, heightTop, new_Pars])
    #print plotId

    #- To save the plots use plot = True
    #plot = False
    plot = True
    #--------------
    
    #path of rain scattering tables
    filepath_rainscat = '/data/optimice/scattering_databases/rain/'
    filename = filepath_rainscat + '0.C_94.0GHz.csv'
	
	#***************************
    #read rain scattering tables into python with pandas as dataframe
    df = pd.read_csv(filename)

    #set header names as variables
    diameter = 'diameter[mm]'
    radarxs = 'radarsx[mm2]'
    wavelength = 'wavelength[mm]'
    temp = 'T[k]'
    extxs = 'extxs[mm2]'

    #constants
    T = df.loc[1,temp]
    wavelen = df.loc[1,wavelength]
    K2 = df.loc[1,'K2']

    #integration constant
    int_const = wavelen**4 / ((math.pi)**5 *K2)

    #variables
    #D = df.loc[:,diameter]
    radar_cross = df.loc[:,radarxs]
    #radar_cross = df.loc[:,diameter]**6.0/int_const

    #ext_cross = df.loc[:,extxs]

    #radar_cross

    #- Parsivel data path
    parsPath = '/data/obs/site/nya/parsivel/l1'
    datePath = ('/').join([year,  month, day])

    strDate = ('').join([year,month,day])

    fileName = 'parsivel_nya_'+strDate+'.nc'
    parsFile = ('/').join([parsPath, datePath, fileName])
    
    #print datePath
    #print strDate 
    #print fileName
    #print parsFile
    #if ii == 0: break

    #Reading the NetCDF File from Parsivel 
    parsNC = Dataset(parsFile, 'r')

    zPar = parsNC.variables['Z'][:]
    tPar = parsNC.variables['time'][:]
    NPar = parsNC.variables['N'][:]
    #nparticl = parsNC.variables['n_particles'][:]

    # Create a DataFrame to look at the Data and to prepare for plot
    epoch = pd.datetime(1970, 1, 1)
    timesPar = epoch + pd.to_timedelta(tPar,'s')

    #parsNC.close()
    parsDataFrame_old = pd.DataFrame(data=zPar,columns=['Ze'], index=timesPar)

	#***************************
    #upscale Parsivel resolution to rain scatterint table resolution
    Z_pars = np.zeros(len(tPar))
    ZD6_pars = np.zeros(len(tPar))
    delta = 0.01
    upscale_end = (len(df)+1.)/100.
    diameter_ups = np.arange(delta,upscale_end,delta)

    for t, val in enumerate(tPar):
        #check where NPar is not NAN to determine class
        #class_num = np.where(np.isnan(NPar[:,t])==False)
        # actual class-number is class_num + 1

        #upscale parsivel resolution - devide NPar by class width in pars_class
        N_ups = (10.0**NPar[:,t])#/pars_class[:,1]

        #convert all nan to zero
        N_ups = np.nan_to_num(N_ups)
        #print(N_ups[:10])
        #PSD = BinnedPSD(bin_edges,NPar[:,t])
        PSD = BinnedPSD(bin_edges,N_ups)

        #calculate upscaled values from parsivel with new radar cross section
        y = PSD(diameter_ups)*df.loc[:,radarxs]
        d6 = PSD(diameter_ups)*df.loc[:,diameter]**6
        #print(y)

        ZD6_pars[t] = d6.sum()*delta#np.trapz(y, dx = delta)
        Z_pars[t] = int_const * y.sum()*delta#np.trapz(y, dx = delta)
        #print(Z[t])

        #if t == 1: break

    Z_pars
    #new = np.where(Z_pars != np.nan)
    #new
    #Z_dbz = 10 * np.log10(Z_pars)
    #Z_dbz.shape

	#***************************
    Ze_Pars_new_dbz = 10 * np.ma.log10(np.abs(Z_pars))
    Ze_Pars_D6_dbz = 10 * np.ma.log10(np.abs(ZD6_pars))
    #Ze_Pars_new_dbz = 10 * np.log10(np.abs(Z_pars))

    print(Ze_Pars_new_dbz)
    Ze_Pars_new_dbz.shape

    parsDataFrame = pd.DataFrame(data=Ze_Pars_new_dbz,columns=['Ze'], index=timesPar)
    D6parsDataFrame = pd.DataFrame(data=Ze_Pars_D6_dbz,columns=['Ze'], index=timesPar)

    #np.where(np.isnan(NPar[:,1]) ==False)

    #plt.plot(tPar, zPar)
    #plt.show()

    #plt.plot(tPar, Ze_Pars_new_dbz)
    #plt.show()

    #Nice Plot
    #plotPARS(parsDataFrame, plotId,'PARSIVEL',  True)

    if year == '2017' and month < '07' or (year == '2017' and month == '07' and day <= '27'):
        W_Band_Path = ('/').join(['/data/obs/site/nya/joyrad94/l1', year, month, day])
        #ncFiles = 'joyrad94_nya_compact_' + year + month + day + '*.nc'

        ncFiles = [f for f in os.listdir(W_Band_Path) if (f.endswith('.nc') and f.startswith('joyrad94_nya_compact_'))]

        label = 'W-Band (Joyrad94)'
        color = 'g'

    if year > '2017' or (month >= '07' and day > '29') or month >= '08':
        W_Band_Path = ('/').join(['/data/obs/site/nya/mirac-a/l1', year, month, day])
        #ncFiles = 'joyrad94_nya_compact_' + year + month + day + '*.nc'

        ncFiles = [f for f in os.listdir(W_Band_Path) if (f.endswith('.nc') and f.startswith('mirac-a_nya_compact_'))]

        label = 'W-Band (Mirac)'
        color = 'b'


    for nn, ncFile in enumerate(ncFiles):
        try:
            ncData = nc.Dataset(W_Band_Path + '/' + ncFile,'r')
        except:
            raise RuntimeError("Could not open file: '" + ncFile+"'")


        keys = ncData.variables.keys()
        needed_keys = ['range', 'time', 'Ze', 'sampleTms']
        n_time = len(ncData.variables['time'])

        #initialize dictionary
        if nn == 0:
            joinedData = {}

        for key in keys:
            if key not in needed_keys:
                continue

            if ncData.variables[key].shape == ():
                data = ncData.variables[key].getValue()
            else:
                data = ncData.variables[key][:]
                shape = data.shape

            #concatenate values of different files
            if nn == 0:
                 joinedData[key] = data
            elif n_time in shape:
                   #print joinedData.keys()
                t_axis = shape.index(n_time)
                joinedData[key] = np.concatenate((joinedData[key],data),axis=t_axis)
            else:
                continue

        ncData.close()
        #if (tmpFile and ncFile.split(".")[-2] == "tmp"):
        #    os.remove(ncFile)


    #print joinedData['Ze'].shape
    #print joinedData['time'].shape

    Ze_W_Band = joinedData['Ze']
    height_W_Band = joinedData['range']
    time_W_Band_secondssince = joinedData['time']
    sample_W_Band = joinedData['sampleTms']


    #convert Ze from mm⁶/m³ into dBZ
    #Ze_joyrad_dbz = []
    Ze_W_Band_dbz = 10 * np.log10(np.abs(Ze_W_Band))

    type(time_W_Band_secondssince)

    #print Ze_joyrad.shape
    #print time_joyrad_secondssince.shape
    #print Ze_joyrad_dbz.shape

    #convert time into UTC
    reference_date = pd.datetime(2001,1,1,0,0,0)
    n_time_vec = len(time_W_Band_secondssince)

    time_W_Band = reference_date + pd.to_timedelta(time_W_Band_secondssince, 'S') + pd.to_timedelta(sample_W_Band, 'ms')
    #print time_joyrad
    #print time_W_Band
    W_Band_DataFrame = pd.DataFrame(index=time_W_Band, columns= height_W_Band, data=Ze_W_Band_dbz)

    #plot_W_Band(W_Band_DataFrame, plotId, label, plot)

    dfSelTime_W_Band = W_Band_DataFrame[start:end]
    dfSelTimeRange_W_Band = dfSelTime_W_Band.transpose()[height[0]:height[1]]
    dfArray_W_Band = np.array(dfSelTimeRange_W_Band.transpose(), np.float)

        # It makes the array one dimensional and
        # removes the nan values 
    dfArrayFlat_W_Band = dfArray_W_Band.flatten()
    dfArrayFlat_W_Band =  dfArrayFlat_W_Band[~np.isnan(dfArrayFlat_W_Band)]

    newParsDF = parsDataFrame[(parsDataFrame.Ze > -40)]
    D6ParsDF = D6parsDataFrame[(D6parsDataFrame.Ze > -40)]
    #parsDataFrame_old=10.0*np.ma.log10(parsDataFrame_old)
    oldParsDF = parsDataFrame_old[(parsDataFrame_old.Ze > -9)]
    #print(newParsDF.Ze)

    med_newpars = np.median(newParsDF.Ze)
    
    med_D6pars = np.median(D6ParsDF.Ze)

    med_oldpars = np.median(oldParsDF.Ze)

    med_WBand = np.median(dfArrayFlat_W_Band)

    diff_newparsW =  med_newpars - med_WBand
    deltaZe_new = np.round(diff_newparsW,1)
    
    diff_oldparsW =  med_oldpars - med_WBand
    deltaZe_old = np.round(diff_oldparsW,1)

    med = [med_oldpars, med_newpars, med_WBand]
    #print(med[1])

    #parsDataFrame.Ze

    ####PLOT
    fig = plt.figure(figsize=(15,6))
    ax = plt.subplot(1,1,1) 

    xmin = -40
    xmax = 50
    
    ymin = 0
    ymax = 0.3

    #alpha = transparency[0,1] 
    n, bins, patches = plt.hist(newParsDF.Ze, 50, 
                               normed=1, facecolor='r',
                               alpha=0.6, label = 'TMM (new Ze)')
                               
    n, bins, patches = plt.hist(D6ParsDF.Ze, 50, 
                               normed=1, facecolor='m',
                               alpha=0.6, label = 'D6 Ze')

    n, bins, patches = plt.hist(oldParsDF.Ze, 50, 
                               normed=1, facecolor='salmon',
                               alpha=0.6, label = 'Parsivel Ze')
                               
        
    n, bins, patches = plt.hist(dfArrayFlat_W_Band, 50, 
                             normed=1, facecolor= color,
                           alpha=0.6, label = label)

    plt.ylabel('PDF', fontsize=18)
    plt.xlabel('Ze [dBZ]', fontsize=18)
    plt.title((' ').join([strDate, start.strftime('%H:%M'), '-',
                          end.strftime('%H:%M'), str(height[0]), '-',
                          str(height[1]),'[m]']), fontsize=18)

    majorLocator = MultipleLocator(5)
    minorLocator = MultipleLocator(2.5)

    ax.xaxis.set_major_locator(majorLocator)

    # for the minor ticks, use no labels; default NullFormatter
    ax.xaxis.set_minor_locator(minorLocator)

    #plt.xticks(np.arange(-50, 35, 5),fontsize=18)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    #plt.ylim(0,ymax)
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.grid(which = 'both')
    first_legend = plt.legend(fontsize=16)
    plt.gca().add_artist(first_legend)

    newpars = ax.axvline(x=med_newpars, ymin= 0, ymax = 1, color = 'r', linewidth = 4, 
               linestyle='dashed',alpha = 0.8, label = 'median TMM = '+ "%5.2f" % med_newpars+' dBZ')

    D6pars = ax.axvline(x=med_D6pars, ymin= 0, ymax = 1, color = 'm', linewidth = 4, 
               linestyle='dashed',alpha = 0.8, label = 'median D6 = '+ "%5.2f" % med_D6pars+' dBZ')
    
    oldpars = ax.axvline(x=med_oldpars, ymin= 0, ymax = 1, color = 'salmon', linewidth = 4, 
               linestyle='dashed',alpha = 0.8, label = 'median Pars = '+ "%5.2f" % med_oldpars+' dBZ')

    Wband = ax.axvline(x=med_WBand, ymin= 0, ymax = 1, color = color, linewidth = 4, 
               linestyle='dashed',alpha = 0.8, label = 'median Mirac = '+ "%5.2f" % med_WBand+' dBZ')

    handles = [newpars, oldpars, Wband]
    
    plt.axhline(y = 0.2, xmin=calcPosition(med_WBand, xmin, xmax), 
                xmax=calcPosition(med_newpars, xmin, xmax), color='k')

    plt.axhline(y = 0.14, xmin=calcPosition(med_WBand, xmin, xmax), 
                xmax=calcPosition(med_oldpars, xmin, xmax), color='k')
    
    plt.text(med_WBand + deltaZe_new/6., 0.21, str(deltaZe_new)+' dB', fontsize=18)
    
    plt.text(med_WBand + deltaZe_old/6., 0.15, str(deltaZe_old)+' dB', fontsize=18)


    #handles, labels = ax.get_legend_handles_labels()
    second_legend = plt.legend(handles = [newpars,D6pars, oldpars, Wband], fontsize=16,loc = 2)
    ax = plt.gca().add_artist(second_legend)
    #ax.add_artist(second_leged)


    #plot=True
    #plot=False

    if plot == True: 
        out = plotId+'_'
        plt.savefig(out+'pdf_analysis_'+str(ii)+'.png', format='png', dpi=200,bbox_inches='tight')
        #print out+'pdf_analysis'+'.png'
    commonIndex = newParsDF.index.intersection(oldParsDF.index)
    plt.figure()
    plt.scatter(oldParsDF.loc[commonIndex],newParsDF.loc[commonIndex],label='TMM',s=2)
    plt.scatter(oldParsDF.loc[commonIndex],D6ParsDF.loc[commonIndex],label='D6',s=1)
    ax=plt.gca()
    ax.set_xlim([-5,35])
    ax.set_ylim([-5,35])
    plt.plot(ax.get_xlim(),ax.get_ylim())
    plt.legend()
    plt.grid()
    plt.xlabel('Parsivel reflectivity  [dBZ]')
    plt.ylabel('Computed reflectivity  [dBZ]')
    plt.savefig(out+'scatter_analysis_'+str(ii)+'.png', format='png', dpi=200,bbox_inches='tight')
    #if ii == 0: break

plt.show()
