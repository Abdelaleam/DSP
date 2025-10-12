import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .Sin_Cos_Waves import Waves, waves
import numpy as np

class Signal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Task2GUI:
    def __init__(self, root, home):
        self.home = home
        self.root = tk.Toplevel(root)
        self.root.title("Task 2 - Signal Generation")
        self.root.geometry("1400x900")
        self.root.configure(bg="#2c3e50")
        self.root.protocol("WM_DELETE_WINDOW", self.back_to_home)

        self.selected_type = tk.StringVar(value=waves.Sin.name)
        self.amplitude = tk.DoubleVar(value=1.0)
        self.freq = tk.DoubleVar(value=5.0)
        self.shifted = tk.DoubleVar(value=0.0)
        self.fs = tk.IntVar(value=20)
        self.discrete_out = None
        self.continous_out = None

        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = tk.Frame(main_frame, bg="#34495e", width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10))
        left_frame.pack_propagate(False)

        tk.Label(left_frame, text="Select Signal Type:", font=("Arial", 10, "bold"),
                 bg="#34495e", fg="#ecf0f1").pack(fill="x", pady=(5,2))
        type_cb = ttk.Combobox(left_frame, textvariable=self.selected_type, state="readonly")
        type_cb['values'] = [waves.Sin.name, waves.Cos.name]
        type_cb.pack(fill="x", pady=2)

        tk.Label(left_frame, text="Amplitude (A):", bg="#34495e", fg="#ecf0f1").pack(anchor="w", pady=(10,2))
        tk.Entry(left_frame, textvariable=self.amplitude, bg="#2c3e50", fg="white", insertbackground="white").pack(fill="x", pady=2)

        tk.Label(left_frame, text="Frequency :", bg="#34495e", fg="#ecf0f1").pack(anchor="w", pady=2)
        tk.Entry(left_frame, textvariable=self.freq, bg="#2c3e50", fg="white", insertbackground="white").pack(fill="x", pady=2)

        tk.Label(left_frame, text="Theta (θ):", bg="#34495e", fg="#ecf0f1").pack(anchor="w", pady=2)
        tk.Entry(left_frame, textvariable=self.shifted, bg="#2c3e50", fg="white", insertbackground="white").pack(fill="x", pady=2)

        tk.Label(left_frame, text="Sampling Freq (Fs):", bg="#34495e", fg="#ecf0f1").pack(anchor="w", pady=2)
        tk.Entry(left_frame, textvariable=self.fs, bg="#2c3e50", fg="white", insertbackground="white").pack(fill="x", pady=2)

        self.create_button(left_frame, "Generate Continuous Signal", self.generate_signal, "#9b59b6", "#8e44ad").pack(fill="x", pady=(20,2))
        self.create_button(left_frame, "Sample Signal", self.sample_signal, "#3498db", "#2980b9").pack(fill="x", pady=2)
        self.create_button(left_frame, "Clear All", self.clear_all, "#e74c3c", "#c0392b").pack(fill="x", pady=10)
        self.create_button(left_frame, "Back to Home", self.back_to_home, "#7f8c8d", "#95a5a6").pack(fill="x", pady=10)

        right_frame = tk.Frame(main_frame, bg="#2c3e50")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig = plt.figure(figsize=(14,9), facecolor='#2c3e50')
        self.ax1 = plt.subplot(211)
        self.ax2 = plt.subplot(212)
        plt.subplots_adjust(hspace=0.4, left=0.1, right=0.95, top=0.95, bottom=0.08)
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('#34495e')
            ax.tick_params(colors='white')
            ax.title.set_color('white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            for spine in ax.spines.values():
                spine.set_color('white')
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_button(self, parent, text, command, color, hover_color, width=None):
        btn = tk.Button(parent, text=text, font=("Arial", 9, "bold"),
                        bg=color, fg="white", activebackground=hover_color,
                        activeforeground="white", relief="raised", bd=1,
                        padx=5, pady=4, cursor="hand2", command=command, width=width)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        return btn

    def generate_signal(self):
        signal_type = getattr(waves, self.selected_type.get())
        x, y = Waves.Gen_sin_cos(signal_type, self.amplitude.get(), self.freq.get(), self.shifted.get())
        self.continous_out = Signal(x, y)
        self.ax1.clear()
        self.ax1.set_title(f"{self.selected_type.get().upper()} Continuous Signal", color='white')
        self.ax1.set_xlabel("x")
        self.ax1.set_ylabel("f(x)")
        self.ax1.plot(x, y, color='cyan')
        self.canvas.draw()

    def sample_signal(self):
        Fs = self.fs.get()
        F = self.freq.get()
        if Fs < 2*F:
            messagebox.showerror("ERROR", f"Fs must be at least {2*F}")
            return
        signal_type = getattr(waves, self.selected_type.get())
        x, y = Waves.Sampling(signal_type, self.amplitude.get(), self.freq.get(), Fs, self.shifted.get())
        self.discrete_out = Signal(x, y)
        self.ax2.clear()
        self.ax2.set_title(f"Sampled {self.selected_type.get().upper()} Signal", color='white')
        self.ax2.set_xlabel("n")
        self.ax2.set_ylabel("f(n)")
        self.ax2.stem(x, y, basefmt="k", linefmt='r-', markerfmt='o')
        self.canvas.draw()

    def clear_all(self):
        self.continous_out = None
        self.discrete_out = None
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.text(0.5, 0.5, "No Data", transform=self.ax1.transAxes, ha='center', va='center', color='gray')
        self.ax2.text(0.5, 0.5, "No Data", transform=self.ax2.transAxes, ha='center', va='center', color='gray')
        self.canvas.draw()

    def back_to_home(self):
        self.root.destroy()
        self.home.root.deiconify()
