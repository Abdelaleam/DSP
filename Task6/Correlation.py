import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Task1 import basic_op
import numpy as np
import math
class Correlation:
    @staticmethod
    def direct_correlation(signal1,signal2):
       N1=len(signal1)
       N2=len(signal2)
       if N1!=N2:
           raise ValueError("Signals must be of the same length for direct correlation.")
       norm_factor = math.sqrt(np.sum(np.array(signal1)**2) * np.sum(np.array(signal2)**2))
       res_values = []
       N = N1
       for j in range(N):
           acc = 0.0
           for i in range(N):
               acc += signal1[i] * signal2[(i + j) % N]
           res_values.append(acc / norm_factor)
       return res_values
    @staticmethod
    def time_delay_analysis(signal1, signal2, Fs):
        corr = Correlation.direct_correlation(signal1, signal2)
        max_index = np.argmax(corr)
        return max_index / Fs
    # helper function
    def get_avg_max_corr(signal, class_path):
        files = [os.path.join(class_path, f) for f in os.listdir(class_path) if f.endswith('.txt')]
        max_corrs = []
        for f in files:
            s = basic_op.read_signal(f).signal[:,1]
            corr = Correlation.direct_correlation(signal, s)
            max_corrs.append(max(corr))
        return np.mean(max_corrs) if max_corrs else 0
    @staticmethod
    def classify_signal(test_signal, class1_path, class2_path):
        avg1 = Correlation.get_avg_max_corr(test_signal, class1_path)
        avg2 = Correlation.get_avg_max_corr(test_signal, class2_path)
        print(f"Avg Corr Class 1: {avg1}")
        print(f"Avg Corr Class 2: {avg2}")
        if avg1 > avg2:
            return "Class 1"
        elif avg2 > avg1:
            return "Class 2"
        else:
            return "Undecided"
        