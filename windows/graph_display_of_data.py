# graph_display_of_data.py
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from image_display import ImageDisplay
from data_center import ExperimentalData

class DataInputVisualisation:
    def __init__(self, root, material):
        self.root = root
        self.material = material
        self.root.title("Data Input Graphical Visualisation")
        self.center_window(900, 700)
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
        if sae_stretch.size == 0 and sae_stress.size == 0:
            label1 = tk.Label(self.root, text='Empty Data', font=("Helvetica", 10), fg="red", bg="white")
            label1.place(x=150, y=200)
        else:
            fig = Figure(figsize=(6, 5), dpi=100, constrained_layout=True)  # Increase size and use constrained_layout
            ax = fig.add_subplot(111)
            ax.plot(sae_stretch, sae_stress, 'o', markerfacecolor='none')
            ax.set_xlabel('Stretch', labelpad=10)  # Add padding
            ax.set_ylabel('Stress', labelpad=10)
            ax.set_title('Uniaxial Tension/Compression')

            # Embed plot
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().place(x=30, y=150, width=350, height=250)


    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - width / 2)
        center_y = int(screen_height / 2 - height / 2)
        self.root.geometry(f'{width}x{height}+{center_x}+{center_y}')
    
    

