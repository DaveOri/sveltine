# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 18:00:40 2017

@author: dori
"""

from mpl_toolkits.basemap import Basemap, cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pygrib
from sklearn.cluster import DBSCAN

from scipy.spatial import ConvexHull, Delaunay
#import networkx as nx

from glob import glob

def plot_map(limits, lons, lats, values,title,save,clinear=True,topvalue=None):
    llat,ulat,llon,rlon = limits
    
    plt.figure()
    m = Basemap(projection='mill',lat_ts=10,llcrnrlon=llon, urcrnrlon=rlon,
                          llcrnrlat=llat,urcrnrlat=ulat, resolution='i')
    
    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
    m.drawmeridians(np.arange(-180.,180.,5.),labels=[0,0,0,1])
    m.drawcountries()
    m.drawstates()
    
    if lons[0,0] > 180:
        lons= lons - 360.0
    
    x,y = m(lons,lats)
    if not topvalue:
        if clinear:
            topvalue = 2
            clevs = np.linspace(0,topvalue,201)
            cs = m.contourf(x,y,values,clevs,cmap=cm.s3pcpn)
            colorlabel=' '
        else:
            topvalue = 10
            clevs = np.linspace(0,topvalue,201)
            cs = m.contourf(x,y,values,clevs,cmap=cm.s3pcpn)
            colorlabel='Flashes km$^{-2}$'
    else:
        ticks=np.linspace(0,topvalue,11)
        cs = m.contourf(x,y,values,levels=ticks)
        colorlabel = 'Lightning probability'
    ticks=np.linspace(0,topvalue,11)
    cbar = plt.colorbar(cs,orientation='vertical',ticks=ticks)
    cbar.set_label(colorlabel)
    plt.title(title)
    plt.savefig(save,dpi=300)
    plt.show()
    #plt.close()
    #return m
    
def sq_norm(v): #squared norm 
    return np.linalg.norm(v)**2
    
def circumcircle(points,simplex):
    A=[points[simplex[k]] for k in range(3)]
    M=[[1.0]*4]
    M+=[[sq_norm(A[k]), A[k][0], A[k][1], 1.0 ] for k in range(3)]
    M=np.asarray(M, dtype=np.float32)
    S=np.array([0.5*np.linalg.det(M[1:,[0,2,3]]), -0.5*np.linalg.det(M[1:,[0,1,3]])])
    a=np.linalg.det(M[1:, 1:])
    b=np.linalg.det(M[1:, [0,1,2]])
    return S/a,  np.sqrt(b/a+sq_norm(S)/a**2) #center=S/a, radius=np.sqrt(b/a+sq_norm(S)/a**2)

def get_alpha_complex(alpha, points, simplexes):
    #alpha is the parameter for the alpha shape
    #points are given data points 
    #simplexes is the  list of indices in the array of points 
    #that define 2-simplexes in the Delaunay triangulation

    return filter(lambda simplex: circumcircle(points,simplex)[1]<alpha, simplexes)

def Plotly_data(points, complex_s):
    #points are the given data points, 
    #complex_s is the list of indices in the array of points defining 2-simplexes(triangles) 
    #in the simplicial complex to be plotted
    X=[]
    Y=[]
    for s in complex_s:
        X+=[points[s[k]][0] for k in [0,1,2,0]]+[None]
        Y+=[points[s[k]][1] for k in [0,1,2,0]]+[None]
    return X,Y


    
Florida = [24.0,33.0,-88.0,-79.0]
llat, ulat, llon, rlon = Florida

folder = 'TS_grid/'
filelist = glob(folder + '*.grb')
for filename in filelist[45:46]:
#for filename in filelist[9:10]:
    datestr = filename[len(folder):-len('.grb')]
#filename = folder + datestr + '.grb'

    grb = pygrib.open(filename)
    prob,lats,lons = grb.message(1).data()
    if lons[0,0] > 180:
        lons = lons - 360.0
    titlestring = 'Prob '
    savestring = folder + 'prob.eps'
    plot_map(limits=Florida,lons=lons,lats=lats,values=prob,title=titlestring,save=savestring,clinear=True,topvalue=1)
    grb.close()
    
    #latarr = lats.flatten()
    #lonarr = lons.flatten()
    #probarr = prob.flatten()
    
    data = pd.DataFrame()
    data['prob'] = prob.flatten()
    data['lats'] = lats.flatten()
    data['lons'] = lons.flatten()
    data = data[data['lats']<ulat]
    data = data[data['lats']>llat]
    data = data[data['lons']<rlon]
    data = data[data['lons']>llon]
    dataint = data[data['prob'] > 0.65].drop('prob',axis=1)
    db = DBSCAN(eps=30/6371., min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(dataint))
    
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    
    plt.figure()
    m = Basemap(projection='mill',lat_ts=10,llcrnrlon=-83, urcrnrlon=rlon,
                          llcrnrlat=24,urcrnrlat=28, resolution='h')
    m.drawcoastlines(linewidth=0.5)
    m.drawparallels(np.arange(-90.,120.,1.),labels=[1,0,0,0])
    m.drawmeridians(np.arange(-180.,180.,1.),labels=[0,0,0,1])
    m.drawcountries()
    m.drawstates()
    
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    
    filepoly = folder + datestr + '.vtx'
    fil = open(filepoly,'w')
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'
    
        class_member_mask = (labels == k)
    
        xy = dataint.values[class_member_mask & ~core_samples_mask]
        #plt.plot(xy[:, 1], xy[:, 0], 'o', markerfacecolor=col,
        #         markeredgecolor='k', markersize=3)
        x,y = m(xy[:, 1], xy[:, 0])
        #print(x,y)
        m.plot(x,y,'v', markerfacecolor=col,markeredgecolor='k', markersize=5)
    
        xy = dataint.values[class_member_mask & core_samples_mask]
        #plt.plot(xy[:, 1], xy[:, 0], 'o', markerfacecolor=col,
        #         markeredgecolor='k', markersize=6)
        x,y = m(xy[:, 1], xy[:, 0])
        #print(x,y)
        m.plot(x,y,'v', markerfacecolor=col,markeredgecolor='k', markersize=10)
                 
        # From clusters extrapolate the Convex Hull
        #print(k,len(xy))
        if len(xy)>2:
            if len(xy)==3:
                hull = ConvexHull(xy,qhull_options="QJ")
                for simplex in hull.simplices:
                    #plt.plot(xy[simplex, 1], xy[simplex, 0], 'b-')
                    x,y = m(xy[simplex, 1], xy[simplex, 0])
                    m.plot(x,y,'b-')
                fil.write(str(xy[hull.vertices].flatten())[2:-2]+'\n')
                
            else:
                tri = Delaunay(xy)
                alpha_complex=get_alpha_complex(0.15, xy, tri.simplices)
                X,Y = Plotly_data(xy, alpha_complex)
                #plt.plot(Y,X,'b-')
                Xre = []
                Yre = []
                for i in range(len(X)):
                    if X[i]:
                        Xre.append(X[i])
                        Yre.append(Y[i])
                        if X[i+1]:
                            xd = int(X[i])
                            xm = int(round((X[i]%1)*60))
                            yd = int(Y[i])
                            ym = int(round((Y[i]%1)*60))
                            if X[i]>=0:
                                xs='N'+str(abs(xd)).zfill(2)+str(abs(xm)).zfill(2)
                            else:
                                xs='S'+str(abs(xd)).zfill(2)+str(abs(xm)).zfill(2)
                            if Y[i]>=0:
                                ys='E'+str(abs(yd)).zfill(3)+str(abs(ym)).zfill(2)
                            else:
                                ys='W'+str(abs(yd)).zfill(3)+str(abs(ym)).zfill(2)
                            fil.write(xs+','+ys+',')
                    else:
                        fil.write('\n')
                        x,y=m(Yre,Xre)
                        m.plot(x,y,'b-')
                        Xre=[]
                        Yre=[]
            
    #plt.xlim([llon, rlon])
    #plt.ylim([llat, ulat])
    orlando=[28.43,-81.31]
    miami=[25.79,-80.29]
    tampa=[27.98,-82.53]
    fl=[26.0075,-80.1528]
    canc=[21.0367,-86.8769]
    #xa,ya = m([orlando[1],miami[1],tampa[1],fl[1],canc[1]],[orlando[0],miami[0],tampa[0],fl[0],canc[0]])
    xa,ya = m([orlando[1],miami[1],tampa[1],canc[1]],[orlando[0],miami[0],tampa[0],canc[0]])
    #m.scatter(xa,ya,29,marker='o',color='y')
    m.plot(xa,ya,'go',markersize=10)
    bound = np.array([[27,-82.5],[26.5,-80.25],[25.75,-80.35],[24.5,-81.25],[27,-82.5]])
    xp,yp=m(bound[:,1],bound[:,0])
    m.plot(xp,yp,'m-',markersize=4,linewidth=5)
    xl,yl=m(-80.3898,25.8)
    m.plot(xl,yl,'xr',markersize=20,mew=10)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()
    
    fil.close()
