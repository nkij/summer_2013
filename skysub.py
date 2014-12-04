########################################################
#skysub.py (original ratio-1.py)
#This program reads in target and sky (fits) files, calculate the average flux at specific wavelengths from both files and compute the ratio.
#Then the program divides the input sky spectrum to this ratio to make it equal to the target spectrum. Finally, this program will subtract sky off the target.
#Use when the target file contains no pure sky
#INPUT: 1.(FITTED) SKY SPECTRUM 2.TARGET SPECTRUM
#OUTPUT: 1.SKY-SUBTRACTED TARGET SPECTRUM
########################################################

#modules

import scipy
import numpy as np
import pyfits as pf
import matplotlib.pyplot as plt
import math as mt
#from pyraf import iraf


#Target Global Vaiables

hdulist_tg = pf.open('mask1-16.0002.fits')
hdr_tg = hdulist_tg[0].header
flux_tg = hdulist_tg[0].data
crval_tg = hdr_tg['CRVAL1']				#Starting wavelength 
cdel_tg = hdr_tg['CDELT1']				#Wavelength axis width
wave_tg = crval_tg + np.arange(len(flux_tg))*cdel_tg	#Create an x-axis
wavelist = [6257.427,6287.316,6307.049,6392.598,6386.544,6498.745,6533.141,6554.000,6562.407,6577.130,6596.863]

fluxtgvalues = np.interp(wavelist, wave_tg, flux_tg)	#wave_tg and flux_tg has to have the same dimension -- can't trim wave_tg
print "the target fluxes ="
print fluxtgvalues


#Sky Global Variables
hdulist_sky = pf.open('sksfitmask1sci16ap2.fits')
hdr_sky = hdulist_sky[0].header
flux_sky = hdulist_sky[0].data
crval_sky = hdr_sky['CRVAL1']				#starting wavelength of sky
cdel_sky = hdr_sky['CDELT1']				#wavelength axis width of sky
x = 6000-crval_sky	
wave_sky = (crval_sky + x) + np.arange(len(flux_sky))*cdel_sky	#+x to correct the axis offset

#Retrieve sky flux at specific wavelength
fluxskyvalues = np.interp(wavelist, wave_sky, flux_sky)
print "The sky fluxes ="
print fluxskyvalues					#an array of fluxes

ratio = np.divide(fluxskyvalues,fluxtgvalues)
print "flux_sky/flux_target ="
print ratio

#average the ratio
ratio_add = np.sum(ratio)
ratio_ave = ratio_add/len(ratio)
print "the average value of ratio is"
print ratio_ave

#Divide the whole sky spectrum with 'ratio' 
flux_sky_div = flux_sky/ratio_ave
print ("The sky/ratio values are ")
print flux_sky_div

#trim the target spectrum to match the sky
a = np.array(wave_tg)
a_trim = wave_sky

print "wave_tg"
print wave_tg
print "wave_sky"
print wave_sky
print "wave_tg_trim"
print a_trim

flux_trim = np.interp(a_trim, wave_tg, flux_tg)


#Subtraction (Target-Sky)
flux_tg_final = np.subtract(flux_trim,flux_sky_div)
print "flux_trim - flux_sky_div ="
print flux_tg_final


#plots
plt.plot(a_trim,flux_trim)
plt.show()

#plt.plot(wave_sky,flux_sky)
#plt.show()

#plt.plot(wave_tg,flux_tg)
#plt.show()

plt.plot(wave_sky,flux_sky_div)
plt.show()

plt.plot(a_trim,flux_tg_final)
plt.show()


#Save finalflux[mask]-[sci]-[aperture]
hdulist_tg.writeto('finalflux1-16-2.fits')

#Finish. Close both files
hdulist_tg.close()
hdulist_sky.close()
