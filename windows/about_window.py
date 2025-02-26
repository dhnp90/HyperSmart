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
        self.center_window(about_window, 450, 500)
        about_window.configure(bg='white')

        # Use TkDefaultFont for consistency
        custom_font = "TkDefaultFont"

        # Initial Information (still using Label)
        initial_info = (
            "HyperSmart Software\nVersion 1.0\n\n"
            "Developed by: Dr. Daniel Henrique Nunes Peixoto\n"
            "Email: danielh_peixoto@hotmail.com"
        )
        initial_label = tk.Label(about_window, text=initial_info, bg='white', 
                                 justify=tk.CENTER, wraplength=380, font=custom_font)
        initial_label.pack(pady=10)

        # Frame to hold text and scrollbar
        frame = tk.Frame(about_window, bg="white")
        frame.pack(pady=10, padx=10, fill="both")  # No expand=True

        # Create Text widget with fixed size
        text_widget = tk.Text(frame, wrap="word", height=30, width=68, bg="white", font=custom_font)
        text_widget.pack(side="left")  # No fill="both", no expand=True

        # Add Scrollbar
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")

        # Link Scrollbar to Text widget
        text_widget.config(yscrollcommand=scrollbar.set)


        # Load text from the .txt file into the Text widget
        file_path = 'About.txt'
        try:
            with open(file_path, 'r', encoding="utf-8") as file:
                about_text = file.read()
                text_widget.insert("1.0", about_text)  # Insert text into Text widget
        except Exception as e:
            text_widget.insert("1.0", f"Error loading file: {e}")

        # Disable editing
        text_widget.config(state="disabled")



