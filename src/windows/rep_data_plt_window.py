# rep_data_plt_window.py

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from helpers.image_display import ImageDisplay
import helpers.geometry_manager as gm
from helpers.path_helpers import resolve_path

class RepDataPlotWindow:
    def __init__(self, root, proceed_callback_back, selected_data):
        self.root = root
        self.proceed_callback_back = proceed_callback_back
        self.selected_data = selected_data
        self.root.title("Graphical Plotting of the Chosen Experimental Data")
        self.root.configure(bg='white')
        
        # Restore previous geometry if available
        geom = gm.get_centered_geometry(gm.get_last_geometry(), 900, 700)
        self.root.geometry(geom)

        # Display the main logo image
        image_path = resolve_path("assets/logos/Logo_HyperSmart.png")             
        ImageDisplay(self.root, image_path, (300, 300), x=300, y=25)

        stress_measure = self.selected_data.get("stress_measure", "Stress")
        units = self.selected_data.get("unit_of_measure", {})
        data = self.selected_data.get("data", {})

        # Uniaxial Tension/Compression
        title1 = tk.Label(self.root, text='Uniaxial Tension/Compression', font=("Arial", 14), fg="black", bg="white")
        title1.place(x=100, y=90)
        self.plot_graph_or_message(data.get("axial"), "Stretch (λ₁)", stress_measure, units.get("axial", ""), 30, 120)

        # Equi-Biaxial Loading
        title2 = tk.Label(self.root, text='Equi-Biaxial Loading', font=("Arial", 14), fg="black", bg="white")
        title2.place(x=590, y=90)
        self.plot_graph_or_message(data.get("biaxial"), "Stretch (λ₁)", stress_measure, units.get("biaxial", ""), 480, 120)

        # Simple Shear
        title3 = tk.Label(self.root, text='Simple Shear', font=("Arial", 14), fg="black", bg="white")
        title3.place(x=170, y=380)
        self.plot_graph_or_message(data.get("simple_shear"), "Shear Parameter (γ₁₂)", stress_measure, units.get("simple_shear", ""), 30, 410)

        # Pure Shear
        title4 = tk.Label(self.root, text='Pure Shear', font=("Arial", 14), fg="black", bg="white")
        title4.place(x=630, y=380)
        self.plot_graph_or_message(data.get("pure_shear"), "Shear Parameter (γ₁₂)", stress_measure, units.get("pure_shear", ""), 480, 410)

        # Back Button
        back_button = tk.Button(self.root, text="Back", command=self.proceed_callback_back)
        back_button.place(x=855, y=665)
        
    def plot_graph_or_message(self, mode_data, x_label, stress_measure, unit, x, y):
        if mode_data:
            x_vals = (
                mode_data.get("stretch") or
                mode_data.get("strain") or
                mode_data.get("gamma") or
                mode_data.get("shear_parameter") or
                []
            )
            y_vals = mode_data.get("stress", [])
            if x_vals and y_vals:
                fig = Figure(figsize=(6, 5), dpi=100, constrained_layout=True)
                ax = fig.add_subplot(111)
                ax.plot(x_vals, y_vals, 'o', markerfacecolor='none')
                ax.set_xlabel(x_label, labelpad=10)

                # Determine stress component symbol
                if x_label == "Stretch (λ₁)":
                    stress_component = "σ₁₁" if self.selected_data.get("stress_measure") == "Cauchy" else "P₁₁"
                elif x_label == "Shear Parameter (γ₁₂)":
                    stress_component = "σ₁₂" if self.selected_data.get("stress_measure") == "Cauchy" else "P₁₂"
                else:
                    stress_component = ""

                # Ensure full name of stress measure
                if stress_measure == "Cauchy":
                    stress_name = "Cauchy Stress"
                elif stress_measure == "Nominal":
                    stress_name = "Nominal Stress"
                else:
                    stress_name = stress_measure

                # Final y-axis label
                if unit:
                    y_label = f"{stress_name} ({stress_component}) [{unit}]"
                else:
                    y_label = f"{stress_name} ({stress_component})"

                ax.set_ylabel(y_label, labelpad=10)
                ax.grid(True)

                canvas = FigureCanvasTkAgg(fig, master=self.root)
                canvas.draw()
                canvas.get_tk_widget().place(x=x, y=y, width=350, height=250)
                return

        # If no data or empty
        msg = tk.Label(self.root, text='Empty Data', font=("Helvetica", 10), fg="red", bg="white")
        msg.place(x=x + 165, y=y + 90)

