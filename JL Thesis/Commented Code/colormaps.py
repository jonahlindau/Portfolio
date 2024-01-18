
#creates color maps for width, delay, and peak of convolutions, compares all simulations (dB combinations)

#this code is pretty clunky and hard-coded

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap
import random
import os
from os import path
import matplotlib.font_manager
import sys

first_db=['0','30','50','70'] #list of initial dBs
second_db=['30','50','70']    #list of final dBs
freq=str(sys.argv[1])
length_Lu_max=['10.0','20.0'] #list of Lu max lengths
data=[]

path=os.getcwd()


viridis = mpl.colormaps['viridis'].resampled(256)

def plot_examples(colormaps,data,label):
    """
    Helper function to plot data with associated colormap.
    """

    fig, axs = plt.subplots(figsize=(4, 3), layout='constrained', squeeze=False)
    for [ax, cmap] in zip(axs.flat, colormaps):
        # if (l+1)%3==0:
        #     psm = ax.pcolormesh(data, cmap=cmap, rasterized=True)
        # else:
        #     psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmax=vmax[l])
        psm = ax.pcolormesh(data, cmap=cmap, rasterized=True)

        cbar = fig.colorbar(psm, ax=ax)
        cbar.set_label(str(label), rotation=270, fontsize = 12, labelpad=18)

    # plt.title(str(everything_titles[l])+' '+str(freq)+'Hz',fontsize = 18)
    plt.title(str(stdevs_titles[i])+' '+str(freq)+'Hz',fontsize=18)
    plt.xlabel('Sound dB',fontsize = 15)
    plt.ylabel('Noise dB',fontsize = 15)
    xaxis=plt.gca()
    xaxis.set_xticks(np.arange(0.5,3,1))
    xaxis.set_xticklabels([30,50,70])
    yaxis=plt.gca()
    yaxis.set_yticks(np.arange(0.5,4,1))
    yaxis.set_yticklabels([0,30,50,70])

    # plt.savefig(path+'/Colormaps/'+str(everything_str[l])+'_'+str(freq)+'Hz_colormap.png')
    plt.savefig(path+'/Colormaps/'+str(stdevs_str[i])+'_'+str(freq)+'Hz_colormap.png',bbox_inches='tight')


for g in length_Lu_max:
    # for freq in freqs:
    delay=np.load(path+'/mean_delay_'+freq+'_Hz_'+g+'Lhmax.npy')
    peak=np.load(path+'/mean_peaks_'+freq+'_Hz_'+g+'Lhmax.npy')
    width=np.load(path+'/mean_widths_'+freq+'_Hz_'+g+'Lhmax.npy')
    delay_stdev=np.load(path+'/stdev_delay_'+freq+'_Hz_'+g+'Lhmax.npy')
    peak_stdev=np.load(path+'/stdev_peaks_'+freq+'_Hz_'+g+'Lhmax.npy')
    width_stdev=np.load(path+'/stdev_widths_'+freq+'_Hz_'+g+'Lhmax.npy')
    delay=delay.reshape((4,3))
    peak=peak.reshape((4,3))
    width=width.reshape((4,3))
    delay_stdev=delay_stdev.reshape((4,3))
    peak_stdev=peak_stdev.reshape((4,3))
    width_stdev=width_stdev.reshape((4,3))



    width[peak<10]=0
    delay[peak<10]=0
    if g =='10.0':
        delay_norm=delay
        peak_norm=peak
        width_norm=width
        delay_normstdev=delay_stdev
        peak_normstdev=peak_stdev
        width_normstdev=width_stdev
    if g =='20.0':
        delay_hhl=delay
        peak_hhl=peak
        width_hhl=width
        delay_hhlstdev=delay_stdev
        peak_hhlstdev=peak_stdev
        width_hhlstdev=width_stdev

peak_difference=peak_norm-peak_hhl
print(peak_difference)
delay_difference=delay_norm-delay_hhl
width_difference=width_norm-width_hhl
delaymin=delay_difference.min()
widthmin=width_difference.min()

if np.any(width_hhl==0) & np.any(delay_hhl==0):
    indices=np.where(width_hhl==0)
    width_difference[indices]=widthmin-0.01
    indices_d=np.where(delay_hhl==0)
    delay_difference[indices_d]=delaymin-0.01

delay_dif_stdev=np.load(path+'/difstdev_delay_'+freq+'Hz_Lumax.npy')
width_dif_stdev=np.load(path+'/difstdev_widths_'+freq+'Hz_Lumax.npy')
peak_dif_stdev=np.load(path+'/difstdev_peaks_'+freq+'Hz_Lumax.npy')
delay_dif_stdev=delay_dif_stdev.reshape((4,3))
width_dif_stdev=width_dif_stdev.reshape((4,3))
peak_dif_stdev=peak_dif_stdev.reshape((4,3))


array=[]

everything=[peak_norm,peak_hhl,peak_difference,delay_norm,delay_hhl,delay_difference,width_norm,width_hhl,width_difference]
stdevs=[peak_normstdev,peak_hhlstdev,peak_dif_stdev,delay_normstdev,delay_hhlstdev,delay_dif_stdev,width_normstdev,width_hhlstdev,width_dif_stdev]
everything_str=['peak_norm','peak_hhl','peak_difference','delay_norm','delay_hhl','delay_difference','width_norm','width_hhl','width_difference']
stdevs_str=['peak_normstdev','peak_hhlstdev','peak_difference_stdev','delay_normstdev','delay_hhlstdev','delay_difference_stdev','width_normstdev','width_hhlstdev','width_difference_stdev']
everything_titles=['Normal Peaks','HHL Peaks','Peak Difference','Normal Delay','HHL Delay','Delay Difference','Normal Width','HHL Width','Width Difference']
stdevs_titles=['Normal Peaks Stdev','HHL Peaks Stdev','Peak Difference Stdev','Normal Delay Stdev','HHL Delay Stdev','Delay Difference Stdev','Normal Width Stdev','HHL Width Stdev','Width Difference Stdev']

colorbar_labels=['Voltage ('+r'$\mu$'+'V)','Voltage ('+r'$\mu$'+'V)','Voltage ('+r'$\mu$'+'V)','Time (ms)','Time (ms)','Time (ms)','Time (ms)','Time (ms)','Time (ms)']
colorbar_labels_stdevs=['Voltage ('+r'$\mu$'+'V)','Voltage ('+r'$\mu$'+'V)','Voltage ('+r'$\mu$'+'V)','Time (ms)','Time (ms)','Time (ms)','Time (ms)','Time (ms)','Time (ms)']
vmax=[350,350,130,2,2,1.4,2.7,2.7,2]

newcolors = viridis(np.linspace(0,1,256))
black=np.array([0,0,0,1])
# newcolors[:1,:] = black
cmap = ListedColormap(newcolors)

# for l in range(len(everything)):
#     plot_examples([cmap],everything[l],colorbar_labels[l])
for i in range(len(stdevs)):
    plot_examples([cmap],stdevs[i],colorbar_labels[i])


