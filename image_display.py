# image_display.py

import tkinter as tk
from PIL import Image, ImageTk

class ImageDisplay:
    def __init__(self, parent, image_path, max_size, x=0, y=0):
        self.parent = parent
        self.image_path = image_path
        self.max_size = max_size
        self.x = x
        self.y = y
        self.display_image()

    def display_image(self):
        # Load the image
        main_image = Image.open(self.image_path)
        # Resize the image while maintaining the aspect ratio
        main_image.thumbnail(self.max_size, Image.LANCZOS)
        # Convert the image to a format Tkinter can use
        main_image_tk = ImageTk.PhotoImage(main_image)
        
        # Add the image to a label and place it at the specified coordinates
        image_label = tk.Label(self.parent, image=main_image_tk, bg='white')
        image_label.place(x=self.x, y=self.y)
        # Keep a reference to prevent the image from being garbage collected
        image_label.image = main_image_tk



