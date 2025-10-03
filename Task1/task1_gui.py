import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .Basic_OP import basic_op   


class Task1GUI:
    def __init__(self, root, home):
        self.home = home
        self.root = tk.Toplevel(root) 
        self.root.title("Task 1 - Signal Operations")
        self.root.geometry("1200x700")  
        self.root.configure(bg="#2c3e50")
        self.root.protocol("WM_DELETE_WINDOW", self.back_to_home)
        self.signal1 = None
        self.signal2 = None
        self.result = None

        # Main frame
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left frame for OP 
        left_frame = tk.Frame(main_frame, bg="#34495e", width=250)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)

        # load and save buttons
        tk.Label(left_frame, text="File Operations:", font=("Arial", 10, "bold"), 
                bg="#34495e", fg="#ecf0f1").pack(fill="x", pady=(0, 3))
        
        self.create_button(left_frame, "Load Signal 1", self.load_signal1, "#2ecc71", "#27ae60").pack(fill="x", pady=1)
        self.create_button(left_frame, "Load Signal 2", self.load_signal2, "#2ecc71", "#27ae60").pack(fill="x", pady=1)
        self.create_button(left_frame, "Save Result", self.save_result, "#9b59b6", "#8e44ad").pack(fill="x", pady=1)

        # clear buttons
        tk.Label(left_frame, text="Clear Operations:", font=("Arial", 10, "bold"), 
                bg="#34495e", fg="#ecf0f1").pack(fill="x", pady=(8, 3))
        
        self.create_button(left_frame, "Clear Signal 1", self.clear_signal1, "#e74c3c", "#c0392b").pack(fill="x", pady=1)
        self.create_button(left_frame, "Clear Signal 2", self.clear_signal2, "#e74c3c", "#c0392b").pack(fill="x", pady=1)
        self.create_button(left_frame, "Clear Result", self.clear_result, "#e74c3c", "#c0392b").pack(fill="x", pady=1)
        self.create_button(left_frame, "Clear All", self.clear_all, "#e67e22", "#d35400").pack(fill="x", pady=1)

        # Math Operations buttons
        tk.Label(left_frame, text="Math Operations:", font=("Arial", 10, "bold"), 
                bg="#34495e", fg="#ecf0f1").pack(fill="x", pady=(8, 3))
        
        self.create_button(left_frame, "Add", self.add_signals, "#3498db", "#2980b9").pack(fill="x", pady=1)
        self.create_button(left_frame, "Subtract", self.sub_signals, "#3498db", "#2980b9").pack(fill="x", pady=1)

        #combobox for select specific signal
        tk.Label(left_frame, text="Apply on:", font=("Arial", 10, "bold"), 
                bg="#34495e", fg="#ecf0f1").pack(fill="x", pady=(8, 3))
        
        target_frame = tk.Frame(left_frame, bg="#34495e")
        target_frame.pack(fill="x", pady=2)
        
        self.target_var = tk.StringVar(value="Signal 1")
        self.target_combo = ttk.Combobox(
            target_frame, textvariable=self.target_var,
            values=["Signal 1", "Signal 2", "Result"], state="readonly", width=12
        )
        self.target_combo.pack(fill="x", padx=2)

        # mul input 
        mult_frame = tk.Frame(left_frame, bg="#34495e")
        mult_frame.pack(fill="x", pady=3)
        
        tk.Label(mult_frame, text="Multiply ×", font=("Arial", 9), 
                bg="#34495e", fg="#ecf0f1").pack(side=tk.LEFT)
        
        self.mult_entry = tk.Entry(mult_frame, width=6, bg="#2c3e50", fg="white", 
                                 insertbackground="white", font=("Arial", 9))
        self.mult_entry.insert(0, "1.0")
        self.mult_entry.pack(side=tk.LEFT, padx=3)
        
        self.create_button(mult_frame, "Apply", self.multiply_signal, "#f39c12", "#e67e22", width=8).pack(side=tk.RIGHT)

        # Delay input
        delay_frame = tk.Frame(left_frame, bg="#34495e")
        delay_frame.pack(fill="x", pady=3)
        
        tk.Label(delay_frame, text="Delay +", font=("Arial", 9), 
                bg="#34495e", fg="#ecf0f1").pack(side=tk.LEFT)
        
        self.delay_entry = tk.Entry(delay_frame, width=6, bg="#2c3e50", fg="white",
                                  insertbackground="white", font=("Arial", 9))
        self.delay_entry.insert(0, "0")
        self.delay_entry.pack(side=tk.LEFT, padx=3)
        
        self.create_button(delay_frame, "Apply", self.delay_signal, "#f39c12", "#e67e22", width=8).pack(side=tk.RIGHT)

        # Folding button
        self.create_button(left_frame, "Folding", self.folding_signal, "#9b59b6", "#8e44ad").pack(fill="x", pady=3)

        # Back to home button
        self.create_button(left_frame, "Back to Home", self.back_to_home, "#7f8c8d", "#95a5a6").pack(fill="x", pady=10)

        # Right frame for plots
        right_frame = tk.Frame(main_frame, bg="#2c3e50")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create plots 
        self.fig = plt.figure(figsize=(8, 9), facecolor='#2c3e50')
        
        # Create 3 subplots 
        self.ax1 = plt.subplot(311)
        self.ax2 = plt.subplot(312)
        self.ax3 = plt.subplot(313)
        
        # space between plots
        plt.subplots_adjust(hspace=0.5)
        
        # Style for plots
        for ax in [self.ax1, self.ax2, self.ax3]:
            ax.set_facecolor('#34495e')
            ax.tick_params(colors='white')
            ax.title.set_color('white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            for spine in ax.spines.values():
                spine.set_color('white')

        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_plot()

    # create button fun
    def create_button(self, parent, text, command, color, hover_color, width=None):
        btn = tk.Button(parent, text=text, font=("Arial", 9, "bold"),
                      bg=color, fg="white", activebackground=hover_color,
                      activeforeground="white", relief="raised", bd=1,
                      padx=5, pady=4, cursor="hand2", command=command, width=width)
        
        # Hover effects
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        return btn

    # see what i packed from combobox
    def get_target_signal(self):
        choice = self.target_var.get()
        if choice == "Signal 1":
            return self.signal1
        elif choice == "Signal 2":
            return self.signal2
        elif choice == "Result":
            return self.result
        return None
     # pick target from combobox
    def set_target_signal(self, new_signal):
        choice = self.target_var.get()
        if choice == "Signal 1":
            self.signal1 = new_signal
        elif choice == "Signal 2":
            self.signal2 = new_signal
        elif choice == "Result":
            self.result = new_signal

    # handle plots
    def update_plot(self):
        # Signal 1
        self.ax1.clear()
        if self.signal1 is not None:
            self.signal1.visualize(self.ax1, "Signal 1")
        else:
            self.ax1.set_title("Signal 1", color='white')
            self.ax1.text(0.5, 0.5, 'No Data', transform=self.ax1.transAxes, 
                         ha='center', va='center', fontsize=10, color='gray')

        # Signal 2
        self.ax2.clear()
        if self.signal2 is not None:
            self.signal2.visualize(self.ax2, "Signal 2")
        else:
            self.ax2.set_title("Signal 2", color='white')
            self.ax2.text(0.5, 0.5, 'No Data', transform=self.ax2.transAxes, 
                         ha='center', va='center', fontsize=10, color='gray')

        # Result
        self.ax3.clear()
        if self.result is not None:
            self.result.visualize(self.ax3, "Result")
        else:
            self.ax3.set_title("Result", color='white')
            self.ax3.text(0.5, 0.5, 'No Data', transform=self.ax3.transAxes, 
                         ha='center', va='center', fontsize=10, color='gray')

        # Reapply styling
        for ax in [self.ax1, self.ax2, self.ax3]:
            ax.set_facecolor('#34495e')
            ax.tick_params(colors='white')
            ax.title.set_color('white')
            for spine in ax.spines.values():
                spine.set_color('white')

        self.canvas.draw()

    # file funs for load and save
    def load_signal1(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            self.signal1 = basic_op.read_signal(path)
            self.update_plot()

    def load_signal2(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            self.signal2 = basic_op.read_signal(path)
            self.update_plot()

    def save_result(self):
        if self.result is None:
            messagebox.showerror("Error", "No result to save!")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            self.result.save_signal(path)
            messagebox.showinfo("Saved", "Signal saved successfully!")

    # OP funs
    def add_signals(self):
        if self.signal1 is not None and self.signal2 is not None:
            self.result = self.signal1.add_signals(self.signal2)
            self.update_plot()

    def sub_signals(self):
        if self.signal1 is not None and self.signal2 is not None:
            self.result = self.signal1.sub_signals(self.signal2)
            self.update_plot()

    def multiply_signal(self):
        sig = self.get_target_signal()
        if sig is not None:
            try:
                c = float(self.mult_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid multiply factor!")
                return
            self.result = sig.multiply(c)
            self.update_plot()

    def delay_signal(self):
        sig = self.get_target_signal()
        if sig is not None:
            try:
                c = float(self.delay_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid delay value!")
                return
            self.result = sig.delay_signal(c)
            self.update_plot()

    def folding_signal(self):
        sig = self.get_target_signal()
        if sig is not None:
            self.result = sig.folding()
            self.update_plot()

    # clear funs
    def clear_signal1(self):
        self.signal1 = None
        self.update_plot()

    def clear_signal2(self):
        self.signal2 = None
        self.update_plot()

    def clear_result(self):
        self.result = None
        self.update_plot()

    def clear_all(self):
        self.signal1 = None
        self.signal2 = None
        self.result = None
        self.mult_entry.delete(0, tk.END)
        self.mult_entry.insert(0, "1.0")
        self.delay_entry.delete(0, tk.END)
        self.delay_entry.insert(0, "0")
        self.update_plot()

    # return to home
    def back_to_home(self):
        self.root.destroy()
        self.home.root.deiconify()