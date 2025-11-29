import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Task1 import basic_op
from Task5.Fourier import Fourier


class Task5GUI:
    def __init__(self, root, home):
        self.home = home
        self.root = tk.Toplevel(root)
        self.root.title("Task 5 - Fourier (one page)")
        self.root.configure(bg="#2c3e50")
        self.root.geometry("1400x900")
        self.root.protocol("WM_DELETE_WINDOW", self.back_to_home)
        
        self.mode = tk.StringVar(value="DFT")
        self.dft_signal = None
        self.dft_freq_bins = None
        self.dft_amplitudes = None
        self.dft_phases = None
        self.dft_fs = tk.DoubleVar(value=1000.0)

        self.idft_amplitudes = None
        self.idft_phases = None
        self.idft_result = None

        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill="both", expand=True, padx=8, pady=8)

        left_frame = tk.Frame(main_frame, bg="#2c3e50", width=320)
        left_frame.pack(side="left", fill="y", padx=(6, 12), pady=6)
        left_frame.pack_propagate(False)

        right_frame = tk.Frame(main_frame, bg="#2c3e50")
        right_frame.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        ttk.Label(left_frame, text="Mode:", font=("Arial", 11, "bold"),
                  background="#2c3e50", foreground="white").pack(anchor="w", pady=(8, 2), padx=8)
        mode_frame = tk.Frame(left_frame, bg="#2c3e50")
        mode_frame.pack(anchor="w", padx=8)
        ttk.Radiobutton(mode_frame, text="DFT", variable=self.mode, value="DFT", command=self._on_mode_change).pack(side="left")
        ttk.Radiobutton(mode_frame, text="IDFT", variable=self.mode, value="IDFT", command=self._on_mode_change).pack(side="left")

        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=8, padx=8)
        ttk.Label(left_frame, text="DFT / Signal", background="#2c3e50", foreground="white").pack(anchor="w", padx=8)
        ttk.Button(left_frame, text="Upload Signal (for DFT)", command=self.load_dft_signal).pack(fill="x", padx=8, pady=6)

        ttk.Label(left_frame, text="Sampling Frequency (Hz):", background="#2c3e50", foreground="white").pack(anchor="w", padx=8)
        ttk.Entry(left_frame, textvariable=self.dft_fs).pack(fill="x", padx=8, pady=(2, 8))

        ttk.Button(left_frame, text="Apply DFT", command=self.apply_dft).pack(fill="x", padx=8, pady=6)
        ttk.Button(left_frame, text="Save DFT Result", command=self.save_dft_result).pack(fill="x", padx=8, pady=6)
        ttk.Button(left_frame, text="Compare DFT Results", command=self.compare_dft_results).pack(fill="x", padx=8, pady=6)

        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=8, padx=8)
        ttk.Label(left_frame, text="IDFT / DFT Data", background="#2c3e50", foreground="white").pack(anchor="w", padx=8)
        ttk.Button(left_frame, text="Upload DFT Data (for IDFT)", command=self.load_idft_data).pack(fill="x", padx=8, pady=6)
        ttk.Button(left_frame, text="Apply IDFT", command=self.apply_idft).pack(fill="x", padx=8, pady=6)
        ttk.Button(left_frame, text="Save Reconstructed Signal", command=self.save_idft_result).pack(fill="x", padx=8, pady=6)
        ttk.Button(left_frame, text="Compare IDFT Results", command=self.compare_idft_results).pack(fill="x", padx=8, pady=6)
        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=8, padx=8)
        ttk.Button(left_frame, text="Clear Plots", command=self.clear_plots).pack(fill="x", padx=8, pady=6)

        ttk.Button(left_frame, text="Close", command=self.root.destroy).pack(side="bottom", fill="x", padx=8, pady=8)

        self.fig, (self.ax_time, self.ax_amp, self.ax_phase) = plt.subplots(3, 1, figsize=(10, 9))
        self.fig.tight_layout(pad=3)
        self._style_plots(self.fig, [self.ax_time, self.ax_amp, self.ax_phase])

        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.clear_plots()
        self._on_mode_change()

    def _style_plots(self, fig, axes):
        for ax in axes:
            ax.grid(True, alpha=0.3)
            ax.set_facecolor("#34495e")
            ax.tick_params(colors="white")
            ax.title.set_color("white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
        fig.patch.set_facecolor("#2c3e50")

    def load_dft_signal(self):
        path = filedialog.askopenfilename(title="Select Signal File", filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        try:
            self.dft_signal = basic_op.read_signal(path)
            messagebox.showinfo("Success", "Signal loaded for DFT.")
            self.update_plots()
        except Exception as e:
            messagebox.showerror("Error loading signal", str(e))

    def apply_dft(self):
        if self.dft_signal is None:
            messagebox.showwarning("No signal", "Upload a signal first (for DFT).")
            return
        try:
            fs = float(self.dft_fs.get())
            if fs <= 0:
                raise ValueError("Sampling frequency must be positive.")
            dft_ret = Fourier.DFT(self.dft_signal.signal[:, 1], fs)
            if isinstance(dft_ret, tuple):
                if len(dft_ret) == 3:
                    self.dft_freq_bins, self.dft_amplitudes, self.dft_phases = dft_ret
                elif len(dft_ret) == 4:
                    self.dft_freq_bins, self.dft_amplitudes, self.dft_phases, _ = dft_ret
                elif len(dft_ret) == 2:
                    self.dft_amplitudes, self.dft_phases = dft_ret
                    self.dft_freq_bins = np.arange(len(self.dft_amplitudes)) * (fs / len(self.dft_amplitudes))
                else:
                    self.dft_amplitudes, self.dft_phases = dft_ret[0], dft_ret[1]
                    self.dft_freq_bins = np.arange(len(self.dft_amplitudes)) * (fs / len(self.dft_amplitudes))
            else:
                raise ValueError("Unexpected return from Fourier.DFT")
            self.dft_freq_bins = np.asarray(self.dft_freq_bins, dtype=float)
            self.dft_amplitudes = np.asarray(self.dft_amplitudes, dtype=float)
            self.dft_phases = np.asarray(self.dft_phases, dtype=float)
            messagebox.showinfo("DFT", "DFT computed.")
            self.update_plots()
        except Exception as e:
            messagebox.showerror("DFT error", str(e))

    def save_dft_result(self):
        if self.dft_amplitudes is None or self.dft_phases is None:
            messagebox.showwarning("No DFT", "Apply DFT first.")
            return
        path = filedialog.asksaveasfilename(title="Save DFT Result", defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("0\n0\n")
                f.write(f"{len(self.dft_amplitudes)}\n")
                for i in range(len(self.dft_amplitudes)):
                    f.write(f"{i} {float(self.dft_amplitudes[i])} {float(self.dft_phases[i])}\n")
            messagebox.showinfo("Saved", "DFT result saved.")
        except Exception as e:
            messagebox.showerror("Save error", str(e))

    def load_idft_data(self):
        path = filedialog.askopenfilename(title="Select DFT Data File", filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        try:
            data = basic_op.read_signal(path)
            arr = np.asarray(data.signal, dtype=float)
            if arr.ndim == 1:
                arr = arr.reshape(-1, arr.size)
            cols = arr.shape[1]
            if cols >= 3:
                self.idft_amplitudes = arr[:, 1].astype(float)
                self.idft_phases = arr[:, 2].astype(float)
            elif cols == 2:
                self.idft_amplitudes = arr[:, 0].astype(float)
                self.idft_phases = arr[:, 1].astype(float)
            elif cols == 1:
                self.idft_amplitudes = arr[:, 0].astype(float)
                self.idft_phases = np.zeros_like(self.idft_amplitudes, dtype=float)
            else:
                raise ValueError("Unrecognized DFT data format.")
            messagebox.showinfo("Loaded", "DFT data loaded for IDFT.")
            self.update_plots()
        except Exception as e:
            messagebox.showerror("Load error", str(e))

    def apply_idft(self):
        if self.idft_amplitudes is None or self.idft_phases is None:
            messagebox.showwarning("No DFT data", "Upload DFT data for IDFT first.")
            return
        try:
            amps = [float(a) for a in np.asarray(self.idft_amplitudes).flatten()]
            phs = [float(p) for p in np.asarray(self.idft_phases).flatten()]
            rec = Fourier.IDFT(amps, phs)
            self.idft_result = [int(round(float(x))) for x in rec]
            messagebox.showinfo("IDFT", "IDFT computed.")
            self.update_plots()
        except Exception as e:
            messagebox.showerror("IDFT error", str(e))

    def save_idft_result(self):
        if self.idft_result is None:
            messagebox.showwarning("No result", "Apply IDFT first.")
            return
        path = filedialog.asksaveasfilename(title="Save Reconstructed Signal", defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("0\n0\n")
                f.write(f"{len(self.idft_result)}\n")
                for i, v in enumerate(self.idft_result):
                    f.write(f"{i} {int(v)}\n")
            messagebox.showinfo("Saved", "Reconstructed signal saved.")
        except Exception as e:
            messagebox.showerror("Save error", str(e))

    def clear_plots(self):
        self.ax_time_clear()
        self.ax_amp_clear()
        self.ax_phase_clear()
        self.canvas.draw()

    def ax_time_clear(self):
        self.ax_time.clear()
        self._style_single_axis(self.ax_time)
        self.ax_time.set_title("Time Domain")
        self.ax_time.set_xlabel("n")
        self.ax_time.set_ylabel("x(n)")
        self.ax_time.axhline(0, color="k")

    def ax_amp_clear(self):
        self.ax_amp.clear()
        self._style_single_axis(self.ax_amp)
        self.ax_amp.set_title("Frequency vs Amplitude")
        self.ax_amp.set_xlabel("Frequency (Hz)")
        self.ax_amp.set_ylabel("Amplitude")
        self.ax_amp.axhline(0, color="k")

    def ax_phase_clear(self):
        self.ax_phase.clear()
        self._style_single_axis(self.ax_phase)
        self.ax_phase.set_title("Frequency vs Phase")
        self.ax_phase.set_xlabel("Frequency (Hz)")
        self.ax_phase.set_ylabel("Phase (radians)")
        self.ax_phase.axhline(0, color="k")

    def _style_single_axis(self, ax):
        ax.grid(True, alpha=0.3)
        ax.set_facecolor("#34495e")
        ax.tick_params(colors="white")
        ax.title.set_color("white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        self.fig.patch.set_facecolor("#2c3e50")

    def update_plots(self):
        self.ax_time_clear()
        self.ax_amp_clear()
        self.ax_phase_clear()

        if self.mode.get() == "DFT":
            if self.dft_signal is not None:
                x = np.asarray(self.dft_signal.signal[:, 0], dtype=float)
                y = np.asarray(self.dft_signal.signal[:, 1], dtype=float)
                self.ax_time.stem(x, y, linefmt='b-', markerfmt='ro', basefmt='k-')
            if self.dft_freq_bins is not None and self.dft_amplitudes is not None:
                self.ax_amp.stem(self.dft_freq_bins, self.dft_amplitudes, linefmt='g-', markerfmt='go', basefmt='k-')
            if self.dft_freq_bins is not None and self.dft_phases is not None:
                self.ax_phase.stem(self.dft_freq_bins, self.dft_phases, linefmt='y-', markerfmt='yo', basefmt='k-')
        else:
            if self.idft_result is not None:
                indices = np.arange(len(self.idft_result))
                self.ax_time.stem(indices, self.idft_result, linefmt='b-', markerfmt='ro', basefmt='k-')
            if self.idft_amplitudes is not None:
                N = len(self.idft_amplitudes)
                fs = float(self.dft_fs.get()) if self.dft_fs.get() else 1.0
                freq_bins = np.arange(N) * (fs / N)
                self.ax_amp.stem(freq_bins, self.idft_amplitudes, linefmt='g-', markerfmt='go', basefmt='k-')
            if self.idft_phases is not None:
                N = len(self.idft_phases)
                fs = float(self.dft_fs.get()) if self.dft_fs.get() else 1.0
                freq_bins = np.arange(N) * (fs / N)
                self.ax_phase.stem(freq_bins, self.idft_phases, linefmt='y-', markerfmt='yo', basefmt='k-')

        self.canvas.draw()

    def _on_mode_change(self):
        self.update_plots()

    def compare_dft_results(self):
        if self.dft_amplitudes is None or self.dft_phases is None:
            messagebox.showwarning("No DFT", "Apply DFT first.")
            return
        path = filedialog.askopenfilename(title="Select Expected Output File", filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        try:
            with open(path, 'r') as f:
                lines = f.readlines()
            expected_amplitudes = []
            expected_phases = []
            for line in lines[3:]:  
                parts = line.strip().split()
                if len(parts) >= 2:
                    amp = float(parts[0].rstrip('f'))
                    phase = float(parts[1].rstrip('f'))
                    expected_amplitudes.append(amp)
                    expected_phases.append(phase)
            rounded_computed_amplitudes = [round(amp, 4) for amp in self.dft_amplitudes]
            rounded_expected_amplitudes = [round(amp, 4) for amp in expected_amplitudes]
            rounded_computed_phases = [round(phase, 4) for phase in self.dft_phases]
            rounded_expected_phases = [round(phase, 4) for phase in expected_phases] 
            from Task5.signalcompare import SignalComapreAmplitude, SignalComaprePhaseShift
            amplitude_match = SignalComapreAmplitude(
                rounded_computed_amplitudes, 
                rounded_expected_amplitudes
            )
            phase_match = SignalComaprePhaseShift(
                rounded_computed_phases, 
                rounded_expected_phases
            )
            if amplitude_match and phase_match:
                messagebox.showinfo("Comparison Result", "DFT results match the expected output!")
            else:
                messagebox.showwarning("Comparison Result", 
                                    f"DFT results do not match the expected output.\n"
                                    f"Amplitude match: {amplitude_match}\n"
                                    f"Phase match: {phase_match}")
        
        except Exception as e:
            messagebox.showerror("Comparison Error", str(e))
    def compare_idft_results(self):
        if self.idft_result is None:
            messagebox.showwarning("No IDFT", "Apply IDFT first.")
            return
        
        path = filedialog.askopenfilename(title="Select Expected Output File", filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        
        try:
            with open(path, 'r') as f:
                lines = f.readlines()
            
            expected_signal = []
            
            for line in lines[3:]:  
                parts = line.strip().split()
                if len(parts) >= 2:
                    value = float(parts[1].rstrip('f')) if 'f' in parts[1] else float(parts[1])
                    expected_signal.append(value)
            
            rounded_computed_signal = [round(val, 4) for val in self.idft_result]
            rounded_expected_signal = [round(val, 4) for val in expected_signal]
            
            from Task5.signalcompare import SignalComapreAmplitude
            
            signal_match = SignalComapreAmplitude(
                rounded_computed_signal, 
                rounded_expected_signal
            )
            
            if signal_match:
                messagebox.showinfo("Comparison Result", "IDFT results match the expected output!")
            else:
                messagebox.showwarning("Comparison Result", 
                                    f"IDFT results do not match the expected output.\n"
                                    f"Signal match: {signal_match}")
        
        except Exception as e:
            messagebox.showerror("Comparison Error", str(e))

    def back_to_home(self):
        self.root.destroy()
        self.home.root.deiconify()
