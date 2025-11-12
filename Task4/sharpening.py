import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Task1 import basic_op
import numpy as np

class Sharpening:
  @staticmethod
  def sharpen(signal, first_deriv):
    if first_deriv:
      result_dict = {}
      for index, row in enumerate(signal):
        n, x = row
        i_n_minus_1 = Sharpening._findIndex(n - 1, signal)
        if i_n_minus_1 == -1:
          continue
        x_n = x
        x_n_minus_1 = signal[i_n_minus_1][1]
        result_dict[n - 1] = x_n - x_n_minus_1
      result_items = sorted(result_dict.items())    
      result_array = np.array(result_items)
      return basic_op(result_array)
    else:
      result_dict = {}
      for index, row in enumerate(signal):
        n, x = row
        i_n_minus_1 = Sharpening._findIndex(n - 1, signal)
        i_n_plus_1 = Sharpening._findIndex(n + 1, signal)
        if i_n_minus_1 == -1 or i_n_plus_1 == -1:
          continue
        n, x = row
        x_n = x
        x_n_minus_1 = signal[i_n_minus_1][1]
        x_n_plus_1 = signal[i_n_plus_1][1]
        result_dict[n - 1] = x_n_plus_1 - 2 * x_n + x_n_minus_1
      result_items = sorted(result_dict.items())    
      result_array = np.array(result_items)
      return basic_op(result_array)
    
  @staticmethod
  def _findIndex(index, signal):
      for i, row in enumerate(signal):
        n, x = row
        if n == index:
          return i
      return -1
    

def main():
  signal = basic_op.read_signal(r"Task4\Signal1.txt")
  sharpened_signal = Sharpening.sharpen(signal.signal, first_deriv=True)
  print("Sharpened Signal (First Derivative):")
  print(sharpened_signal)

if __name__ == "__main__":
  main()