import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Task1 import basic_op
from Task4.convolution import Convolution
from Task5.Fourier import Fourier
from Task7.FIR import FIR
from Task7.windows import Windows


class Task7GUI:
    def __init__(self, root, home):
        self.home = home
        self.root = tk.Toplevel(root)
        self.root.title("Task 7 - FIR Filter")
        self.root.configure(bg="#2c3e50")
        self.root.geometry("1400x900")
        self.root.protocol("WM_DELETE_WINDOW", self.back_to_home)
        
        # filter params
        self.filter_type = tk.StringVar(value="Low Pass")
        self.sampling_freq = tk.DoubleVar(value=8000.0)
        self.cutoff_freq = tk.DoubleVar(value=1500.0)
        self.f1 = tk.DoubleVar(value=150.0)
        self.f2 = tk.DoubleVar(value=250.0)
        self.transition_band = tk.DoubleVar(value=500.0)
        self.stop_attenuation = tk.DoubleVar(value=50.0)
        
        # method selection
        self.filtering_method = tk.StringVar(value="Convolution")
        
        # signal data
        self.input_signal = None
        self.filter_coeffs = None
        self.filtered_signal = None
        
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill="both", expand=True, padx=8, pady=8)

        left_frame = tk.Frame(main_frame, bg="#2c3e50", width=320)
        left_frame.pack(side="left", fill="y", padx=(6, 12), pady=6)
        left_frame.pack_propagate(False)

        right_frame = tk.Frame(main_frame, bg="#2c3e50")
        right_frame.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        # filter type selection
        ttk.Label(left_frame, text="Filter Type:", font=("Arial", 11, "bold"),
                  background="#2c3e50", foreground="white").pack(anchor="w", pady=(8, 2), padx=8)
        
        filter_types = ["Low Pass", "High Pass", "Band Pass", "Band Stop"]
        for ft in filter_types:
            ttk.Radiobutton(left_frame, text=ft, variable=self.filter_type, 
                          value=ft, command=self.on_filter_type_change).pack(anchor="w", padx=20)
        
        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=8, padx=8)
        
        # filter parameters
        ttk.Label(left_frame, text="Filter Parameters:", font=("Arial", 11, "bold"),
                  background="#2c3e50", foreground="white").pack(anchor="w", pady=(4, 2), padx=8)
        
        ttk.Label(left_frame, text="Sampling Freq (Hz):", background="#2c3e50", 
                 foreground="white").pack(anchor="w", padx=8)
        ttk.Entry(left_frame, textvariable=self.sampling_freq).pack(fill="x", padx=8, pady=(2, 6))
        
        self.fc_label = ttk.Label(left_frame, text="Cutoff Freq (Hz):", background="#2c3e50", 
                                 foreground="white")
        self.fc_label.pack(anchor="w", padx=8)
        self.fc_entry = ttk.Entry(left_frame, textvariable=self.cutoff_freq)
        self.fc_entry.pack(fill="x", padx=8, pady=(2, 6))
        
        self.f1_label = ttk.Label(left_frame, text="F1 (Hz):", background="#2c3e50", 
                                 foreground="white")
        self.f1_entry = ttk.Entry(left_frame, textvariable=self.f1)
        
        self.f2_label = ttk.Label(left_frame, text="F2 (Hz):", background="#2c3e50", 
                                 foreground="white")
        self.f2_entry = ttk.Entry(left_frame, textvariable=self.f2)
        
        ttk.Label(left_frame, text="Transition Band (Hz):", background="#2c3e50", 
                 foreground="white").pack(anchor="w", padx=8)
        ttk.Entry(left_frame, textvariable=self.transition_band).pack(fill="x", padx=8, pady=(2, 6))
        
        ttk.Label(left_frame, text="Stop Attenuation (dB):", background="#2c3e50", 
                 foreground="white").pack(anchor="w", padx=8)
        ttk.Entry(left_frame, textvariable=self.stop_attenuation).pack(fill="x", padx=8, pady=(2, 6))
        
        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=8, padx=8)
        
        # filtering method
        ttk.Label(left_frame, text="Filtering Method:", font=("Arial", 11, "bold"),
                  background="#2c3e50", foreground="white").pack(anchor="w", pady=(4, 2), padx=8)
        
        method_frame = tk.Frame(left_frame, bg="#2c3e50")
        method_frame.pack(anchor="w", padx=8)
        ttk.Radiobutton(method_frame, text="Convolution", variable=self.filtering_method, 
                       value="Convolution").pack(side="left")
        ttk.Radiobutton(method_frame, text="DFT/IDFT", variable=self.filtering_method, 
                       value="DFT/IDFT").pack(side="left")
        
        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=8, padx=8)
        
        # buttons
        ttk.Button(left_frame, text="Design Filter", command=self.design_filter).pack(fill="x", padx=8, pady=4)
        ttk.Button(left_frame, text="Load Signal", command=self.load_signal).pack(fill="x", padx=8, pady=4)
        ttk.Button(left_frame, text="Apply Filter", command=self.apply_filter).pack(fill="x", padx=8, pady=4)
        ttk.Button(left_frame, text="Save Filtered Signal", command=self.save_filtered_signal).pack(fill="x", padx=8, pady=4)
        ttk.Button(left_frame, text="Clear Plots", command=self.clear_plots).pack(fill="x", padx=8, pady=4)
        
        ttk.Button(left_frame, text="Back to Home", command=self.back_to_home).pack(side="bottom", fill="x", padx=8, pady=8)
        
        # plots
        self.fig, (self.ax_input, self.ax_filter, self.ax_output) = plt.subplots(3, 1, figsize=(10, 9))
        self.fig.tight_layout(pad=3)
        self.style_plots(self.fig, [self.ax_input, self.ax_filter, self.ax_output])
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.clear_plots()
        self.on_filter_type_change()
    
    def style_plots(self, fig, axes):
        for ax in axes:
            ax.grid(True, alpha=0.3)
            ax.set_facecolor("#34495e")
            ax.tick_params(colors="white")
            ax.title.set_color("white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
        fig.patch.set_facecolor("#2c3e50")
    
    def style_single_axis(self, ax):
        ax.grid(True, alpha=0.3)
        ax.set_facecolor("#34495e")
        ax.tick_params(colors="white")
        ax.title.set_color("white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        self.fig.patch.set_facecolor("#2c3e50")
    
    def on_filter_type_change(self):
        ft = self.filter_type.get()
        if ft in ["Band Pass", "Band Stop"]:
            # hide cutoff freq
            self.fc_label.pack_forget()
            self.fc_entry.pack_forget()
            # show f1 and f2
            self.f1_label.pack(anchor="w", padx=8)
            self.f1_entry.pack(fill="x", padx=8, pady=(2, 6))
            self.f2_label.pack(anchor="w", padx=8)
            self.f2_entry.pack(fill="x", padx=8, pady=(2, 6))
        else:
            # hide f1 and f2
            self.f1_label.pack_forget()
            self.f1_entry.pack_forget()
            self.f2_label.pack_forget()
            self.f2_entry.pack_forget()
            # show cutoff freq
            self.fc_label.pack(anchor="w", padx=8)
            self.fc_entry.pack(fill="x", padx=8, pady=(2, 6))
    
    def design_filter(self):
        try:
            fs = float(self.sampling_freq.get())
            tb = float(self.transition_band.get())
            sa = float(self.stop_attenuation.get())
            ft = self.filter_type.get()
            
            if ft == "Low Pass":
                fc = float(self.cutoff_freq.get())
                self.filter_coeffs = FIR.fir_lpf(fs, fc, tb, sa)
            elif ft == "High Pass":
                fc = float(self.cutoff_freq.get())
                self.filter_coeffs = FIR.fir_hpf(fs, fc, tb, sa)
            elif ft == "Band Pass":
                f1 = float(self.f1.get())
                f2 = float(self.f2.get())
                self.filter_coeffs = FIR.fir_band_pass(fs, f1, f2, tb, sa)
            elif ft == "Band Stop":
                f1 = float(self.f1.get())
                f2 = float(self.f2.get())
                self.filter_coeffs = FIR.fir_band_stop(fs, f1, f2, tb, sa)
            
            messagebox.showinfo("Success", f"Filter designed with {len(self.filter_coeffs)} coefficients")
            self.update_plots()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def load_signal(self):
        path = filedialog.askopenfilename(title="Select Signal File", filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        try:
            self.input_signal = basic_op.read_signal(path)
            messagebox.showinfo("Success", "Signal loaded")
            self.update_plots()
        except Exception as e:
            messagebox.showerror("Error loading signal", str(e))
    
    def apply_filter(self):
        if self.filter_coeffs is None:
            messagebox.showwarning("No filter", "Design a filter first")
            return
        if self.input_signal is None:
            messagebox.showwarning("No signal", "Load a signal first")
            return
        
        try:
            method = self.filtering_method.get()
            x_indices = self.input_signal.signal[:, 0].astype(int)
            x_values = self.input_signal.signal[:, 1]
            
            if method == "Convolution":
                # use convolution
                signal_x = np.column_stack((x_indices, x_values))
                M = (len(self.filter_coeffs) - 1) // 2
                h_indices = np.arange(-M, M + 1)
                signal_h = np.column_stack((h_indices, self.filter_coeffs))
                result = Convolution.convolve(signal_x, signal_h)
                y_indices = result.signal[:, 0].astype(int)
                y_values = result.signal[:, 1]
            else:
                # use DFT/IDFT
                y_values = self.filter_with_dft_idft(x_values, self.filter_coeffs)
                M = (len(self.filter_coeffs) - 1) // 2
                first_idx = int(x_indices[0]) + (-M)
                y_indices = np.arange(first_idx, first_idx + len(y_values))
            
            # store result
            self.filtered_signal = np.column_stack((y_indices, y_values))
            
            messagebox.showinfo("Success", f"Filter applied using {method}")
            self.update_plots()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def filter_with_dft_idft(self, x_values, h):
        # determine output length
        N = len(x_values) + len(h) - 1
        
        # zero pad both signals to length N
        x_padded = np.zeros(N)
        h_padded = np.zeros(N)
        x_padded[:len(x_values)] = x_values
        h_padded[:len(h)] = h
        
        # compute DFT
        X_amp, X_phase = Fourier.DFT(x_padded)
        H_amp, H_phase = Fourier.DFT(h_padded)
        
        X = [X_amp[k] * np.exp(1j * X_phase[k]) for k in range(N)]
        H = [H_amp[k] * np.exp(1j * H_phase[k]) for k in range(N)]
        
        # multiply in frequency domain
        Y = [X[k] * H[k] for k in range(N)]
        
        # convert back to amplitude and phase
        Y_amp = [abs(y) for y in Y]
        Y_phase = [np.angle(y) for y in Y]
        
        # compute IDFT
        y_values = Fourier.IDFT(Y_amp, Y_phase)
        
        return np.array(y_values)
    
    def save_filtered_signal(self):
        if self.filtered_signal is None:
            messagebox.showwarning("No result", "Apply filter first")
            return
        
        path = filedialog.asksaveasfilename(title="Save Filtered Signal", 
                                           defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        
        try:
            with open(path, "w") as f:
                f.write("0\n0\n")
                f.write(f"{len(self.filtered_signal)}\n")
                for i in range(len(self.filtered_signal)):
                    idx = int(self.filtered_signal[i, 0])
                    val = float(self.filtered_signal[i, 1])
                    f.write(f"{idx} {val}\n")
            messagebox.showinfo("Saved", "Filtered signal saved")
        except Exception as e:
            messagebox.showerror("Save error", str(e))
    
    def clear_plots(self):
        self.ax_input.clear()
        self.style_single_axis(self.ax_input)
        self.ax_input.set_title("Input Signal")
        self.ax_input.set_xlabel("n")
        self.ax_input.set_ylabel("x(n)")
        self.ax_input.axhline(0, color="k")
        
        self.ax_filter.clear()
        self.style_single_axis(self.ax_filter)
        self.ax_filter.set_title("Filter Coefficients")
        self.ax_filter.set_xlabel("n")
        self.ax_filter.set_ylabel("h(n)")
        self.ax_filter.axhline(0, color="k")
        
        self.ax_output.clear()
        self.style_single_axis(self.ax_output)
        self.ax_output.set_title("Filtered Signal")
        self.ax_output.set_xlabel("n")
        self.ax_output.set_ylabel("y(n)")
        self.ax_output.axhline(0, color="k")
        
        self.canvas.draw()
    
    def update_plots(self):
        self.clear_plots()
        
        # plot input signal
        if self.input_signal is not None:
            x = self.input_signal.signal[:, 0]
            y = self.input_signal.signal[:, 1]
            self.ax_input.stem(x, y, linefmt='b-', markerfmt='ro', basefmt='k-')
        
        # plot filter coefficients
        if self.filter_coeffs is not None:
            M = (len(self.filter_coeffs) - 1) // 2
            h_indices = np.arange(-M, M + 1)
            self.ax_filter.stem(h_indices, self.filter_coeffs, linefmt='g-', markerfmt='go', basefmt='k-')
        
        # plot filtered signal
        if self.filtered_signal is not None:
            y_idx = self.filtered_signal[:, 0]
            y_val = self.filtered_signal[:, 1]
            self.ax_output.stem(y_idx, y_val, linefmt='m-', markerfmt='mo', basefmt='k-')
        
        self.canvas.draw()
    
    def back_to_home(self):
        self.root.destroy()
        self.home.root.deiconify()
