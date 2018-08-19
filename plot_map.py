from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

# Map edges #
llon=-90	# left longitude
rlon=-75	# right longitude
llat=20		# lower latitude
ulat=35		# upper latitude

# Labels #
titlestring = 'This is a map'
savestring = 'savefigure.png' # change to .eps .pdf or whatever to change file format

# Create DATA to plot#
nlats = 180;
nlons = 360;
delta = 2.*np.pi/(nlons-1)

lats = (0.5*np.pi-delta*np.indices((nlats,nlons))[0,:,:])
lons = (delta*np.indices((nlats,nlons))[1,:,:])

wave = 0.75*(np.sin(2.*lats)**8*np.cos(4.*lons))
mean = 0.5*np.cos(2.*lats)*((np.sin(2.*lats))**2 + 2.)
values = wave+mean

LONS = lons*180/np.pi - 180
LATS = lats*180/np.pi

# MAPPING #
plt.figure()
m = Basemap(projection='mill',lat_ts=10,llcrnrlon=llon, urcrnrlon=rlon,
                      llcrnrlat=llat,urcrnrlat=ulat, resolution='i')

m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(-90.,120.,5.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,5.),labels=[0,0,0,1])
m.drawcountries()
m.drawstates()

x,y = m(LONS,LATS)
#ticks=np.linspace(0,1,11)
cs = m.contourf(x,y,values)#,levels=ticks)
cbar = plt.colorbar(cs,orientation='vertical')#,ticks=ticks)
plt.title(titlestring)
plt.savefig(savestring,dpi=300)
plt.close()
