import tkinter as tk
from PIL import Image, ImageTk
import os
from windows.experimental_data_input import ExperimentalDataWindow
from windows.project_info_window import ProjectInfoWindow
from windows.about_window import AboutWindow
from image_display import ImageDisplay
from data_center import ExperimentalData

class HyperSmartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HyperSmart Software")
        self.center_window(500, 700)
        self.root.configure(bg='white')

        # Load and set the window icon
        icon_size = (32, 32)
        minilogo_image = Image.open('MiniLogo.png')
        minilogo_image.thumbnail(icon_size, Image.LANCZOS)
        minilogo_image_tk = ImageTk.PhotoImage(minilogo_image)
        self.root.iconphoto(False, minilogo_image_tk)

        # Initialize the first window
        self.open_main_window()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - width / 2)
        center_y = int(screen_height / 2 - height / 2)
        self.root.geometry(f'{width}x{height}+{center_x}+{center_y}')

    def open_main_window(self):
        self.clear_window()

        # Images
        ImageDisplay (self.root, "logo_cnpq.png", (50, 50), x=30, y=20)             # Display the CNPq logo image    
        ImageDisplay (self.root, "eesc_logomarca1.png", (100, 50), x=380, y=20)     # Display the EESC logo image
        ImageDisplay(self.root, "Logo_HyperSmart.png", (300,300), x=100, y=280)     # Display the main logo image

        # Add the "Start New Calibration" button
        start_button = tk.Button(self.root, text="Start New Calibration", command=self.open_project_info)
        start_button.place(x=(500-110)/2, y=380)  

        # Add the "About HyperSmart" button
        about_button = tk.Button(self.root, text="About HyperSmart", command=self.show_about_info)
        about_button.place(x=10, y=665)

    def show_about_info(self):
        AboutWindow(self.root)

    def open_project_info(self):
        self.clear_window()
        ProjectInfoWindow(self.root, self.open_experimental_data_input)

    def open_experimental_data_input(self, material):
        self.clear_window()
        ExperimentalDataWindow(self.root, material)
        
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# teste
def main():
    root = tk.Tk()
    app = HyperSmartApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()







