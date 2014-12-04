#vmap.py
#This program will plot Ha, NII, and OI position-velocity map 
#Start with Ha

import pyfits as pf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random
import pylab

mdflist = pf.open('GN2010BQ056-03.fits')	
mdf = mdflist[1].data

vradec = np.loadtxt('vradec.txt', usecols = (0,1,2))
gradec = np.loadtxt('gradec.txt', usecols = (1,2))

ra = vradec[:,1]
dec = vradec[:,2]
v = vradec[:,0]

rag = gradec[:,0]
decg = gradec[:,1]


ax = plt.axes()

# Pull up the image
#plt.figure()
#im = Image.open('tree_small.png')
#plt.imshow(im, origin='lower')

# pick a colormap
cmap = plt.get_cmap('jet')
norm = plt.normalize(min(v), max(v))

# put points for each observation (no colouring)
ax.scatter(ra, dec, s=50, c=v, marker = 'o', cmap = cm.jet )
ax.scatter(rag, decg, s=50, marker = '+')

# create a mappable suitable for creation of a colorbar
mappable = cm.ScalarMappable(norm, cmap)
mappable.set_array(v)

# create the colorbar
cb = plt.colorbar(mappable)    
cb.set_label('Velocity (km/s)')

# Axes titles
plt.title("H-alpha colormap")
plt.xlabel('X')
plt.ylabel('Y')

ax.invert_xaxis()
plt.show()
