import numpy as np
import math
from Task7.windows import Windows

class FIR:
  def __init__(self):
    pass

  @staticmethod
  def fir_lpf(Fs, Fc, transition_band, stop_attenuation):
    # Adjust cutoff freq
    Fc_adjusted = Fc + transition_band / 2

    # Normalize cutoff freq
    fc = Fc_adjusted / Fs   # MUST be between 0 and 0.5
    
    delta_f = transition_band / Fs
    window = Windows()
    window_params = window.get_window_params(stop_attenuation)
    window_type = window_params[0]
    C = window_params[1]
    # Compute filter length N
    N = math.ceil(C / delta_f)

    # N must be odd

    if N % 2 == 0:
      N += 1
    

    h_ideal = np.zeros(N)

    M = (N - 1) // 2

    for n in range(N):
      if n == M:
        # avoid division by zero
        h_ideal[n] = 2 * fc
      else:
        h_ideal[n] = math.sin(2 * math.pi * fc * (n - M)) / (math.pi * (n - M))

    # Choose Window
    w = window.generate_window(window_type, N)

    # Apply it here
    h = h_ideal * w

    return h

  @staticmethod
  def fir_hpf(Fs, Fc, transition_band, stop_attenuation):
    # Adjust cutoff freq
    Fc_adjusted = Fc - transition_band / 2

    # Normalize cutoff freq
    fc = Fc_adjusted / Fs   
    
    # Compute transition width
    delta_f = transition_band / Fs
    window = Windows()
    window_params = window.get_window_params(stop_attenuation)
    window_type = window_params[0]
    C = window_params[1]
    # Compute filter length N
    N = math.ceil(C / delta_f)

    # N must be odd
    if N % 2 == 0:
      N += 1
    
    h_ideal = np.zeros(N)

    M = (N - 1) // 2

    for n in range(N):
      if n == M:
        h_ideal[n] = 1 - 2 * fc
      else:
        h_ideal[n] = -math.sin(2 * math.pi * fc * (n - M)) / (math.pi * (n - M))

    # Choose Window
    w = window.generate_window(window_type, N)

    # Apply it here
    h = h_ideal * w

    return h


  @staticmethod
  def fir_band_pass(Fs, F1, F2, transition_band, stop_attenuation):

    fc1 = (F1 - transition_band / 2) / Fs
    fc2 = (F2 + transition_band / 2) / Fs

    # 2. Compute Filter Length (N)
    delta_f = transition_band / Fs
    window = Windows()
    window_type, C = window.get_window_params(stop_attenuation)
    
    N = math.ceil(C / delta_f)
    if N % 2 == 0: N += 1

    # 3. Compute Ideal Impulse Response
    h_ideal = np.zeros(N)
    M = (N - 1) // 2

    for n in range(N):
      if n == M:
        h_ideal[n] = 2 * (fc2 - fc1)
      else:
        term2 = math.sin(2 * math.pi * fc2 * (n - M)) / (math.pi * (n - M))
        term1 = math.sin(2 * math.pi * fc1 * (n - M)) / (math.pi * (n - M))
        h_ideal[n] = term2 - term1

    w = window.generate_window(window_type, N)
    return h_ideal * w

  @staticmethod
  def fir_band_stop(Fs, F1, F2, transition_band, stop_attenuation):
    fc1 = (F1 + transition_band / 2) / Fs
    fc2 = (F2 - transition_band / 2) / Fs

    delta_f = transition_band / Fs
    window = Windows()
    window_type, C = window.get_window_params(stop_attenuation)
    
    N = math.ceil(C / delta_f)
    if N % 2 == 0: N += 1

    h_ideal = np.zeros(N)
    M = (N - 1) // 2

    for n in range(N):
      if n == M:
        h_ideal[n] = 1 - 2 * (fc2 - fc1)
      else:
        term1 = math.sin(2 * math.pi * fc1 * (n - M)) / (math.pi * (n - M))
        term2 = math.sin(2 * math.pi * fc2 * (n - M)) / (math.pi * (n - M))
        h_ideal[n] = term1 - term2

    w = window.generate_window(window_type, N)
    return h_ideal * w


