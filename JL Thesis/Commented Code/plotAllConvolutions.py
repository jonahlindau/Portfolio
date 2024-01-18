# encoding=utf8

#This script takes the spike times of an auditory nerve population as an input and convolves the spikes with the unitary response of CAP.
#The output is a figure with simulated CAPs (plot.png)

from __future__ import division
import matplotlib
#matplotlib.use('Agg')
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import random
from scipy.io import loadmat
import os
from os import path
from matplotlib.patches import Rectangle
import sys
import pickle as pl
import matplotlib.font_manager

#Unitary response of CAP from Bourien et al., J Neurophysiol 112: 1025–1039, 2014. (K=1.14815 to simulate a 100uV CAP at 80dB SPL)
def func_conv(t):
    return 1.14815*0.14*np.exp(-1.440*t)*np.sin(2*np.pi*0.994*t)  

currentPath = os.getcwd()

#input parameters
first_spl=[0,30,50,70]    #
second_spl=[30,50,70]
# second_spl=[60]
trial_no=3
length_Lu_max=[10.0, 20.0]
length_Lu_min=[10.0, 10.0]
length_Lh_max=[1.0, 1.0]
length_Lh_min=[1.0, 1.0]
color=["red","blue"]
freq=int(sys.argv[1])
time_all = 7

for first in range(len(first_spl)):
	for second in range(len(second_spl)):
		for g in range(len(length_Lh_min)):

			#start and end times of the simulation
			start = -0.503 #to shift the peak of the unitary response of CAP to 0 ms
			stop = start + time_all
			tstep = loadmat('timestep.mat')['dt'][0][0]*1000
			arraylength = int(time_all/tstep)
			num_timestep = int((stop-start)/tstep)
			t=np.linspace(start,stop,num_timestep)

			convs_all=np.empty((trial_no,arraylength))
			#generate convolution function
			func = np.array([])
			conv_t=3 #damped oscillations are negligible after 3ms
			t1=np.linspace(start,start+conv_t,int(conv_t/tstep))
			for i in t1:
				func = np.append(func,[func_conv(i)])
			x= round(optimize.fmin(lambda x: func_conv(x),0)[0],3)

			for j in range(0,trial_no,1):
				spikes = np.load(currentPath+'/spikes_'+str(first_spl[first])+'i'+str(second_spl[second])+'f_dB_'+str(freq)+'Hz_Lumax'+str(length_Lu_max[g])+'_Lumin'+str(length_Lu_min[g])+'_Lhmax'+str(length_Lh_max[g])+'_Lhmin'+str(length_Lh_min[g])+'.npy',allow_pickle=True)[j]
				spike_times = np.concatenate(spikes)
				spike_times = np.around(np.sort(spike_times,axis = None),decimals=3) #sorted spike times of a population
		#		spike_times = np.array([1.1,3.3,8])
				unique_elements, counts_elements = np.unique(spike_times, return_counts=True) #unique_elements: each unique spike times ; count_elements: how many spikes in the population at each unique spike time
				spike_times=np.asarray((unique_elements, counts_elements))

				spike_array = np.array([])

				#generate an array (spike_array) of length "num_timestep" that shows number of spikes at each time step
				for i in range(len(spike_times[0])):
					if i == 0:
						spike_array = np.append(spike_array,np.zeros([1,int(round((spike_times[0][i]-x)/tstep,0))]))
						spike_array = np.append(spike_array,[spike_times[1][i]])

					else:
						spike_array = np.append(spike_array,np.zeros([1,int(round((spike_times[0][i]-spike_times[0][i-1])/tstep,0))-1]))
						spike_array = np.append(spike_array,[spike_times[1][i]])


				if len(spike_array)< num_timestep:
					spike_array = np.append(spike_array,np.zeros([1,num_timestep-len(spike_array)]))

				#convolve with the unitary response
				conv=np.convolve(spike_array,func)
				convs_all[j]=conv[:arraylength]

				# np.save(currentPath+'/convolution_'+str(j+1)+str(first_spl[first])+'i'+str(second_spl[second])+'f_dB_'+str(freq)+'_Hz.npy',conv)
		        
				# t=np.linspace(0-0.503,time_all-0.503,arraylength)
				# plt.plot(t,convs_all[j],linewidth=2)
				# plt.show()
				# import pdb; pdb.set_trace()

			#calculate avg and standard error of CAPs
			conv_avg=np.average(convs_all,axis=0)
			conv_sterr=np.std(convs_all,axis=0)/np.sqrt(trial_no)

			# Plot simulated CAPs
			if path.exists("plot.pickle"):
				fig=pl.load(open('plot.pickle','rb'))
			else:
				fig=plt.figure(figsize=(4.5,2.5),layout='constrained')
				ax=fig.add_axes([0.13,0.16,0.83,0.8])
				ax.tick_params(right="off",top="off")

				plt.rcParams['mathtext.default'] = "regular"
				plt.xlabel('Time (ms)',fontsize=16,labelpad=0)
				plt.ylabel('Voltage ('+r'$\mu$'+'V)',fontsize=16,labelpad=2)
				xmin=0
				xmax=7
				plt.xlim(xmin, xmax)
				pf=Rectangle((1,-410),2.5,20,facecolor='gray',edgecolor='None')
				ax.add_patch(pf)
				plt.text(2,-408,'Noise only',fontsize=15,color='w')
				pe=Rectangle((3.5,-410),2.5,20,facecolor='green',edgecolor='None')
				ax.add_patch(pe)
				plt.text(4.2,-408,'Sound with Noise',fontsize=15,color='w')
				plt.ylim(-410,65)
				plt.tick_params(labelsize=10)

			t=np.linspace(0-0.503,7-0.503,arraylength)
			plt.plot(t,conv_avg,linewidth=2,color=color[g])
			plt.fill_between(t,conv_avg-conv_sterr,conv_avg+conv_sterr,linewidth=0,alpha=0.3,facecolor=color[g])
			pl.dump(fig,open('plot.pickle','wb'))
			plt.savefig(currentPath+'/new_convolution_'+str(first_spl[first])+'i'+str(second_spl[second])+'f_dB_'+str(freq)+'_Hz.png',dpi=300)
			np.save(currentPath+'/new_convolution_'+str(first_spl[first])+'i'+str(second_spl[second])+'f_dB_'+str(freq)+'_Hz.npy',conv_avg)
            
            
            
		os.remove(currentPath+'/plot.pickle')
