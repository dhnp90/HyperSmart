# about_window.py
import tkinter as tk
from tkinter import messagebox

class AboutWindow:
    def __init__(self, root):
        self.root = root
        self.create_window()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        center_x = int(screen_width / 2 - width / 2)
        center_y = int(screen_height / 2 - height / 2)
        window.geometry(f'{width}x{height}+{center_x}+{center_y}')

    def create_window(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About HyperSmart")
        self.center_window(about_window, 400, 520)
        about_window.configure(bg='white')

        # Initial Information
        initial_info = "HyperSmart Software\nVersion 1.0\n\nDeveloped by: Dr. Daniel Henrique Nunes Peixoto\nEmail: danielh_peixoto@hotmail.com"
        initial_label = tk.Label(about_window, text=initial_info, bg='white', justify=tk.CENTER, wraplength=380)
        initial_label.pack(pady=10)

        # Load text from the .txt file (left-justified)
        file_path = 'About.txt'
        with open(file_path, 'r') as file:
            about_text = file.read()
        about_label = tk.Label(about_window, text=about_text, bg='white', justify=tk.LEFT, wraplength=380)
        about_label.pack(pady=20)
