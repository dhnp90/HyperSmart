import tkinter as tk
from tkinter import font

# Initialize the Tkinter root window
root = tk.Tk()

# Check if a specific font is available
font_name = "Cambria Math"
if font_name in font.families():
    print(f"{font_name} is available!")
else:
    print(f"{font_name} is NOT available. Please install it.")

root.mainloop()
