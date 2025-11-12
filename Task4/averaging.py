import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Task1 import basic_op
import numpy as np


class AveragingWindow:
  @staticmethod
  def average(signal, window_size):
    result_dict = {}
    for i in range(len(signal)):
      n, x = signal[i]
      window = signal[i : i + window_size]
      if len(window) < window_size:
        break
      avg_value = sum([val for idx, val in window]) / window_size
      result_dict[n] = round(avg_value, 3)
    result_items = sorted(result_dict.items())
    result_array = np.array(result_items, dtype=float)
    return basic_op(result_array)
  
if __name__ == "__main__":
  signal = basic_op.read_signal(r"Task4\Signal1.txt")
  averaged_signal = AveragingWindow.average(signal.signal, window_size=5)
  print("Averaged Signal:")
  print(averaged_signal)

      