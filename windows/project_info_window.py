import tkinter as tk
from tkinter import ttk
from image_display import ImageDisplay
from data_center import ExperimentalData
from windows.experimental_data_input import ExperimentalDataWindow

class ProjectInfoWindow:
    def __init__(self, root, proceed_callback):
        self.root = root
        self.proceed_callback = proceed_callback
        self.root.title("Stress Measure Selection")
        self.root.geometry("500x700")

        # Display the main logo
        ImageDisplay(self.root, 'Logo_HyperSmart.png', (300, 300), x=100, y=25)

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

        # Next button to submit the material name
        next_button = tk.Button(self.root, text="Next", command=self.proceed)
        next_button.place(x=450, y=665)
    
    def proceed(self):
        # Create/Initialize a Material object 
        material = ExperimentalData() 

        # Assign material name from the entry widget
        material_name = self.material_name_entry.get()
        material.assign_material_name(material_name)

        # Assign the stress measure based on user selection
        stress_measure = 0 if self.stress_measure_var.get() == "Nominal Stress" else 1
        material.assign_stress_measure('stress_measure', stress_measure)

        # Call the proceed callback to open the next window
        self.proceed_callback(material)
