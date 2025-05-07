# graph_display_of_data.py

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from auxiliary_py_modules.image_display import ImageDisplay
from auxiliary_py_modules.data_center import ExperimentalData
from windows.experimental_data_input import ExperimentalDataWindow

class DataInputVisualisation:
    def __init__(self, root, material, proceed_callback, go_back_callback):
        self.root = root
        self.material = material
        self.proceed_callback = proceed_callback
        self.go_back = go_back_callback
        self.root.title("Data Input Graphical Visualisation")
        self.center_window(900, 760)
        self.root.configure(bg='white')

        # Display the main logo image
        ImageDisplay(self.root, 'Logo_HyperSmart.png', (300, 300), x=300, y=25)

        # Get experimental data 
        sae_stretch = material.get_vector('sae_stretch')
        sae_stress = material.get_vector('sae_stress')
        ebl_stretch = material.get_vector('ebl_stretch')
        ebl_stress = material.get_vector('ebl_stress')
        ss_shear_parameter = material.get_vector('ss_shear_parameter')
        ss_stress = material.get_vector('ss_stress')
        ps_shear_parameter = material.get_vector('ps_shear_parameter')
        ps_stress = material.get_vector('ps_stress')

        # Uniaxial Tension/Compression
        title1 = tk.Label(self.root, text='Uniaxial Tension/Compression', font=("Arial", 14), fg="black", bg="white")
        title1.place(x=100, y=120)
        if sae_stretch.size == 0 and sae_stress.size == 0:
            label1 = tk.Label(self.root, text='Empty Data', font=("Helvetica", 10), fg="red", bg="white")
            label1.place(x=195, y=240)
        else:
            fig = Figure(figsize=(6, 5), dpi=100, constrained_layout=True)  # Increase size and use constrained_layout
            ax = fig.add_subplot(111)
            ax.plot(sae_stretch, sae_stress, 'o', markerfacecolor='none')
            ax.set_xlabel('Stretch (λ₁)', labelpad=10)  # Add padding
            ax.set_ylabel('Stress (σ₁₁)', labelpad=10)
            ax.grid(True)
            # Embed plot
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().place(x=30, y=150, width=350, height=250)

        # Equi-Biaxial Loading
        title2 = tk.Label(self.root, text='Equi-Biaxial Loading', font=("Arial", 14), fg="black", bg="white")
        title2.place(x=590, y=120)
        if ebl_stretch.size == 0 and ebl_stress.size == 0:
            label2 = tk.Label(self.root, text='Empty Data', font=("Helvetica", 10), fg="red", bg="white")
            label2.place(x=645, y=250)
        else:
            fig = Figure(figsize=(6, 5), dpi=100, constrained_layout=True)  # Increase size and use constrained_layout
            ax = fig.add_subplot(111)
            ax.plot(ebl_stretch, ebl_stress, 'o', markerfacecolor='none')
            ax.set_xlabel('Stretch (λ₁)', labelpad=10)  # Add padding
            ax.set_ylabel('Stress (σ₁₁)', labelpad=10)
            ax.grid(True)
            # Embed plot
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().place(x=480, y=150, width=350, height=250)

        # Simple Shear
        title3 = tk.Label(self.root, text='Simple Shear', font=("Arial", 14), fg="black", bg="white")
        title3.place(x=170, y=420)
        if  ss_shear_parameter.size == 0 and ss_stress.size == 0:
            label3 = tk.Label(self.root, text='Empty Data', font=("Helvetica", 10), fg="red", bg="white")
            label3.place(x=195, y=550)
        else:
            fig = Figure(figsize=(6, 5), dpi=100, constrained_layout=True)  # Increase size and use constrained_layout
            ax = fig.add_subplot(111)
            ax.plot(ss_shear_parameter, ss_stress, 'o', markerfacecolor='none')
            ax.set_xlabel('Shear Parameter (γ₁₂)', labelpad=10)  # Add padding
            ax.set_ylabel('Shear Stress (σ₁₂)', labelpad=10)
            ax.grid(True)
            # Embed plot
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().place(x=30, y=450, width=350, height=250)

        # Pure Shear
        title4 = tk.Label(self.root, text='Pure Shear', font=("Arial", 14), fg="black", bg="white")
        title4.place(x=630, y=420)
        if  ps_shear_parameter.size == 0 and ps_stress.size == 0:
            label4 = tk.Label(self.root, text='Empty Data', font=("Helvetica", 10), fg="red", bg="white")
            label4.place(x=645, y=550)
        else:
            fig = Figure(figsize=(6, 5), dpi=100, constrained_layout=True)  # Increase size and use constrained_layout
            ax = fig.add_subplot(111)
            ax.plot(ps_shear_parameter, ps_stress, 'o', markerfacecolor='none')
            ax.set_xlabel('Shear Parameter (γ₁₂)', labelpad=10)  # Add padding
            ax.set_ylabel('Shear Stress (σ₁₂)', labelpad=10)
            ax.grid(True)
            # Embed plot
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().place(x=480, y=450, width=350, height=250)

        # Add "Confirm" button
        confirm_button = tk.Button(self.root, text="Confirm Data Input!", command=lambda: self.proceed(material))
        confirm_button.place(x=770, y=725)

        # Add "Correct/Add Data Input"
        go_back_button = tk.Button(self.root, text="Correct/Add Data", command=lambda: self.go_back(material))
        go_back_button.place(x=660, y=725)

    def proceed(self, material):
        # Call the proceed callback to open the next window
        self.proceed_callback(material)

    def go_back(self, material):
        # Call the go_back callback to return to the previous window 
        self.go_back_callback(material)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - width / 2)
        center_y = int(screen_height / 2 - ((height + 80)/ 2))
        self.root.geometry(f'{width}x{height}+{center_x}+{center_y}')
