# graph_display_of_data.py
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from image_display import ImageDisplay

class DataInputVisualisation:
    def __init__(self, root, material):
        self.root = root
        self.material = material
        self.root.title("Data Input Graphical Visualisation")
        self.center_window(900, 700)
        self.root.configure(bg='white')

        # Display the main logo image
        ImageDisplay(self.root, 'Logo_HyperSmart.png', (300, 300), x=300, y=25)


    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - width / 2)
        center_y = int(screen_height / 2 - height / 2)
        self.root.geometry(f'{width}x{height}+{center_x}+{center_y}')


