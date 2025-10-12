import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from .Signal_Quantization import quantization

class Task3GUI:
    def __init__(self, root, home):
        self.root = tk.Toplevel(root)
        self.root.title("Task 3 - Signal Quantization and Encoding")
        self.root.configure(bg="#2c3e50")
        self.root.protocol("WM_DELETE_WINDOW", self.back_to_home)
        self.home = home
        self.signal = None
        self.encoded_result = None
        self.q_data = None
        self.num_bits = tk.IntVar()
        self.num_levels = tk.IntVar()
        self.quant_mode = tk.StringVar(value="bits")
        self.avg_error = tk.StringVar(value="Average Error Power: N/A")

        left_frame = tk.Frame(self.root, bg="#2c3e50")
        left_frame.pack(side="left", fill="y", padx=15, pady=15)
        right_frame = tk.Frame(self.root, bg="#2c3e50")
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ttk.Label(left_frame, text="Quantization Controls", font=("Arial", 14, "bold"),
                  foreground="white", background="#2c3e50").pack(pady=10)
        ttk.Button(left_frame, text="Upload Signal", command=self.load_signal).pack(fill="x", pady=5)

        ttk.Radiobutton(left_frame, text="Use Number of Bits", variable=self.quant_mode,
                        value="bits", command=self.toggle_mode).pack(pady=3)
        ttk.Radiobutton(left_frame, text="Use Number of Levels", variable=self.quant_mode,
                        value="levels", command=self.toggle_mode).pack(pady=3)

        ttk.Label(left_frame, text="Number of Bits:", background="#2c3e50", foreground="white").pack()
        self.bits_entry = ttk.Entry(left_frame, textvariable=self.num_bits)
        self.bits_entry.pack(fill="x", pady=3)

        ttk.Label(left_frame, text="Number of Levels:", background="#2c3e50", foreground="white").pack()
        self.levels_entry = ttk.Entry(left_frame, textvariable=self.num_levels, state="disabled")
        self.levels_entry.pack(fill="x", pady=3)

        ttk.Button(left_frame, text="Quantize Signal", command=self.quantize_signal).pack(fill="x", pady=10)
        ttk.Label(left_frame, textvariable=self.avg_error, background="#2c3e50",
                  foreground="white", font=("Arial", 11, "italic")).pack(pady=5)
        ttk.Button(left_frame, text="Save Encoded Result", command=self.save_encoded_result).pack(fill="x", pady=10)
        ttk.Button(left_frame, text="Back to Home", command=self.back_to_home).pack(fill="x", pady=20)

        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 7))
        self.fig.tight_layout(pad=3)
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self._style_plots()
        self.toggle_mode()

    def _style_plots(self):
        for ax in [self.ax1, self.ax2]:
            ax.grid(True, alpha=0.3)
            ax.set_facecolor("#34495e")
            ax.tick_params(colors="white")
            ax.title.set_color("white")
        self.fig.patch.set_facecolor("#2c3e50")

    def toggle_mode(self):
        if self.quant_mode.get() == "bits":
            self.bits_entry.config(state="normal")
            self.levels_entry.config(state="disabled")
        else:
            self.bits_entry.config(state="disabled")
            self.levels_entry.config(state="normal")

    def load_signal(self):
        path = filedialog.askopenfilename(title="Select Signal File", filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        try:
            self.signal = quantization.read_signal(path).signal
            messagebox.showinfo("Success", "Signal loaded successfully!")
            self.update_plots()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load signal:\n{e}")

    def quantize_signal(self):
        if self.signal is None:
            messagebox.showwarning("No Signal", "Please upload a signal first.")
            return
        try:
            num_bits = self.num_bits.get() if self.quant_mode.get() == "bits" else 0
            num_levels = self.num_levels.get() if self.quant_mode.get() == "levels" else 0
            x, y, q_y, q_error, avg_err, encoded_result = quantization.quantize_signal(
                self.signal, num_levels=num_levels, num_bits=num_bits
            )
            q_y = np.round(q_y, 2)
            encoded_result[:, 1] = np.round(encoded_result[:, 1].astype(float), 2)
            self.q_data = (x, y, q_y)
            self.encoded_result = encoded_result
            self.avg_error.set(f"Average Error Power: {avg_err:.6f}")
            self.update_plots()
        except Exception as e:
            messagebox.showerror("Error", f"Quantization failed:\n{e}")

    def update_plots(self):
        self.ax1.clear(); self.ax2.clear()
        self._style_plots()
        if self.signal is not None:
            x = self.signal[:, 0]
            y = self.signal[:, 1]
            self.ax1.stem(x, y, linefmt='b-', markerfmt='ro')
            self.ax1.set_title("Uploaded Signal")
            self.ax1.set_xlabel("x")
            self.ax1.set_ylabel("x(n)")
        if self.q_data is not None:
            x, y, q_y = self.q_data
            self.ax2.stem(x, q_y, linefmt='g-', markerfmt='ro')
            self.ax2.set_title("Quantized Signal")
            self.ax2.set_xlabel("x")
            self.ax2.set_ylabel("q(n)")
        self.canvas.draw()

    def save_encoded_result(self):
        if self.encoded_result is None:
            messagebox.showwarning("No Data", "Please quantize first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt")])
        if not path:
            return
        quantization.save_signal(self.encoded_result, path)
        messagebox.showinfo("Saved", "Encoded result saved successfully!")

    def back_to_home(self):
        self.root.destroy()
        self.home.root.deiconify()
