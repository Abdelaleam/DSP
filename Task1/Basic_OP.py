import numpy as np
import matplotlib.pyplot as plt


class basic_op:
    def __init__(self,signal):
        self.signal = np.array(signal,dtype=int)
    @classmethod
    def read_signal(cls, path):
        signal = np.loadtxt(path, skiprows=3)
        return cls(signal)
    def save_signal(self,path):
        with open(path,"w")as f:
            f.write("0\n")
            f.write("0\n")
            f.write(f"{len(self.signal)}\n")
            for row in self.signal:
                index,value=row
                f.write(f"{int(index)} {value:}\n")
    def add_signals(self, other):
        unique_indicies = np.union1d(self.signal[:, 0], other.signal[:, 0])
        res = np.zeros((len(unique_indicies), 2))
        res[:, 0] = unique_indicies
        for s in [self.signal, other.signal]:
            for row in s:
                index, value = row  
                exist = res[:, 0] == index
                res[exist, 1] += value
        return basic_op(res)
    def multiply(self,c):
        new_signal=self.signal.copy()
        new_signal[:,1]*=c
        return basic_op(new_signal)
    def sub_signals(self,other):
        return self.add_signals(other.multiply(-1))
    def delay_signal(self,c):
        new_signal=self.signal.copy()
        new_signal[:,0]-=c
        return basic_op(new_signal)
    def folding(self):
        new_signal=self.signal.copy()
        new_signal[:,0]=-new_signal[:,0]
        new_signal=new_signal[::-1]
        return basic_op(new_signal)
    def visualize(self, ax=None, title="Signal"):
        show_fig = False
        if ax is None:
            fig, ax = plt.subplots(figsize=(10, 5))
            show_fig = True
        X = self.signal[:, 0]
        Y = self.signal[:, 1]
        ax.stem(X, Y, linefmt='b-', markerfmt='ro', basefmt='p-')
        ax.set_title(title)
        ax.set_xlabel("t")
        ax.set_ylabel("f(t)")
        ax.grid(True, alpha=0.3)
        if show_fig:
            plt.show()

    def __str__(self):
        return str(self.signal)
    
