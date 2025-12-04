import tkinter as tk
from tkinter import ttk
from Task1.task1_gui import Task1GUI
from Task2.task2_gui import Task2GUI
from Task3.task3_gui import Task3GUI
from Task4.task4_gui import Task4GUI
from Task5.task5_gui import Task5GUI
import os

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("DSP Tasks - Home")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2c3e50")
        self.root.protocol("WM_DELETE_WINDOW", self.exit_program)

        ico_path = "signal_1871160.ico"
        if os.path.exists(ico_path):
            try:
                self.root.iconbitmap(ico_path)
            except Exception as e:
                print("Icon load error:", e)
        else:
            print("No logo.ico found, skipping icon setup")

        self.title_label = tk.Label(
            self.root,
            text="Welcome to DSP Program",
            font=("Arial Black", 34),
            bg="#2c3e50",
            fg="#00ffcc"
        )
        self.title_label.place(relx=0.5, rely=0.1, anchor="center")

        self.task1_btn = self.create_button(
            text="Task 1\n[Signal Operations]",
            bg="#1abc9c", hover="#16a085",
            command=self.open_task1
        )
        self.task1_btn.place(relx=0.05, rely=0.20, anchor="w", width=250, height=80)

        self.task2_btn = self.create_button(
            text="Task 2\n[Signal Generation]",
            bg="#3498db", hover="#2980b9",
            command=self.open_task2
        )
        self.task2_btn.place(relx=0.05, rely=0.35, anchor="w", width=250, height=80)

        self.task3_btn = self.create_button(
            text="Task 3\n[Signal Quantization & Encoding]",
            bg="#9b59b6", hover="#8e44ad",
            command=self.open_task3
        )
        self.task3_btn.config(font=("Arial", 10, "bold"))
        self.task3_btn.place(relx=0.05, rely=0.50, anchor="w", width=250, height=80)

        self.task4_btn = self.create_button(
            text="Task 4\n[Signal Processing]",
            bg="#e67e22", hover="#d35400",
            command=self.open_task4
        )
        self.task4_btn.place(relx=0.05, rely=0.65, anchor="w", width=250, height=80)

        self.exit_btn = self.create_button(
            text="Exit",
            bg="#e74c3c", hover="#c0392b",
            command=self.exit_program
        )
        self.task5_btn = self.create_button(
            text="Task 5\n[Fourier Transform]",
            bg="#f1c40f", hover="#f39c12",
            command=self.open_task5
        )
        self.task5_btn.place(relx=0.05, rely=0.80, anchor="w", width=250, height=80)
        self.exit_btn.place(relx=0.95, rely=0.95, anchor="se", width=200, height=50)

        

    def create_button(self, text, bg, hover, command):
        btn = tk.Button(
            self.root, text=text, font=("Arial", 16, "bold"),
            bg=bg, fg="white", activebackground=hover, activeforeground="white",
            relief="flat", padx=15, pady=15, cursor="hand2", command=command
        )
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    def open_task1(self):
        self.root.withdraw()
        Task1GUI(self.root, self)

    def open_task2(self):
        self.root.withdraw()
        Task2GUI(self.root, self)

    def open_task3(self):
        self.root.withdraw()
        Task3GUI(self.root, self)

    def open_task4(self):
        self.root.withdraw()
        Task4GUI(self.root, self)

    def open_task5(self):
        self.root.withdraw()
        Task5GUI(self.root, self)

    def exit_program(self):
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HomePage(root)
    root.mainloop()
