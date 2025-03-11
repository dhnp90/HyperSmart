# exp_data_opt_window.py

import tkinter as tk
from image_display import ImageDisplay

class ExpDataOptions:
    def __init__(self, root, callback_input, callback_repository):
        self.root = root
        self.proceed_callback_input = callback_input
        self.proceed_callback_repository = callback_repository
        self.root.title("Experimental Data Options")
        self.root.geometry("500x700")

        # Display the main logo
        ImageDisplay(self.root, 'Logo_HyperSmart.png', (300, 300), x=100, y=25)

        # Input Experimental Data Directly Button
        input_data_button = tk.Button(self.root, text='Input Experimental Data', width=55, height=1, justify="center", command=self.proceed_callback_input)
        input_data_button.place(x=54, y=300)

        # Use Experimental Data Repository
        use_reposit_button = tk.Button(self.root, text='Use the Experimental Data Repository', width=55, height=1, justify="center", command=self.proceed_callback_repository)
        use_reposit_button.place(x=54, y=360)