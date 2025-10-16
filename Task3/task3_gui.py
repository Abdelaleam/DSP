import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import io
import sys
from .Signal_Quantization import quantization
from .Test_1.QuanTest1 import QuantizationTest1
from .Test_2.QuanTest2 import QuantizationTest2

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
        self.q_error = None
        self.num_bits = tk.IntVar()
        self.num_levels = tk.IntVar()
        self.quant_mode = tk.StringVar(value="bits")

        left_frame = tk.Frame(self.root, bg="#2c3e50")
        left_frame.pack(side="left", fill="y", padx=15, pady=15)
        
        center_frame = tk.Frame(self.root, bg="#2c3e50")
        center_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
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
        ttk.Button(left_frame, text="Back to Home", command=self.back_to_home).pack(fill="x", pady=20)

        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(8, 9))
        self.fig.tight_layout(pad=3)
        self.canvas = FigureCanvasTkAgg(self.fig, master=center_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self._style_plots()
        self.toggle_mode()

        table_frame = tk.Frame(right_frame, bg="#2c3e50")
        table_frame.pack(fill="both", expand=True, pady=10)
        
        ttk.Label(table_frame, text="Quantization Results", font=("Arial", 14, "bold"),
                  foreground="white", background="#2c3e50").pack(pady=10)
        
        table_container = tk.Frame(table_frame, bg="#2c3e50")
        table_container.pack(fill="both", expand=True)
        
        columns = ("x", "y", "q_y", "q_error", "encoded_result", "indices")
        self.results_table = ttk.Treeview(table_container, columns=columns, show="headings", height=30)
        
        self.results_table.heading("x", text="X")
        self.results_table.heading("y", text="Y")
        self.results_table.heading("q_y", text="Q(X)")
        self.results_table.heading("q_error", text="QError")
        self.results_table.heading("encoded_result", text="Encoded")
        self.results_table.heading("indices", text="Index")
        
        self.results_table.column("x", width=60, anchor="center")
        self.results_table.column("y", width=80, anchor="center")
        self.results_table.column("q_y", width=120, anchor="center")
        self.results_table.column("q_error", width=120, anchor="center")
        self.results_table.column("encoded_result", width=80, anchor="center")
        self.results_table.column("indices", width=60, anchor="center")
        
        v_scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.results_table.yview)
        h_scrollbar = ttk.Scrollbar(table_container, orient="horizontal", command=self.results_table.xview)
        self.results_table.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        self.results_table.pack(side="left", fill="both", expand=True)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Treeview",
                       background="#34495e",
                       foreground="white",
                       fieldbackground="#34495e",
                       rowheight=35,
                       font=('Arial', 10))
        
        style.configure("Treeview.Heading",
                       background="#1abc9c",
                       foreground="white",
                       relief="flat",
                       font=('Arial', 11, 'bold'))
        
        style.map("Treeview", 
                 background=[('selected', '#e74c3c')],
                 foreground=[('selected', 'white')])

    def _style_plots(self):
        for ax in [self.ax1, self.ax2, self.ax3]:
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
            x, y, q_y, q_error, avg_err, encoded_result, indices = quantization.quantize_signal(
                self.signal, num_levels=num_levels, num_bits=num_bits
            )
            q_y = np.round(q_y, 2)
            q_error = np.round(q_error, 4)
            encoded_result[:, 1] = np.round(encoded_result[:, 1].astype(float), 2)
            self.q_data = (x, y, q_y)
            self.q_error = q_error
            self.encoded_result = encoded_result
            self.indices = indices
            self.avg_err = avg_err
            self.update_table(x, y, q_y, q_error, encoded_result, indices, avg_err)

            old_stdout = sys.stdout
            sys.stdout = mystdout = io.StringIO()
            if self.quant_mode.get() == "bits":
                QuantizationTest1('Task3/Test_1/Quan1_Out.txt', list(encoded_result[:, 0]), list(q_y))
            else:
                QuantizationTest2('Task3/Test_2/Quan2_Out.txt', list(indices), list(encoded_result[:, 0]), list(q_y), list(q_error))
            sys.stdout = old_stdout
            test_message = mystdout.getvalue().strip()

            messagebox.showinfo("Quantization Test", test_message if test_message else "Test completed.")
            self.update_plots()
        except Exception as e:
            messagebox.showerror("Error", f"Quantization failed:\n{e}")

    def update_table(self, x, y, q_y, q_error, encoded_result, indices, avg_err):
        for item in self.results_table.get_children():
            self.results_table.delete(item)
        for i in range(len(x)):
            bits_str = str(encoded_result[i, 0]) if i < len(encoded_result) else ""
            self.results_table.insert("", "end", values=(
                f"{int(x[i])}" if i < len(x) else "",
                f"{y[i]:.4f}" if i < len(y) else "",
                f"{q_y[i]:.4f}" if i < len(q_y) else "",
                f"{q_error[i]:.6f}" if i < len(q_error) else "",
                bits_str,
                f"{indices[i]}" if i < len(indices) else ""
            ))
        avg_row = self.results_table.insert("", "end", values=(
            "AVG", "", "", f"{avg_err:.6f}", "", "", ""
        ))
        self.results_table.tag_configure('avg_row', background='#2c3e50', foreground='#f39c12')
        self.results_table.item(avg_row, tags=('avg_row',))

    def update_plots(self):
        self.ax1.clear(); self.ax2.clear(); self.ax3.clear()
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
        if self.q_error is not None:
            self.ax3.plot(x, self.q_error, color='yellow', linewidth=2)
            self.ax3.set_title("Quantization Error")
            self.ax3.set_xlabel("x")
            self.ax3.set_ylabel("Q_Error")
        self.canvas.draw()

    def back_to_home(self):
        self.root.destroy()
        self.home.root.deiconify()
