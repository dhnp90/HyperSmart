# about_window.py
import tkinter as tk
from tkinter import messagebox

class AboutWindow:
    def __init__(self, root):
        self.root = root
        self.create_window()

    def create_window(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About HyperSmart")
        about_window.geometry("400x520")
        about_window.configure(bg='white')

        # Initial Information
        initial_info = "HyperSmart Software\nVersion 1.0\n\nDeveloped by: Dr. Daniel Henrique Nunes Peixoto\nEmail: danielh_peixoto@hotmail.com"
        initial_label = tk.Label(about_window, text=initial_info, bg='white', justify=tk.CENTER, wraplength=380)
        initial_label.pack(pady=10)

        # Load text from the .txt file (left-justified)
        file_path = 'About.txt'
        with open(file_path, 'r') as file:
            about_text = file.read()
        about_label = tk.Label(about_window, text=about_text, bg='white',justify=tk.LEFT, wraplength=380)
        about_label.pack(pady=20)
