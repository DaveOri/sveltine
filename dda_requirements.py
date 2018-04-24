# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 16:15:09 2017

@author: dori
"""

import numpy as np
import matplotlib.pyplot as plt

def mem(np,nx,N,Nr):
    return (288.+384.*np/nx+192/np)*N+463*Nr

D = np.linspace(0.1,20,1000)
d = 0.02 # mm = 20 micron
nd = D/d
N = (nd*nd*nd*0.6).astype(int)
npr = 32
nx = nd
mass = 8.9e-5*D**2.1
Nr=1
M = mem(npr,nx,N,Nr)*1e-9

plt.figure()
ax = plt.gca()
ax.loglog(D,M,label='total')
ax.loglog(D,M/(nd/5.0).astype(int),label='per cpu')
axt = ax.twinx()
axt.plot(D,(nd/10.0).astype(int),c='g',label='# of cpu')
ax.legend()
axt.legend(loc=4)
ax.set_xlim([0,20])
ax.set_ylim([0,200])
ax.set_xlabel('Particle size    [mm]')
ax.set_ylabel('Memory requirement   [GB]')
axt.set_ylabel('Number of cpu')
plt.grid()
plt.savefig('/home/dori/memory.png',dpi=600)

proc = [12,12,12,28,28,24,24,30,30,36,36,128]
time = [171206,165266,161195,61618,55447,92689,84562,55376,60124,50214,48214,10000]

plt.figure()
plt.scatter(proc,np.array(time)/3600.)
plt.xlabel('Number of parallel cores   [#]')
plt.ylabel('Total wall time   [hours]')
plt.grid()
plt.savefig('/home/dori/scaling.png')

cores = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,12,12,12,10,4,12,12,24,24,24,12,12,12,12,256,256,12,36,24,30,36,30,12,30,30]
tt = [18,50,115,234,438,1421,1513,1976,4256,6182,7186,10522,12139,11008,12846,19021,24808,9244,20401,14921,24518,53180,27565,30247,11476,35491,34420,41731,82818,113334,138581,10231,11977,117419,177154,58067,60374,128395,126635,126167,135842,150247]
dim = [0.4,0.6,0.8,1,1.2,1.5,1.6,1.8,2,2.3,2.4,2.5,2.7,2.8,3.,3.2,3.6,3.7,4.,4.1,4.4,4.6,4.8,5.1,5.2,5.4,5.7,6.1,6.7,7.4,7.6,8.1,8.6,9.,9.6,10.,10.9,11.5,11.9,12.6,13.,14.4,15.1]
dim = dim[:len(tt)]
corehrs = np.multiply(np.array(cores),np.array(tt)/3600)
plt.figure()
plt.semilogy(dim,corehrs)
plt.xlabel('Particle size [mm]')
plt.ylabel('corehours')
plt.grid()
plt.savefig('/home/dori/corehours.png')
print(corehrs.sum())

fig, ax = plt.subplots()
ind = [1,2]
ax.bar(ind,[697.0*64,791.16*128])
ax.set_xticks(ind)
ax.set_xticklabels(['4 full nodes', 'many more'],label='corehours')
ax.set_ylabel('coreseconds')
ax.legend()
plt.savefig('/home/dori/node_efficiency.png')

fig, ax = plt.subplots()
ind = [1,2]
compute=[697.0,791.16]
queue=[7000.3,200.1]
p1 = ax.bar(ind,compute)
p2 = ax.bar(ind,queue,bottom=compute)
ax.set_xticks(ind)
ax.set_xticklabels(['4 full nodes', 'scheduler nodes'])
ax.set_ylabel('time [s]')
ax.legend((p1[0],p2[0]),('compute','queue'))
plt.savefig('/home/dori/node_performance.png')