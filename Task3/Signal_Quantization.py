import numpy as np
import matplotlib.pyplot as plt
class quantization:
    def __init__(self,signal):
        self.signal = np.array(signal,dtype=float)
    @classmethod
    def read_signal(cls, path):
        signal = np.loadtxt(path, skiprows=3)
        return cls(signal)

    @staticmethod
    def quantize_signal(signal,num_levels=0, num_bits=0):
        y=signal[:,1]
        x=signal[:,0]
        if(num_bits==0 and num_levels==0):
            print('Error! ,You should wirte #OfLevels Or #Bits')
        if(num_bits!=0):
            num_levels=2**num_bits
        min_val=np.min(y)
        max_val=np.max(y)
        delta=(max_val-min_val)/num_levels
        ranges=np.arange(min_val, max_val + delta, delta)
        midpoints=(ranges[:-1]+ranges[1:])/2
        range_indices=np.digitize(y,ranges,right=True)
        range_indices=np.clip(range_indices,1,num_levels)
        q_y=midpoints[range_indices-1]
        q_error=q_y-y
        avg_power_err=np.mean(q_error**2)
        if(num_bits==0):
            num_bits = int(np.ceil(np.log2(num_levels)))    
        encoded_index = [format(index - 1, f'0{num_bits}b') for index in range_indices]
        encoded_result = np.column_stack((encoded_index, q_y))
        return x,y,q_y,q_error,avg_power_err,encoded_result,range_indices,delta
   