import tkinter as tk
from tkinter import ttk
from image_display import ImageDisplay

class ProjectInfoWindow:
    def __init__(self, root, proceed_callback):
        self.root = root
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
        stress_measure_combobox['values'] = ("Cauchy Stress", "Nominal Stress")
        stress_measure_combobox.place(x=50, y=320, width=400)
        stress_measure_combobox.current(0)  # Set the default value

        # Next button to submit the material name
        next_button = tk.Button(self.root, text="Next", command=lambda: self.proceed_with_project_name(proceed_callback))
        next_button.place(x=450, y=665)
