'''
import matplotlib.pyplot as plt

def read_and_store(filename, s, t_ex_A, s_B, t_ex_B, s_C, t_ex_C, s_P, t_ex_P):
    # Open the .txt file
    try:
        input_file = open(filename, 'r')
    except FileNotFoundError:
        while True:
            filename = input("Invalid or wrong file name! Please input the correct .txt file name: ")
            try:
                input_file = open(filename, 'r')
                break
            except FileNotFoundError:
                continue

    # Read the file content
    lines = input_file.readlines()
    input_file.close()  # Close the file after reading

    # -------------------------------------------- SAE MODE DATA --------------------------------------------
    if len(lines) > 1:
        first_line = lines[1].strip()
        if first_line != "n":
            s.extend(map(float, first_line.split()))

    if len(lines) > 2:
        second_line = lines[2].strip()
        if second_line != "n":
            t_ex_A.extend(map(float, second_line.split()))

    # -------------------------------------------- E-BL MODE DATA --------------------------------------------
    if len(lines) > 4:
        third_line = lines[4].strip()
        if third_line != "n":
            s_B.extend(map(float, third_line.split()))

    if len(lines) > 5:
        fourth_line = lines[5].strip()
        if fourth_line != "n":
            t_ex_B.extend(map(float, fourth_line.split()))

    # -------------------------------------------- SS MODE DATA --------------------------------------------
    if len(lines) > 7:
        fifth_line = lines[7].strip()
        if fifth_line != "n":
            s_C.extend(map(float, fifth_line.split()))

    if len(lines) > 8:
        sixth_line = lines[8].strip()
        if sixth_line != "n":
            t_ex_C.extend(map(float, sixth_line.split()))

    # -------------------------------------------- PS MODE DATA --------------------------------------------
    if len(lines) > 10:
        seventh_line = lines[10].strip()
        if seventh_line != "n":
            s_P.extend(map(float, seventh_line.split()))

    if len(lines) > 11:
        eighth_line = lines[11].strip()
        if eighth_line != "n":
            t_ex_P.extend(map(float, eighth_line.split()))

    # -------------------------------------------- TYPE OF STRESS MEASURE --------------------------------------------
    info1 = 0
    if len(lines) > 13:
        stress_def = lines[13].strip()
        if stress_def == "Nominal":
            info1 = 1
        elif stress_def == "Cauchy":
            info1 = 2
        else:
            print("Error: The stress measure line cannot be read.")
            info1 = -1

    # PURE MODES WITH DATA
    info2 = 0
    if s and not s_B and not s_C and not s_P:
        info2 = 1
    elif s and s_B and not s_C and not s_P:
        info2 = 2
    elif s and not s_B and s_C and not s_P:
        info2 = 3
    elif s and not s_B and not s_C and s_P:
        info2 = 4
    elif s and s_B and s_C and not s_P:
        info2 = 5
    elif s and s_B and not s_C and s_P:
        info2 = 6
    else:
        info2 = -1

    return info1, info2

def plot_exp_data(s, t_ex_A, s_B, t_ex_B, s_C, t_ex_C, s_P, t_ex_P, info1):
    """
    Plots four (x, y) pairs in a single figure with four subplots.

    Parameters:
    s, t_ex_A: Coordinates for the first line
    s_B, t_ex_B: Coordinates for the second line
    s_C, t_ex_C: Coordinates for the third line
    s_P, t_ex_P: Coordinates for the fourth line
    """
    # Create a figure with 2 rows and 2 columns of subplots
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.tight_layout(pad=5)  # Add spacing between subplots
    
    x_label_1 = "Stretch $ \lambda_1 $"
    x_label_2 = "Shear Parameter $ \gamma $"

    if info1 == 1:
        y_label_1 = "Nominal Stress $ P_{12}  $"
        y_label_2 = "Nominal Stress $ P_{12} $"

    else:
        y_label_1 = "Cauchy Stress $ \sigma_{11} $"
        y_label_2 = "Cauchy Stress $ \sigma_{12} $"

    # Plot first pair
    axs[0, 0].plot(s, t_ex_A, label='Pair 1', marker='o', linestyle='-', color='blue')
    axs[0, 0].set_title('Simple Axial Extension')
    axs[0, 0].set_xlabel(x_label_1)
    axs[0, 0].set_ylabel(y_label_1)
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # Plot second pair
    axs[0, 1].plot(s_B, t_ex_B, label='Pair 2', marker='s', linestyle='--', color='red')
    axs[0, 1].set_title('Equi-Biaxial Loading')
    axs[0, 1].set_xlabel(x_label_1)
    axs[0, 1].set_ylabel(y_label_1)
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # Plot third pair
    axs[1, 0].plot(s_C, t_ex_C, label='Pair 3', marker='^', linestyle='-.', color='green')
    axs[1, 0].set_title('Simple Shear')
    axs[1, 0].set_xlabel(x_label_2)
    axs[1, 0].set_ylabel(y_label_2)
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # Plot fourth pair
    axs[1, 1].plot(s_P, t_ex_P, label='Pair 4', marker='d', linestyle=':', color='purple')
    axs[1, 1].set_title('Pure Shear')
    axs[1, 1].set_xlabel(x_label_2)
    axs[1, 1].set_ylabel(y_label_2)
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    # Show all plots
    plt.show()

def main():
    # -------------------------------- Handling .txt File --------------------------------

    filename = input("Please enter .txt file name: ")   # Request user input

    # Vectors to store experimental data for different modes of deformation 
    s = []       # Stretch for the SAE pure mode of deformation 
    t_ex_A = []  # Stress for the SAE pure mode of deformation 
    s_B = []     # Stretch for the EB-L pure mode of deformation 
    t_ex_B = []  # Stress for the EB-L pure mode of deformation 
    s_C = []     # Shear parameter for the SS pure mode of deformation 
    t_ex_C = []  # Stress for the SS pure mode of deformation 
    s_P = []     # Stretch for the PS pure mode of deformation 
    t_ex_P = []  # Stress for the PS pure mode of deformation

    # Call read_and_store function to open and read a .txt file and store values in the vectors
    info1, info2 = read_and_store(filename, s, t_ex_A, s_B, t_ex_B, s_C, t_ex_C, s_P, t_ex_P)

    print(s)
    print(t_ex_A)
    # Plot experimental data
    plot_exp_data(s, t_ex_A, s_B, t_ex_B, s_C, t_ex_C, s_P, t_ex_P, info1)

if __name__ == "__main__":
    main()
'''

import tkinter as tk
from PIL import Image, ImageTk
import os
from windows.experimental_data_input import ExperimentalDataInputWindow
from windows.project_info_window import ProjectInfoWindow
from image_display import ImageDisplay

class HyperSmartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HyperSmart Software")
        self.root.geometry("500x700")
        self.root.configure(bg='white')

        # Load and set the window icon
        icon_size = (32, 32)
        minilogo_image = Image.open('MiniLogo.png')
        minilogo_image.thumbnail(icon_size, Image.LANCZOS)
        minilogo_image_tk = ImageTk.PhotoImage(minilogo_image)
        self.root.iconphoto(False, minilogo_image_tk)

        # Initialize the first window
        self.open_main_window()

    def open_main_window(self):
        self.clear_window()

        # Display the CNPq logo image
        ImageDisplay (self.root, "logo_cnpq.png", (50, 50), x=30, y=20)

        # Display the EESC logo image
        ImageDisplay (self.root, "eesc_logomarca1.png", (100, 50), x=380, y=20)

        # Display the main logo image
        ImageDisplay(self.root, "Logo_HyperSmart.png", (300,300), x=100, y=280)

        # Add the "Start New Calibration" button
        start_button = tk.Button(self.root, text="Start New Calibration", command=self.open_project_info)
        start_button.place(x=(500-110)/2, y=380)  

        # Add the "About HyperSmart" button
        about_button = tk.Button(self.root, text="About HyperSmart", command=self.show_about_info)
        about_button.place(x=10, y=665)

    def open_project_info(self):
        self.clear_window()
        ProjectInfoWindow(self.root, self.open_experimental_data_input)

    def show_about_info(self):
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

    def open_experimental_data_input(self, selected_stress):
        print(f'Selected Stress: {selected_stress}')
        self.clear_window()
        ExperimentalDataInputWindow(self.root)

    def open_about_hypersmart(self):
        # Define what happens when the "About HyperSmart" button is clicked
        print("About HyperSmart button clicked!")
        
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







