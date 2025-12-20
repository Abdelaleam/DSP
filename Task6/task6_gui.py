import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Task1 import basic_op
import io
from Task6.Correlation import Correlation

current_dir = os.path.dirname(os.path.abspath(__file__))
compare_signal_path = os.path.join(current_dir, "Correlation Task Files", "Point1 Correlation")
if compare_signal_path not in sys.path:
    sys.path.append(compare_signal_path)

try:
    import CompareSignal  # type: ignore
except ImportError:
    print(f"Warning: Could not import CompareSignal from {compare_signal_path}")
    CompareSignal = None

class Task6GUI:
    def __init__(self, root, home):
        self.home = home
        self.root = tk.Toplevel(root)
        self.root.title("Task 6 - Correlation & Time Delay")
        self.root.configure(bg="#2c3e50")
        self.root.geometry("1400x900")
        self.root.protocol("WM_DELETE_WINDOW", self.back_to_home)

        self.signal1 = None
        self.signal2 = None
        self.fs_var = tk.DoubleVar(value=100.0)
        self.result_signal = None
        
        self.class1_path = None
        self.class2_path = None

        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill="both", expand=True, padx=8, pady=8)

        left_frame = tk.Frame(main_frame, bg="#2c3e50", width=320)
        left_frame.pack(side="left", fill="y", padx=(6, 12), pady=6)
        left_frame.pack_propagate(False)

        right_frame = tk.Frame(main_frame, bg="#2c3e50")
        right_frame.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        ttk.Label(left_frame, text="Signal 1", font=("Arial", 11, "bold"),
                  background="#2c3e50", foreground="white").pack(anchor="w", pady=(8, 2), padx=8)
        ttk.Button(left_frame, text="Load Signal 1", command=self.load_signal_1).pack(fill="x", padx=8, pady=4)

        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=8, padx=8)

        ttk.Label(left_frame, text="Signal 2", font=("Arial", 11, "bold"),
                  background="#2c3e50", foreground="white").pack(anchor="w", pady=(8, 2), padx=8)
        ttk.Button(left_frame, text="Load Signal 2", command=self.load_signal_2).pack(fill="x", padx=8, pady=4)

        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=8, padx=8)

        ttk.Label(left_frame, text="Sampling Frequency (Hz):", background="#2c3e50", foreground="white").pack(anchor="w", padx=8)
        ttk.Entry(left_frame, textvariable=self.fs_var).pack(fill="x", padx=8, pady=(2, 8))

        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=8, padx=8)
        ttk.Label(left_frame, text="Correlation Ops", font=("Arial", 11, "bold"),
                  background="#2c3e50", foreground="white").pack(anchor="w", pady=(8, 2), padx=8)
        
        ttk.Button(left_frame, text="Compute Correlation", command=self.compute_correlation).pack(fill="x", padx=8, pady=6)
        ttk.Button(left_frame, text="Time Delay Analysis", command=self.compute_time_delay).pack(fill="x", padx=8, pady=6)
        ttk.Button(left_frame, text="Compare Result", command=self.compare_result).pack(fill="x", padx=8, pady=6)
        
        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=8, padx=8)
        ttk.Label(left_frame, text="Classification", font=("Arial", 11, "bold"),
                  background="#2c3e50", foreground="white").pack(anchor="w", pady=(8, 2), padx=8)
        
        ttk.Button(left_frame, text="Select Class 1 Folder", command=self.select_class1_folder).pack(fill="x", padx=8, pady=4)
        ttk.Button(left_frame, text="Select Class 2 Folder", command=self.select_class2_folder).pack(fill="x", padx=8, pady=4)
        ttk.Button(left_frame, text="Classify Signal 1", command=self.classify_signal_1).pack(fill="x", padx=8, pady=6)


        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=8, padx=8)
        ttk.Button(left_frame, text="Clear Plots", command=self.clear_plots).pack(fill="x", padx=8, pady=6)

        ttk.Button(left_frame, text="Back to Home", command=self.back_to_home).pack(side="bottom", fill="x", padx=8, pady=8)

        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(10, 9))
        self.fig.tight_layout(pad=3)
        self._style_plots(self.fig, [self.ax1, self.ax2, self.ax3])

        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.clear_plots()

    def _style_plots(self, fig, axes):
        for ax in axes:
            ax.grid(True, alpha=0.3)
            ax.set_facecolor("#34495e")
            ax.tick_params(colors="white")
            ax.title.set_color("white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('white')
        fig.patch.set_facecolor("#2c3e50")

    def _reset_axes(self):
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self._style_plots(self.fig, [self.ax1, self.ax2, self.ax3])
        
        self.ax1.set_title("Signal 1")
        self.ax1.set_xlabel("Sample Index")
        self.ax1.set_ylabel("Amplitude")

        self.ax2.set_title("Signal 2")
        self.ax2.set_xlabel("Sample Index")
        self.ax2.set_ylabel("Amplitude")

        self.ax3.set_title("Correlation Result")
        self.ax3.set_xlabel("Lag Index")
        self.ax3.set_ylabel("Correlation")

    def clear_plots(self):
        self.signal1 = None
        self.signal2 = None
        self.result_signal = None
        self._reset_axes()
        self.canvas.draw()

    def load_signal_1(self):
        path = filedialog.askopenfilename(title="Select Signal 1 File", filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        try:
            self.signal1 = basic_op.read_signal(path)
            self._plot_signal(self.ax1, self.signal1, "Signal 1", color='cyan')
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Signal 1: {e}")

    def load_signal_2(self):
        path = filedialog.askopenfilename(title="Select Signal 2 File", filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        try:
            self.signal2 = basic_op.read_signal(path)
            self._plot_signal(self.ax2, self.signal2, "Signal 2", color='magenta')
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Signal 2: {e}")
    
    def select_class1_folder(self):
        path = filedialog.askdirectory(title="Select Class 1 Folder")
        if path:
            self.class1_path = path
            messagebox.showinfo("Selected", f"Class 1 Folder selected:\n{os.path.basename(path)}")
            
    def select_class2_folder(self):
        path = filedialog.askdirectory(title="Select Class 2 Folder")
        if path:
            self.class2_path = path
            messagebox.showinfo("Selected", f"Class 2 Folder selected:\n{os.path.basename(path)}")

    def _plot_signal(self, ax, sig_obj, title, color='b'):
        ax.clear()
        self._style_plots(self.fig, [ax])
        ax.set_title(title)
        
        if hasattr(sig_obj, 'signal'):
            data = np.array(sig_obj.signal)
            if data.ndim > 1 and data.shape[1] >= 2:
                x = data[:, 0]
                y = data[:, 1]
                ax.stem(x, y, linefmt=color, markerfmt=color[0]+'o', basefmt='white')
            else:
                ax.stem(data, linefmt=color, markerfmt=color[0]+'o', basefmt='white')
        else:
            ax.stem(sig_obj, linefmt=color, markerfmt=color[0]+'o', basefmt='white')

    def compute_correlation(self):
        if self.signal1 is None or self.signal2 is None:
            messagebox.showwarning("Missing Data", "Please load both Signal 1 and Signal 2.")
            return

        try:
            s1 = [float(val) for val in np.array(self.signal1.signal)[:, 1]]
            s2 = [float(val) for val in np.array(self.signal2.signal)[:, 1]]

            corr_values = Correlation.direct_correlation(s1, s2)
            self.result_signal = corr_values

            self.ax3.clear()
            self._style_plots(self.fig, [self.ax3])
            self.ax3.set_title("Normalized Cross-Correlation")
            self.ax3.set_xlabel("Lag")
            self.ax3.set_ylabel("Normalized Amplitude")
            
            x_indices = np.arange(len(corr_values))
            
            self.ax3.stem(x_indices, corr_values, linefmt='yellow', markerfmt='yo', basefmt='white')
            
            self.canvas.draw()
            messagebox.showinfo("Success", "Correlation computed successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Correlation failed: {e}")

    def compute_time_delay(self):
        if self.signal1 is None or self.signal2 is None:
            messagebox.showwarning("Missing Data", "Please load both Signal 1 and Signal 2.")
            return

        try:
            fs = self.fs_var.get()
            if fs <= 0:
                raise ValueError("Fs must be > 0")

            s1 = [float(val) for val in np.array(self.signal1.signal)[:, 1]]
            s2 = [float(val) for val in np.array(self.signal2.signal)[:, 1]]

            delay = Correlation.time_delay_analysis(s1, s2, fs)
            
            messagebox.showinfo("Time Delay Analysis", f"Estimated Time Delay: {delay} seconds\n(Lag: {int(delay * fs)} samples)")

        except Exception as e:
            messagebox.showerror("Error", f"Time Delay Analysis failed: {e}")

    def compare_result(self):
        if self.result_signal is None:
            messagebox.showwarning("Missing Data", "Please compute correlation first.")
            return

        if CompareSignal is None:
            messagebox.showerror("Error", "CompareSignal script not found.")
            return

        path = filedialog.askopenfilename(title="Select Expected Output File (Signal)", filetypes=[("Text Files", "*.txt")])
        if not path:
            return

        try:
            indices = list(range(len(self.result_signal)))
            samples = self.result_signal

            captured_output = io.StringIO()
            sys.stdout = captured_output

            try:
                CompareSignal.Compare_Signals(path, indices, samples)
            except Exception as inner_e:
                print(f"\nError during comparison: {inner_e}")
            finally:
                sys.stdout = sys.__stdout__

            output_msg = captured_output.getvalue()
            if "Test case passed successfully" in output_msg:
                 messagebox.showinfo("Comparison Result", output_msg)
            else:
                 messagebox.showwarning("Comparison Result", output_msg)

        except Exception as e:
            sys.stdout = sys.__stdout__
            messagebox.showerror("Error", f"Comparison failed: {e}")

    def classify_signal_1(self):
        if self.signal1 is None:
            messagebox.showwarning("Missing Siganl", "Please load Signal 1 (Test Signal).")
            return
        if not self.class1_path or not self.class2_path:
            messagebox.showwarning("Missing Folders", "Please select both Class 1 and Class 2 folders.")
            return

        try:
            s1 = [float(val) for val in np.array(self.signal1.signal)[:, 1]]
            result = Correlation.classify_signal(s1, self.class1_path, self.class2_path)
            messagebox.showinfo("Classification Result", f"Signal 1 is classified as:\n\n{result}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Classification failed: {e}")

    def back_to_home(self):
        self.root.destroy()
        self.home.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    class MockHome:
        def __init__(self):
            self.root = root
    
    app = Task6GUI(root, MockHome())
    root.withdraw() 
    root.mainloop()
