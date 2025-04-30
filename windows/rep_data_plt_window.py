# rep_data_plt_window.py

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from auxiliary_py_modules.image_display import ImageDisplay
import auxiliary_py_modules.geometry_manager as gm


class RepDataPlotWindow:
    def __init__(self, root, proceed_callback_back, selected_data):
        self.root = root
        self.proceed_callback_back = proceed_callback_back
        self.selected_data = selected_data
        self.root.title("Graphical Plotting of the Chosen Experimental Data")

        # Restore previous geometry if available
        geom = gm.get_centered_geometry(gm.get_last_geometry(), 1200, 700)
        self.root.geometry(geom)

        # Logo adjusted place
        ImageDisplay(self.root, 'Logo_HyperSmart.png', (300, 300), x=450, y=5)

        # Plot the available modes
        self.plot_fixed_positions()

        # Back Button
        back_button = tk.Button(self.root, text="Back", command=self.proceed_callback_back)
        back_button.place(x=1155, y=665)

    def plot_fixed_positions(self):
        # Define placement positions (x, y) for each plot/message
        placements = {
            "axial": (50, 150),
            "biaxial": (630, 150),
            "simple_shear": (50, 450),
            "pure_shear": (630, 450)
        }

        mode_labels = {
            "axial": "Axial",
            "biaxial": "Biaxial",
            "simple_shear": "Simple Shear",
            "pure_shear": "Pure Shear"
        }

        stress_measure = self.selected_data.get("stress_measure", "Stress")  # e.g., "Cauchy"
        units = self.selected_data.get("unit_of_measure", {})  # dictionary per mode

        for mode, (x, y) in placements.items():
            data = self.selected_data.get("data", {}).get(mode, None)
            if data:
                x_vals = (
                    data.get("stretch") or
                    data.get("strain") or
                    data.get("gamma") or
                    data.get("shear_parameter") or
                    []
                )
                y_vals = data.get("stress", [])

                if x_vals and y_vals:
                    fig = plt.Figure(figsize=(4.2, 4.0), dpi=100)
                    ax = fig.add_subplot(111)
                    ax.plot(x_vals, y_vals, marker='o', linestyle='-')
                    ax.set_title(f'{mode_labels[mode]} Data', fontsize=10)

                    # Y-axis label
                    unit = units.get(mode, "")
                    if unit and unit is not False:
                        y_label = f"{stress_measure} Stress [{unit}]"
                    else:
                        y_label = f"{stress_measure} Stress"
                    ax.set_ylabel(y_label, fontsize=9)

                    # X-axis label depending on mode
                    if mode in ["axial", "biaxial"]:
                        ax.set_xlabel("Stretch (λ)", fontsize=9)
                    else:
                        ax.set_xlabel("Shear Parameter (γ)", fontsize=9)

                    ax.tick_params(axis='both', labelsize=8)

                    # Ensure layout fits all labels
                    fig.tight_layout(rect=[0, 0.03, 1, 1])

                    canvas = FigureCanvasTkAgg(fig, master=self.root)
                    canvas.draw()
                    canvas_widget = canvas.get_tk_widget()
                    canvas_widget.place(x=x, y=y, width=520, height=220)
                else:
                    self._show_no_data_message(x, y)
            else:
                self._show_no_data_message(x, y)

    def _show_no_data_message(self, x, y):
        message = tk.Label(
            self.root,
            text="No available data",
            font=("Arial", 12),
            bg="white",
            fg="gray"
        )
        message.place(x=x, y=y, width=520, height=220)

