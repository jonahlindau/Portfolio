% This script calculates release probabilities at each time step from each synapse in response to 5ms sound whose pressure level is defined by dB (in decibels) as an input. 
% The simulation starts and ends with 5ms long 0dB sound. 
% To calculate the probabilities, the model from "Steadman MA and Sumner CJ (2018) Changes in Neuronal Representations of Consonants in the Ascending Auditory System and Their Role in Speech Recognition. Front. Neurosci. 12:671. doi: 10.3389/fnins.2018.00671" is used. See https://zenodo.org/record/1345757#.X8aHLdNKhTY for the original version of the model implementation. 
% The output is a 63 (21 channels x 3 types)-by-15000 (number of timesteps) array (probs_*dB.mat)

function calcReleaseProbsLoop(dB1,dB2,dB3) %input dBs

addpath (['.' filesep 'neural-representations-of-speech-master/Scripts/Auditory Nerve Model']);

paramnames={'GP_LSR','GP_MSR','GP_HSR'};  %low, medium and high spontaneous rate synapses (aka HT, MT and LT) 
BF=round(greenwood(21,1000,8000)); %define the frequencies of channels based on greenwood function
% BF=round(greenwood(21,5600,32000)); %define the frequencies of channels based on greenwood function
freq=[1966 4920 7265];  %sound frequency in Hz
dB=[0,dB1,dB2,dB3];
snr = 0.1;

save('BF.mat','BF')
for freqloop=1:1:3
    figure;

    for dbloop_i=1:1:4
    
        for dbloop_f=2:1:4
                
            %define timestep based on the sound frequency
            fs=freq(freqloop)*1000;
            % dt=1/fs; 
            dt=1/10000000;
            dtname=strcat('timestep.mat');
            save(dtname,'dt')
            
            %start the simulation with 1ms 0dB sound
            time1=dt:dt:0.001;
            signal1=zeros(length(time1));
            sig1=signal1(1,:);
            
            %10ms sound stimulus
            dur=0.005;    %duration of sound stimulus in seconds
            time2=time1(end)+dt:dt:time1(end)+dur;
            signal2=sum(sin(2*pi*freq(freqloop)*(time2-0.0035)), 1);
            sig2=setleveldb(signal2,dB(dbloop_f)); 
            
            
            %end the simulation with 1ms 0dB sound
            time3=time2(end)+dt:dt:time2(end)+0.001;
            signal3=zeros(length(time3));
            sig3=signal3(1,:);

            
            %combine time and signal vectors
            time=[time1,time2,time3];
            
           
            S = RandStream('mt19937ar','Seed',5489);
            sig_w_awgn = awgn(sig2,snr,'measured',S,'linear');
            
%             tryce=setleveldb(sig_w_awgn,dB(dbloop_f));
%             plot(tryce);

            att=setleveldb(sig_w_awgn-sig2,dB(dbloop_i));
            wn=[sig1,att,sig3];
            sig=[sig1,sig2,sig3];
            sig_awgn = [sig1,sig2+att,sig3];

            if dbloop_i == 1
                fhnewsig = zeros(1,length(wn)/2);
                sig_awgn=sig;
            else
                fhnewsig=wn(1:length(wn)/2);
            end

            sig_halves=[fhnewsig,sig_awgn((length(wn)/2)+1:end)];
            
            save(strcat('wn_sig.mat'),'wn');
            
            subplot(4,3,(dbloop_f-1)+3*(dbloop_i-1));
            plot(time*1000,sig_halves);
            title(strcat(num2str(freq(freqloop)),' Hz, ',num2str(dB(dbloop_i)),'dB Noise | ',num2str(dB(dbloop_f)),'dB Sound'));
            xlabel('Time (ms)');
            ylabel('Signal');
            
            ANprob_halves=zeros(length(BF)*length(paramnames),length(time));
            
            for y=1:numel(paramnames)
              modeldata_halves=runmodel_prob(sig_halves,fs,BF,paramnames{y});
              z=length(BF)*y;
              ANprob_halves(z-(length(BF)-1):z,:)=modeldata_halves;
            end
            
            probname_halves=strcat('probs_',num2str(dB(dbloop_i)),'i',num2str(dB(dbloop_f)),'f_dB_',num2str(freq(freqloop)),'Hz_halves.mat');
            save(probname_halves,'ANprob_halves')
        
        end
    end
end    

end

