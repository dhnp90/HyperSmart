''' 
------------------------------------------------------------------------
-------------------------------- Header --------------------------------
------------------------------------------------------------------------
The goal of this project is to provide scientists from various fields, 
including mechanical, civil, and biomedical engineering, with a robust 
tool to calibrate and select the most appropriate model to mechanically 
describe the behavior of hyperelastic materials.

Contributions:
Dr. D. H. N. Peixoto (USP)	
Conceptualization, Software Implementation, Research Execution

Prof. Dr. E. D. Leonel (USP) 	
Conceptualization, Research Supervision

Prof. Dr. M. Greco (UFMG)
Conceptualization, Research Collaboration
'''

'''
------------------------------------------------------------------------
------------------------- Software Description -------------------------
------------------------------------------------------------------------
This software aims to contemplate the following three main features:

Experimental Data Handling:

    - Experimental Data Repository;

    - Experimental Data Input by User;

Hyperelastic Model Selecting:

    - Selection by the User of a Hyperelastic Model From The Library of
    Models Contained in the Program;

    - Insertion of Custom Hyperelastic Model by the User;

    - Computational-Assisted Selection of Optimized Hyperelastic Model;

Material Parameters Calibration:

    - Use of Bayesian Inference Approach;

    - Library of Numerical Methods for Calibration;
'''

# Importing Python Libraries
import tkinter as tk
from PIL import Image, ImageTk
import os

# Import classes that define/control the App Windows
from windows.experimental_data_input import ExperimentalDataWindow
from windows.project_info_window import ProjectInfoWindow
from windows.about_window import AboutWindow
from windows.graph_display_of_data import DataInputVisualisation
from windows.model_first_window import ModelingChoice
from windows.model_options_window import OptionsOfModels
from windows.exp_data_opt_window import ExpDataOptions
from windows.mat_repository_window import MatRepositoryWindow
from windows.exp_data_info import ChosenExpDataInfo
from windows.access_data_window import AccessExpDataWindow
from windows.rep_data_plt_window import RepDataPlotWindow
from windows.rep_data_plt_confirm import RepDataPlotConfirmWindow

# Import Auxiliary Classes
from helpers.image_display import ImageDisplay
from helpers.data_center import ExperimentalData
import helpers.geometry_manager as gm
from helpers.path_helpers import resolve_path

# The HyperSmartApp class is the main of the software
class HyperSmartApp:
    def __init__(self, root):

        # ------------------------------------------------ App First Window and About ------------------------------------------------
        self.root = root
        self.input_status = {"sae_stretch": False, "ebl_stretch": False, "ss_shear_parameter": False, "ps_shear_parameter": False}
        self.root.title("HyperSmart Software")
        self.center_window(500, 700)
        self.root.configure(bg='white')

        # Load and set the window icon
        icon_size = (32, 32)
        minilogo_image = Image.open(r'C:\Users\Daniel Peixoto\OneDrive\Programação\Python\ajusteCurvasSHG\HyperSmart\src\assets\logos\MiniLogo.png')
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
        image_path = resolve_path("assets/logos/logo_cnpq.png")             # Display the CNPq logo image 
        ImageDisplay(self.root, image_path, (70,70), x=20, y=40)
        image_path = resolve_path("assets/logos/eesc_logomarca1.png")       # Display the EESC logo image
        ImageDisplay(self.root, image_path, (180, 100), x=160, y=30)
        image_path = resolve_path("assets/logos/Logo_HyperSmart.png")       # Display the main logo image
        ImageDisplay(self.root, image_path, (300,300), x=100, y=280)
        image_path = resolve_path("assets/logos/LogoEEUFMG1.png")            # Display the EEUFMG logo image
        ImageDisplay(self.root, image_path, (90,90), x=395, y=25)

        # Add the "Start New Calibration" button
        start_button = tk.Button(self.root, text="Start New Calibration", command=self.exp_data_options)
        start_button.place(x=(500-110)/2, y=380)  

        # Add the "About HyperSmart" button
        about_button = tk.Button(self.root, text="About HyperSmart", command=self.show_about_info)
        about_button.place(x=10, y=665)

    def show_about_info(self):
        AboutWindow(self.root)

    # ----------------------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------- Experimental Data Core: Repository & User Input --------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------------------------

    # ---------------------------------------- First Window of the Experimental Data Core: Options -------------------------------------------
    def exp_data_options(self):
        # Store the applied geometry for reuse
        self.root.update_idletasks()
        gm.set_last_geometry(self.root.geometry())
        # Destroy previous Window
        self.clear_window()
        # Call class which defines the new window design and functionality
        ExpDataOptions(self.root, self.open_project_info, self.data_mat_repository, self.open_main_window)

    # ------------------------------------------------------- Data Repository Branch ---------------------------------------------------------
    def data_mat_repository(self):
        # Store the applied geometry for reuse
        self.root.update_idletasks()
        gm.set_last_geometry(self.root.geometry())
        # Destroy previous Window
        self.clear_window()
        # Call class which defines the new window design and functionality
        MatRepositoryWindow(self.root, self.exp_data_options, self.rep_data_plt_confirm, self.open_data_info)

    def open_data_info(self, selected_data=None):
        # Store the applied geometry for reuse
        self.root.update_idletasks()
        gm.set_last_geometry(self.root.geometry())
        # Destroy previous Window
        self.clear_window()
        # Call class which defines the new window design and functionality
        ChosenExpDataInfo(self.root, self.data_mat_repository, self.open_access_data, selected_data)

    def open_access_data(self, selected_data):
        # Store the applied geometry for reuse
        self.root.update_idletasks()
        gm.set_last_geometry(self.root.geometry())
        # Destroy previous Window
        self.clear_window()
        # Call class which defines the new window design and functionality
        AccessExpDataWindow(self.root,self.data_mat_repository,self.repository_data_plt, selected_data)

    def repository_data_plt(self, selected_data):
        # Store the applied geometry for reuse
        self.root.update_idletasks()
        gm.set_last_geometry(self.root.geometry())
        # Destroy previous Window
        self.clear_window()
        # Call class which defines the new window design and functionality
        RepDataPlotWindow(self.root,self.data_mat_repository, selected_data)

    def rep_data_plt_confirm(self, material, input_status):
        # Store the applied geometry for reuse
        self.root.update_idletasks()
        gm.set_last_geometry(self.root.geometry())
        # Destroy previous Window
        self.clear_window()
        # Call class which defines the new window design and functionality
        RepDataPlotConfirmWindow(self.root, self.data_mat_repository, self.open_model_first_window, material, input_status)
    
    # ------------------------------------------------------ User Data Input Branch ----------------------------------------------------------
    def open_project_info(self):
        # Store the applied geometry for reuse
        self.root.update_idletasks()
        gm.set_last_geometry(self.root.geometry())
        # Destroy previous Window
        self.clear_window()
        ProjectInfoWindow(self.root, self.open_experimental_data_input, self.exp_data_options)

    def open_experimental_data_input(self, material, input_status):
        # Store the applied geometry for reuse
        self.root.update_idletasks()
        gm.set_last_geometry(self.root.geometry())
        # Destroy previous Window
        self.clear_window()
        ExperimentalDataWindow(self.root, material, self.open_graph_display_of_data, self.open_project_info, input_status)

    def open_graph_display_of_data(self, material, input_status):
        # Store the applied geometry for reuse
        self.root.update_idletasks()
        gm.set_last_geometry(self.root.geometry())
        # Destroy previous Window
        self.clear_window()
        DataInputVisualisation(self.root, material, self.open_model_first_window, self.open_experimental_data_input, input_status)

    # ----------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------- Hyperelastic Model Selection Core --------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------------------------  

    # ---------------------------------- First Window of the Hyperelastic Model Selection Core: Options --------------------------------------

    def open_model_first_window(self, material, input_status):
        # Store the applied geometry for reuse
        self.root.update_idletasks()
        gm.set_last_geometry(self.root.geometry())
        # Destroy previous Window
        self.clear_window()
        ModelingChoice(self.root, material, self.open_model_options_window, self.exp_data_options, input_status)

    # -------------------------------------------------- Library of Hyperelastic Models ------------------------------------------------------
    
    def open_model_options_window(self, material):
        # Store the applied geometry for reuse
        self.root.update_idletasks()
        gm.set_last_geometry(self.root.geometry())
        # Destroy previous Window
        self.clear_window()
        OptionsOfModels(self.root, material)
    
    

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
