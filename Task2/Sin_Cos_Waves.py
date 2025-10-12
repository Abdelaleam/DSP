from enum import Enum
import numpy as np
import matplotlib.pyplot as plt

class waves(Enum):
    Sin = 'sin'
    Cos = 'cos'

class Waves:
    @staticmethod
    def Gen_sin_cos(signal: waves, Amp, Freq, Theta):
        #n
        domain = np.arange(0, 1, 0.001)
        if signal == waves.Sin:
            Y = Amp * np.sin(2 * np.pi * Freq * domain + Theta)
        elif signal == waves.Cos:
            Y = Amp * np.cos(2 * np.pi * Freq * domain + Theta)
        else:
            Y = np.array([])
            domain = np.array([])
        return domain, Y

    @staticmethod
    def Sampling(signal: waves, Amp, Freq, Fs, Theta=0):
        # n
        domain = np.arange(0, 1, 1 / Fs)
        if signal == waves.Sin:
            Y = Amp * np.sin(2 * np.pi * Freq * domain + Theta)
        elif signal == waves.Cos:
            Y = Amp * np.cos(2 * np.pi * Freq * domain + Theta)
        else:
            Y = np.array([])
            domain = np.array([])
        return domain, Y


