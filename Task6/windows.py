import numpy as np
import math

class Windows:
  def __init__(self):
    pass

  def choose_window(self, stop_attenuation, N):
    if stop_attenuation <= 21:
        return self._rectangular_window(N)
    elif stop_attenuation <= 53:
        return self._hamming_window(N)

  def _rectangular_window(self, N):
    return np.ones(N)

  def _hamming_window(self, N):
    w = np.zeros(N)
    for n in range(N):
        w[n] = 0.54 - 0.46 * math.cos(2 * math.pi * n / (N - 1))
    return w
