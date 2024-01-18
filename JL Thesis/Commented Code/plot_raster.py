import numpy as np
import matplotlib.pyplot as plt
import sys
import os

#Load the file with spike time information for raster plot
#spikes=np.load('/Users/maralbudak/Desktop/recover/Documents/ZochowskiLab/MSOpaper/data/anf0_Lu10.0_1channels_800Hz_65dB_100ms_right.npy',allow_pickle=True)



first_spl=int(sys.argv[1])
second_spl=int(sys.argv[2])
trials_tot=3
length_Lu_max=float(sys.argv[3])
length_Lu_min=float(sys.argv[4])
length_Lh_max=float(sys.argv[5])
length_Lh_min=float(sys.argv[6])
freq=1966       #Sound signal frequency

path = os.getcwd()

spikes=np.load('spikes_'+str(first_spl)+'i'+str(second_spl)+'f_dB_'+str(freq)+'Hz_Lumax'+str(length_Lu_max)+'_Lumin'+str(length_Lu_min)+'_Lhmax'+str(length_Lh_max)+'_Lhmin'+str(length_Lh_min)+'.npy',allow_pickle=True)


#number of neurons whose spikes are recorded 
new = spikes[1]

nrOfNeurons = len(new)


plt.rcParams.update({'font.size': 22})
plt.figure(figsize=(10,6))


for i in range(nrOfNeurons):
	spk=new[i]
	plt.plot(spk,[i]*len(spk),'ko')

plt.xlim(0,7)
plt.ylim(0,6400)
if length_Lu_max == length_Lu_min:
	plt.title(str(freq)+"Hz – "+str(first_spl)+"dB Noise, "+str(second_spl)+"dB Sound, Lu = "+str(length_Lu_min))

else:
	plt.title(str(freq)+"Hz – "+str(first_spl)+"dB Noise "+str(second_spl)+"dB Sound, Lu Max = "+str(length_Lu_max)+", Lu Min = "+str(length_Lu_min)+", Lh = 1")

plt.xlabel('Time (ms)')
plt.ylabel('SGN ID')
plt.show()
