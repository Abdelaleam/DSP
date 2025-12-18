import numpy as np
import math
from windows import Windows

class FIR:
  def __init__(self):
    pass

  @staticmethod
  def fir_lpf(Fs, Fc, transition_band, stop_attenuation):
    # Adjust cutoff freq
    Fc_adjusted = Fc - transition_band / 2

    # Normalize cutoff freq
    fc = Fc_adjusted / Fs   # MUST be between 0 and 0.5
    
    # Compute transition width
    delta_f = transition_band / Fs

    # Compute filter length N

    N = math.ceil(3.3 / delta_f)

    # N must be odd

    if N % 2 == 0:
      N += 1
    
    # Compute impulse response

    h_ideal = np.zeros(N)

    M = (N - 1) // 2

    for n in range(N):
      if n == M:
        # avoid division by zero
        h_ideal[n] = 2 * fc
      else:
        h_ideal[n] = math.sin(2 * math.pi * fc * (n - M)) / (math.pi * (n - M))

    # Choose Window
    window = Windows()
    w = window.choose_window(stop_attenuation, N)

    # Apply it here
    h = h_ideal * w

    return h


