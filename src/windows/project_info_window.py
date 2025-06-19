import tkinter as tk
from tkinter import ttk
from helpers.image_display import ImageDisplay
from helpers.data_center import ExperimentalData
from windows.experimental_data_input import ExperimentalDataWindow
from helpers.path_helpers import resolve_path
import helpers.geometry_manager as gm

class ProjectInfoWindow:
    def __init__(self, root, proceed_callback_next, proceed_callback_back):
        self.root = root
        self.proceed_callback_next = proceed_callback_next
        self.proceed_callback_back = proceed_callback_back
        self.root.title("Stress Measure Selection")

        # Restore previous geometry if available
        geom = gm.get_centered_geometry(gm.get_last_geometry(), 500, 700)
        self.root.geometry(geom)

        # Display the main logo
        image_path = resolve_path("assets/logos/Logo_HyperSmart.png")             
        ImageDisplay(self.root, image_path, (300, 300), x=100, y=25)

        # Add "Material" label and entry
        material_name_label = tk.Label(self.root, text="Material:", bg='white', font=("Helvetica", 10))
        material_name_label.place(x=50, y=250)
        self.material_name_entry = tk.Entry(self.root)
        self.material_name_entry.place(x=50, y=270, width=400)

        # Add "Choose the Stress Measure" label and combobox 
        stress_measure_label = tk.Label(self.root, text="Choose the Stress Measure:", bg='white', font=("Helvetica", 10))
        stress_measure_label.place(x=50, y=300)
        self.stress_measure_var = tk.StringVar(self.root)
        stress_measure_combobox = ttk.Combobox(self.root, textvariable=self.stress_measure_var)
        stress_measure_combobox['values'] = ("Nominal Stress", "Cauchy Stress")
        stress_measure_combobox.place(x=50, y=320, width=400)
        stress_measure_combobox.current(0)  # Set the default value

        # Add "Choose the Unit of Measurement" label and combobox 
        unit_label = tk.Label(self.root, text="Choose the Stress Measure:", bg='white', font=("Helvetica", 10))
        unit_label.place(x=50, y=350)
        self.unit_var = tk.StringVar(self.root)
        unit_combobox = ttk.Combobox(self.root, textvariable=self.unit_var)
        unit_combobox['values'] = ("MPa", "kPa")
        unit_combobox.place(x=50, y=370, width=400)
        unit_combobox.current(0)  # Set the default value

        # Next button to submit the material name
        next_button = tk.Button(self.root, text="Next", command=self.proceed)
        next_button.place(x=450, y=665)

        # Add "Back" button
        back_button = tk.Button(self.root, text="Back", command=self.proceed_callback_back)
        back_button.place(x=410, y=665)
    
    def proceed(self):
        # Create/Initialize a Material object 
        material = ExperimentalData() 

        # Assign material name from the entry widget
        material_name = self.material_name_entry.get()
        material.assign_material_name(material_name)

        # Assign the stress measure based on user selection
        stress_measure = 0 if self.stress_measure_var.get() == "Nominal Stress" else 1
        material.assign_stress_measure('stress_measure', stress_measure)

        # Assign the unit of measurement based on user selection
        unit_of_measurement = 0 if self.unit_var.get() == "MPa" else 1
        material.assign_unit('stress_measure', unit_of_measurement)

        # Reset input_status dictionary
        input_status = {
            "sae_stretch": False,
            "ebl_stretch": False,
            "ss_shear_parameter": False,
            "ps_shear_parameter": False
        }

        # Call the proceed callback to open the next window
        self.proceed_callback_next(material, input_status)