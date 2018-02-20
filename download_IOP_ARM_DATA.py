# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 13:47:41 2017

@author: dori
"""

import urllib.request as req
import os
datafolder = '/data/optimice/scattering_databases/ARM_aydin_GMM/Aggregates/'
version = '20171207'
list_of_files = datafolder + 'ListOfASMfilenames_' + version + '.txt'

filelist = open(list_of_files,'r')
listlines = filelist.readlines()

urlbase = 'http://iop.archive.arm.gov/arm-iop-file/0pi-data/aydin/Aggregates/AmplitudeScatteringMatrices/'

for line in listlines:
    if '.nc' in line:
        filename = line.split()[-1]
        print(filename)
        url = urlbase + filename
        savefile = datafolder+'AmplitudeScatteringMatrices/'+filename
        if os.path.isfile(savefile):
            print(savefile+' DONE')
        else:
            req.urlretrieve(url,savefile)