# model_first_window.py

import tkinter as tk
from image_display import ImageDisplay

class ModelingChoice:
    def __init__(self, root, material):
        self.root = root
        self.material = material
        self.root.title = "Defining Hyperelastic Model"
        self.center_window(500, 700)
        self.root.configure(bg='white')

        # Display the main logo image
        ImageDisplay(self.root, 'Logo_HyperSmart.png', (300, 300), x=100, y=25)

        # Create the button to ask help to define the best hyperelastic model 
        help_choose_model_button = tk.Button(self.root, text='Help me define the best hyperelastic model to represent my material', width=55, height=1, justify="center")
        help_choose_model_button.place(x=54, y=300)

        # Create button to ask for help calibrating hyperelastic model already chosen
        help_calibration_button = tk.Button(self.root, text='I already chose the most appropriate hyperelastic model;\n Help me calibrate its material parameters', width=55, height=2, justify="center")
        help_calibration_button.place(x=54, y=360)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - width / 2)
        center_y = int(screen_height / 2 - height / 2)
        self.root.geometry(f'{width}x{height}+{center_x}+{center_y}')
