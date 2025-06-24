# model_first_window.py
import tkinter as tk
from helpers.image_display import ImageDisplay
import helpers.geometry_manager as gm
from helpers.path_helpers import resolve_path

class ModelingChoice:
    def __init__(self, root, material, proceed_callbak_foward, proceed_callback_back, input_status):
        self.root = root
        self.material = material
        self.input_status = input_status
        self.proceed_callback_foward = proceed_callbak_foward
        self.proceed_callback_back = proceed_callback_back
        self.root.title("Defining Hyperelastic Model")

        # Restore previous geometry if available
        geom = gm.get_centered_geometry(gm.get_last_geometry(), 500, 700)
        self.root.geometry(geom)

        self.root.configure(bg='white')

        # Display the main logo image
        image_path = resolve_path("assets/logos/Logo_HyperSmart.png")             
        ImageDisplay(self.root, image_path, (300, 300), x=100, y=25)

        # Create the button to ask help to define the best hyperelastic model 
        help_choose_model_button = tk.Button(self.root, text='Help me define the best hyperelastic model to represent my material', width=55, height=1, justify="center")
        help_choose_model_button.place(x=54, y=300)

        # Create button to ask for help calibrating hyperelastic model already chosen
        help_calibration_button = tk.Button(self.root, text='I already chose the most appropriate hyperelastic model;\n Help me calibrate its material parameters', width=55, height=2, justify="center",command=self.open_options_window)
        help_calibration_button.place(x=54, y=360)

        # Create button to go back to previous window
        back_button = tk.Button(self.root, text="Back", command=self.proceed_callback_back) 
        back_button.place(x=450, y=665)

    def open_options_window(self):
        """Call the callback function to open OptionsOfModels window."""
        self.proceed_callback_foward(self.material)

