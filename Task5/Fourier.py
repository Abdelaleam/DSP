import sys, os

# Add parent directory (Tasks folder) to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Task1 import basic_op
import numpy as np
import math


class Fourier:
    @staticmethod
    def DFT(signal,fs=None):
        amplitudes=[]
        phases=[]
        N=len(signal)
        for k in range(N):
            res=0
            for n in range(N):
                exp_term= -2j * math.pi * k * n / N
                res+= signal[n]*np.exp(exp_term)
            amplitudes.append(abs(res))
            phases.append(np.angle(res))
        # if fs:
        #     freq_bins=[k*fs/N for k in range(N)]
        #     return freq_bins,amplitudes,phases
        return amplitudes,phases
    @staticmethod
    def IDFT(amplitudes,phases):
        N=len(amplitudes)
        signal=[]
        for n in range(N):
            res=complex(0,0)
            for k in range(N):
                adj=amplitudes[k]*math.cos(phases[k])
                opp=amplitudes[k]*math.sin(phases[k])
                xk=complex(adj,opp)
                exp_term= 2j * math.pi * k * n / N
                res+= xk * np.exp(exp_term)
            res=res/N
            signal.append(round(res.real))
        return signal
    
    
    
def main():
    signal=basic_op.read_signal(r"D:\Abdelaleam\Courses\New folder\DSP\Tasks\Task5\input_Signal_DFT.txt")
    amplitudes,phases=Fourier.DFT(signal.signal[:,1])
    print("DFT Amplitudes:")
    print(amplitudes)
    print("DFT Phases:")
    print(phases)
    signal2=basic_op.read_signal(r"D:\Abdelaleam\Courses\New folder\DSP\Tasks\Task5\input_Signal_IDFT.txt")
    rec_signal=Fourier.IDFT(signal2.signal[:,0],signal2.signal[:,1])
    print("Reconstructed Signal from IDFT:")
    print(rec_signal)


if __name__ == "__main__":
    main()