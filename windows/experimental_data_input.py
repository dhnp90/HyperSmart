import tkinter as tk
from image_display import ImageDisplay

class ExperimentalDataInputWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Experimental Data Input")
        self.root.geometry("500x700")

        # Display the main logo image
        ImageDisplay(self.root, 'Logo_HyperSmart.png', (300, 300), x=100, y=25)

        # Define deformation modes
        deformation_modes = ["Simple Axial Extension", "Equi-Biaxial Loading", "Simple Shear", "Pure Shear"]
        top_padding = tk.Label(root, bg='white')
        top_padding.pack(pady=(200, 0))
        
        for item in deformation_modes:
            button = tk.Button(root, text=item)
            button.pack(pady=30)

