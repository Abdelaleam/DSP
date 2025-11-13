import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys
import os
import importlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Task1 import basic_op
from Task4.averaging import AveragingWindow
from Task4.convolution import Convolution
from Task4.sharpening import Sharpening

# Import test functions
test_module = importlib.import_module('Task4.DSP Task4 TEST functions')
AveragingTest = test_module.AveragingTest
SharpeningTest = test_module.SharpeningTest
ConvolutionTest = test_module.ConvolutionTest
AveragingTest2 = test_module.AveragingTest2
SharpeningTest2 = test_module.SharpeningTest2

class Task4GUI:
    def __init__(self, root, home):
        self.root = tk.Toplevel(root)
        self.root.title("Task 4 - Signal Processing (Averaging, Convolution, Sharpening)")
        self.root.configure(bg="#2c3e50")
        self.root.protocol("WM_DELETE_WINDOW", self.back_to_home)
        self.home = home
        
        # Data storage
        self.avg_signal = None
        self.avg_result = None
        self.avg_window_size = tk.IntVar(value=5)
        
        self.conv_signal1 = None
        self.conv_signal2 = None
        self.conv_result = None
        
        self.sharp_signal = None
        self.sharp_result = None
        self.sharp_mode = tk.BooleanVar(value=True)  # True for first derivative, False for second
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Style the notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#2c3e50", borderwidth=0)
        style.configure("TNotebook.Tab", background="#34495e", foreground="white", 
                       padding=[20, 10], font=('Arial', 11, 'bold'))
        style.map("TNotebook.Tab", background=[("selected", "#1abc9c")])
        
        # Create tabs
        self.create_averaging_tab()
        self.create_convolution_tab()
        self.create_sharpening_tab()
        
        # Back button at bottom
        back_frame = tk.Frame(self.root, bg="#2c3e50")
        back_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(back_frame, text="Back to Home", command=self.back_to_home).pack(side="right")
    
    def create_averaging_tab(self):
        avg_frame = tk.Frame(self.notebook, bg="#2c3e50")
        self.notebook.add(avg_frame, text="Averaging")
        
        # Left panel - Controls
        left_frame = tk.Frame(avg_frame, bg="#2c3e50", width=250)
        left_frame.pack(side="left", fill="y", padx=15, pady=15)
        left_frame.pack_propagate(False)
        
        ttk.Label(left_frame, text="Averaging Controls", font=("Arial", 14, "bold"),
                  foreground="white", background="#2c3e50").pack(pady=10)
        
        ttk.Button(left_frame, text="Upload Signal", command=self.load_avg_signal).pack(fill="x", pady=5)
        
        ttk.Label(left_frame, text="Window Size:", background="#2c3e50", foreground="white").pack(pady=(10, 3))
        window_entry = ttk.Entry(left_frame, textvariable=self.avg_window_size)
        window_entry.pack(fill="x", pady=3)
        
        ttk.Button(left_frame, text="Apply Averaging", command=self.apply_averaging).pack(fill="x", pady=10)
        ttk.Button(left_frame, text="Save Result", command=self.save_avg_result).pack(fill="x", pady=5)
        ttk.Button(left_frame, text="Compare with Test Case 1", command=self.compare_avg_test1).pack(fill="x", pady=5)
        ttk.Button(left_frame, text="Compare with Test Case 2", command=self.compare_avg_test2).pack(fill="x", pady=5)
        
        # Center panel - Plots
        center_frame = tk.Frame(avg_frame, bg="#2c3e50")
        center_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.avg_fig, (self.avg_ax1, self.avg_ax2) = plt.subplots(2, 1, figsize=(8, 6))
        self.avg_fig.tight_layout(pad=3)
        self.avg_canvas = FigureCanvasTkAgg(self.avg_fig, master=center_frame)
        self.avg_canvas.get_tk_widget().pack(fill="both", expand=True)
        self._style_plots(self.avg_fig, [self.avg_ax1, self.avg_ax2])
    
    def create_convolution_tab(self):
        conv_frame = tk.Frame(self.notebook, bg="#2c3e50")
        self.notebook.add(conv_frame, text="Convolution")
        
        # Left panel - Controls
        left_frame = tk.Frame(conv_frame, bg="#2c3e50", width=250)
        left_frame.pack(side="left", fill="y", padx=15, pady=15)
        left_frame.pack_propagate(False)
        
        ttk.Label(left_frame, text="Convolution Controls", font=("Arial", 14, "bold"),
                  foreground="white", background="#2c3e50").pack(pady=10)
        
        ttk.Button(left_frame, text="Upload Signal 1", command=self.load_conv_signal1).pack(fill="x", pady=5)
        ttk.Button(left_frame, text="Upload Signal 2", command=self.load_conv_signal2).pack(fill="x", pady=5)
        
        ttk.Button(left_frame, text="Apply Convolution", command=self.apply_convolution).pack(fill="x", pady=10)
        ttk.Button(left_frame, text="Save Result", command=self.save_conv_result).pack(fill="x", pady=5)
        ttk.Button(left_frame, text="Compare with Test Case", command=self.compare_conv_test).pack(fill="x", pady=5)
        
        # Center panel - Plots
        center_frame = tk.Frame(conv_frame, bg="#2c3e50")
        center_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.conv_fig, (self.conv_ax1, self.conv_ax2, self.conv_ax3) = plt.subplots(3, 1, figsize=(8, 9))
        self.conv_fig.tight_layout(pad=3)
        self.conv_canvas = FigureCanvasTkAgg(self.conv_fig, master=center_frame)
        self.conv_canvas.get_tk_widget().pack(fill="both", expand=True)
        self._style_plots(self.conv_fig, [self.conv_ax1, self.conv_ax2, self.conv_ax3])
    
    def create_sharpening_tab(self):
        sharp_frame = tk.Frame(self.notebook, bg="#2c3e50")
        self.notebook.add(sharp_frame, text="Sharpening")
        
        # Left panel - Controls
        left_frame = tk.Frame(sharp_frame, bg="#2c3e50", width=250)
        left_frame.pack(side="left", fill="y", padx=15, pady=15)
        left_frame.pack_propagate(False)
        
        ttk.Label(left_frame, text="Sharpening Controls", font=("Arial", 14, "bold"),
                  foreground="white", background="#2c3e50").pack(pady=10)
        
        ttk.Button(left_frame, text="Upload Signal", command=self.load_sharp_signal).pack(fill="x", pady=5)
        
        ttk.Label(left_frame, text="Derivative Mode:", background="#2c3e50", foreground="white").pack(pady=(10, 3))
        ttk.Radiobutton(left_frame, text="First Derivative", variable=self.sharp_mode,
                       value=True, command=self.update_sharp_plot).pack(pady=3)
        ttk.Radiobutton(left_frame, text="Second Derivative", variable=self.sharp_mode,
                       value=False, command=self.update_sharp_plot).pack(pady=3)
        
        ttk.Button(left_frame, text="Apply Sharpening", command=self.apply_sharpening).pack(fill="x", pady=10)
        ttk.Button(left_frame, text="Save Result", command=self.save_sharp_result).pack(fill="x", pady=5)
        ttk.Button(left_frame, text="Compare with Test Case 1", command=self.compare_sharp_test1).pack(fill="x", pady=5)
        ttk.Button(left_frame, text="Compare with Test Case 2", command=self.compare_sharp_test2).pack(fill="x", pady=5)
        
        # Center panel - Plots
        center_frame = tk.Frame(sharp_frame, bg="#2c3e50")
        center_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.sharp_fig, (self.sharp_ax1, self.sharp_ax2) = plt.subplots(2, 1, figsize=(8, 6))
        self.sharp_fig.tight_layout(pad=3)
        self.sharp_canvas = FigureCanvasTkAgg(self.sharp_fig, master=center_frame)
        self.sharp_canvas.get_tk_widget().pack(fill="both", expand=True)
        self._style_plots(self.sharp_fig, [self.sharp_ax1, self.sharp_ax2])
    
    def _style_plots(self, fig, axes):
        for ax in axes:
            ax.grid(True, alpha=0.3)
            ax.set_facecolor("#34495e")
            ax.tick_params(colors="white")
            ax.title.set_color("white")
        fig.patch.set_facecolor("#2c3e50")
    
    # Averaging methods
    def load_avg_signal(self):
        path = filedialog.askopenfilename(title="Select Signal File", filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        try:
            self.avg_signal = basic_op.read_signal(path)
            messagebox.showinfo("Success", "Signal loaded successfully!")
            self.update_avg_plot()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load signal:\n{e}")
    
    def apply_averaging(self):
        if self.avg_signal is None:
            messagebox.showwarning("No Signal", "Please upload a signal first.")
            return
        try:
            window_size = self.avg_window_size.get()
            if window_size < 1:
                messagebox.showerror("Error", "Window size must be at least 1.")
                return
            self.avg_result = AveragingWindow.average(self.avg_signal.signal, window_size)
            messagebox.showinfo("Success", "Averaging applied successfully!")
            self.update_avg_plot()
        except Exception as e:
            messagebox.showerror("Error", f"Averaging failed:\n{e}")
    
    def save_avg_result(self):
        if self.avg_result is None:
            messagebox.showwarning("No Result", "Please apply averaging first.")
            return
        path = filedialog.asksaveasfilename(title="Save Result", defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt")])
        if path:
            try:
                self.avg_result.save_signal(path)
                messagebox.showinfo("Success", "Result saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save:\n{e}")
    
    def update_avg_plot(self):
        self.avg_ax1.clear()
        self.avg_ax2.clear()
        self._style_plots(self.avg_fig, [self.avg_ax1, self.avg_ax2])
        
        if self.avg_signal is not None:
            x = self.avg_signal.signal[:, 0]
            y = self.avg_signal.signal[:, 1]
            self.avg_ax1.stem(x, y, linefmt='b-', markerfmt='ro', basefmt='k-')
            self.avg_ax1.set_title("Original Signal")
            self.avg_ax1.set_xlabel("n")
            self.avg_ax1.set_ylabel("x(n)")
        
        if self.avg_result is not None:
            x = self.avg_result.signal[:, 0]
            y = self.avg_result.signal[:, 1]
            self.avg_ax2.stem(x, y, linefmt='g-', markerfmt='ro', basefmt='k-')
            self.avg_ax2.set_title("Averaged Signal")
            self.avg_ax2.set_xlabel("n")
            self.avg_ax2.set_ylabel("y(n)")
        
        self.avg_canvas.draw()
    
    # Convolution methods
    def load_conv_signal1(self):
        path = filedialog.askopenfilename(title="Select Signal 1", filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        try:
            self.conv_signal1 = basic_op.read_signal(path)
            messagebox.showinfo("Success", "Signal 1 loaded successfully!")
            self.update_conv_plot()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load signal:\n{e}")
    
    def load_conv_signal2(self):
        path = filedialog.askopenfilename(title="Select Signal 2", filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        try:
            self.conv_signal2 = basic_op.read_signal(path)
            messagebox.showinfo("Success", "Signal 2 loaded successfully!")
            self.update_conv_plot()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load signal:\n{e}")
    
    def apply_convolution(self):
        if self.conv_signal1 is None or self.conv_signal2 is None:
            messagebox.showwarning("Missing Signal", "Please upload both signals first.")
            return
        try:
            self.conv_result = Convolution.convolve(self.conv_signal1.signal, self.conv_signal2.signal)
            messagebox.showinfo("Success", "Convolution applied successfully!")
            self.update_conv_plot()
        except Exception as e:
            messagebox.showerror("Error", f"Convolution failed:\n{e}")
    
    def save_conv_result(self):
        if self.conv_result is None:
            messagebox.showwarning("No Result", "Please apply convolution first.")
            return
        path = filedialog.asksaveasfilename(title="Save Result", defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt")])
        if path:
            try:
                self.conv_result.save_signal(path)
                messagebox.showinfo("Success", "Result saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save:\n{e}")
    
    def update_conv_plot(self):
        self.conv_ax1.clear()
        self.conv_ax2.clear()
        self.conv_ax3.clear()
        self._style_plots(self.conv_fig, [self.conv_ax1, self.conv_ax2, self.conv_ax3])
        
        if self.conv_signal1 is not None:
            x = self.conv_signal1.signal[:, 0]
            y = self.conv_signal1.signal[:, 1]
            self.conv_ax1.stem(x, y, linefmt='b-', markerfmt='ro', basefmt='k-')
            self.conv_ax1.set_title("Signal 1")
            self.conv_ax1.set_xlabel("n")
            self.conv_ax1.set_ylabel("x₁(n)")
        
        if self.conv_signal2 is not None:
            x = self.conv_signal2.signal[:, 0]
            y = self.conv_signal2.signal[:, 1]
            self.conv_ax2.stem(x, y, linefmt='orange', markerfmt='go', basefmt='k-')
            self.conv_ax2.set_title("Signal 2")
            self.conv_ax2.set_xlabel("n")
            self.conv_ax2.set_ylabel("x₂(n)")
        
        if self.conv_result is not None:
            x = self.conv_result.signal[:, 0]
            y = self.conv_result.signal[:, 1]
            self.conv_ax3.stem(x, y, linefmt='g-', markerfmt='ro', basefmt='k-')
            self.conv_ax3.set_title("Convolved Signal")
            self.conv_ax3.set_xlabel("n")
            self.conv_ax3.set_ylabel("y(n)")
        
        self.conv_canvas.draw()
    
    # Sharpening methods
    def load_sharp_signal(self):
        path = filedialog.askopenfilename(title="Select Signal File", filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        try:
            self.sharp_signal = basic_op.read_signal(path)
            messagebox.showinfo("Success", "Signal loaded successfully!")
            self.update_sharp_plot()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load signal:\n{e}")
    
    def apply_sharpening(self):
        if self.sharp_signal is None:
            messagebox.showwarning("No Signal", "Please upload a signal first.")
            return
        try:
            first_deriv = self.sharp_mode.get()
            self.sharp_result = Sharpening.sharpen(self.sharp_signal.signal, first_deriv)
            mode_text = "First Derivative" if first_deriv else "Second Derivative"
            messagebox.showinfo("Success", f"Sharpening ({mode_text}) applied successfully!")
            self.update_sharp_plot()
        except Exception as e:
            messagebox.showerror("Error", f"Sharpening failed:\n{e}")
    
    def save_sharp_result(self):
        if self.sharp_result is None:
            messagebox.showwarning("No Result", "Please apply sharpening first.")
            return
        path = filedialog.asksaveasfilename(title="Save Result", defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt")])
        if path:
            try:
                self.sharp_result.save_signal(path)
                messagebox.showinfo("Success", "Result saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save:\n{e}")
    
    def update_sharp_plot(self):
        self.sharp_ax1.clear()
        self.sharp_ax2.clear()
        self._style_plots(self.sharp_fig, [self.sharp_ax1, self.sharp_ax2])
        
        if self.sharp_signal is not None:
            x = self.sharp_signal.signal[:, 0]
            y = self.sharp_signal.signal[:, 1]
            self.sharp_ax1.stem(x, y, linefmt='b-', markerfmt='ro', basefmt='k-')
            self.sharp_ax1.set_title("Original Signal")
            self.sharp_ax1.set_xlabel("n")
            self.sharp_ax1.set_ylabel("x(n)")
        
        if self.sharp_result is not None:
            x = self.sharp_result.signal[:, 0]
            y = self.sharp_result.signal[:, 1]
            mode_text = "First Derivative" if self.sharp_mode.get() else "Second Derivative"
            self.sharp_ax2.stem(x, y, linefmt='g-', markerfmt='ro', basefmt='k-')
            self.sharp_ax2.set_title(f"Sharpened Signal ({mode_text})")
            self.sharp_ax2.set_xlabel("n")
            self.sharp_ax2.set_ylabel("y(n)")
        
        self.sharp_canvas.draw()
    
    # Comparison methods
    def compare_avg_test1(self):
        if self.avg_result is None:
            messagebox.showwarning("No Result", "Please apply averaging first.")
            return
        try:
            indices = self.avg_result.signal[:, 0].astype(int).tolist()
            samples = self.avg_result.signal[:, 1].tolist()
            AveragingTest(indices, samples)
        except Exception as e:
            messagebox.showerror("Error", f"Comparison failed:\n{e}")

    def compare_avg_test2(self):
        if self.avg_result is None:
            messagebox.showwarning("No Result", "Please apply averaging first.")
            return
        try:
            indices = self.avg_result.signal[:, 0].astype(int).tolist()
            samples = self.avg_result.signal[:, 1].tolist()
            AveragingTest2(indices, samples)
        except Exception as e:
            messagebox.showerror("Error", f"Comparison failed:\n{e}")

    def compare_conv_test(self):
        if self.conv_result is None:
            messagebox.showwarning("No Result", "Please apply convolution first.")
            return
        try:
            indices = self.conv_result.signal[:, 0].astype(int).tolist()
            samples = self.conv_result.signal[:, 1].tolist()
            ConvolutionTest(indices, samples)
        except Exception as e:
            messagebox.showerror("Error", f"Comparison failed:\n{e}")

    def compare_sharp_test1(self):
        if self.sharp_result is None:
            messagebox.showwarning("No Result", "Please apply sharpening first.")
            return
        try:
            indices = self.sharp_result.signal[:, 0].astype(int).tolist()
            samples = self.sharp_result.signal[:, 1].tolist()
            SharpeningTest(indices, samples)
        except Exception as e:
            messagebox.showerror("Error", f"Comparison failed:\n{e}")

    def compare_sharp_test2(self):
        if self.sharp_result is None:
            messagebox.showwarning("No Result", "Please apply sharpening first.")
            return
        try:
            indices = self.sharp_result.signal[:, 0].astype(int).tolist()
            samples = self.sharp_result.signal[:, 1].tolist()
            SharpeningTest2(indices, samples)
        except Exception as e:
            messagebox.showerror("Error", f"Comparison failed:\n{e}")

    def back_to_home(self):
        self.root.destroy()
        self.home.root.deiconify()

