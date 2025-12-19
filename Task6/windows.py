import numpy as np
import math

class Windows:
  def __init__(self):
    pass
  
  def get_window_params(self, stop_attenuation):
    if stop_attenuation <= 21:
      return 'rectangular', 0.9
    elif stop_attenuation <= 53:
      return 'hamming', 3.3
    elif stop_attenuation <= 75:
      return 'blackman', 5.5

  def generate_window(self, window_type, N):
    if window_type == 'rectangular':
      return self._rectangular_window(N)
    elif window_type == 'hamming':
      return self._hamming_window(N)
    elif window_type == 'blackman':
      return self._blackman_window(N)

  def _rectangular_window(self, N):
    return np.ones(N)

  def _hamming_window(self, N):
    w = np.zeros(N)
    for n in range(N):
      n_centered = n - (N - 1) / 2
      w[n] = 0.54 + 0.46 * math.cos(2 * math.pi * n_centered / (N - 1))
    return w
    
  def _blackman_window(self, N):
    w = np.zeros(N)
    for n in range(N):
      n_centered = n - (N - 1) / 2
      term1 = 0.5 * math.cos(2 * math.pi * n_centered / (N - 1))
      term2 = 0.08 * math.cos(4 * math.pi * n_centered / (N - 1))
      w[n] = 0.42 + term1 + term2
    return w
