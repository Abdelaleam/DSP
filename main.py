import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Task1.task1_gui import Task1GUI
import os


class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("DSP Tasks - Home")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2c3e50")
        self.root.protocol("WM_DELETE_WINDOW", self.exit_program)

        # main icon
        ico_path = "signal_1871160.ico"
        if os.path.exists(ico_path):
            try:
                self.root.iconbitmap(ico_path)
            except Exception as e:
                print("Icon load error:", e)
        else:
            print("No logo.ico found, skipping icon setup")
        # title
        self.title_label = tk.Label(self.root, text="Welcome to DSP Program",
                                    font=("Arial Black", 34), bg="#2c3e50", fg="#00ffcc")
        self.title_label.place(relx=0.5, rely=0.1, anchor="center")

        # buttons style
        self.open_btn = tk.Button(self.root, text="Task 1\n[Signal Operations]", 
                                 font=("Arial", 16, "bold"),
                                 bg="#1abc9c", fg="#ffffff",
                                 activebackground="#16a085", activeforeground="#ffffff",
                                 relief="flat", padx=15, pady=15,
                                 cursor="hand2",
                                 command=self.open_task1)
        self.open_btn.place(relx=0.05, rely=0.4, anchor="w", width=200, height=50)

        self.exit_btn = tk.Button(self.root, text="Exit",
                                 font=("Arial", 16, "bold"),
                                 bg="#e74c3c", fg="#ffffff",
                                 activebackground="#c0392b", activeforeground="#ffffff",
                                 relief="flat", padx=15, pady=15,
                                 cursor="hand2",
                                 command=self.exit_program)
        self.exit_btn.place(relx=0.95, rely=0.95, anchor="se", width=200, height=50)

        # hover effects
        self.open_btn.bind("<Enter>", lambda e: self.open_btn.config(bg="#16a085"))
        self.open_btn.bind("<Leave>", lambda e: self.open_btn.config(bg="#1abc9c"))
        
        self.exit_btn.bind("<Enter>", lambda e: self.exit_btn.config(bg="#c0392b"))
        self.exit_btn.bind("<Leave>", lambda e: self.exit_btn.config(bg="#e74c3c"))

    def open_task1(self):
        self.root.withdraw()
        Task1GUI(self.root, self)

    def exit_program(self):
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = HomePage(root)
    root.mainloop()