import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Task1 import basic_op
import numpy as np


class Convolution:
  @staticmethod
  def convolve(signal_1, signal_2):
    result_dict = {}
    for row1 in signal_1:
      n1, x1 = row1
      for row2 in signal_2:
        n2, x2 = row2
        n = n1 + n2
        x = x1 * x2
        if n in result_dict:
          result_dict[n] += x
        else:
          result_dict[n] = x
    result_items = sorted(result_dict.items())
    result_array = np.array(result_items)
    return basic_op(result_array)
  

def main():
  signal1 = basic_op.read_signal(r"Task4\Signal1.txt")
  signal2 = basic_op.read_signal(r"Task4\Signal2.txt")
  convolved_signal = Convolution.convolve(signal1.signal, signal2.signal)
  print("Convolved Signal:")
  print(convolved_signal)



if __name__ == "__main__":
  main()

