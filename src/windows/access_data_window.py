# access_data_window.py

import tkinter as tk
from tkinter import scrolledtext
from helpers.image_display import ImageDisplay
import helpers.geometry_manager as gm
from helpers.path_helpers import resolve_path

class AccessExpDataWindow:
    def __init__(self, root, proceed_callback_back, proceed_callback_graph_plt, selected_data):
        self.root = root
        self.proceed_callback_back = proceed_callback_back
        self.proceed_callback_graph_plt = proceed_callback_graph_plt
        self.selected_data = selected_data
        self.root.title("Material Experimental Data to be Accessed")

        # Restore previous geometry if available
        geom = gm.get_centered_geometry(gm.get_last_geometry(), 1200, 700)
        self.root.geometry(geom)

        # Logo adjusted place
        image_path = resolve_path("assets/logos/Logo_HyperSmart.png")             
        ImageDisplay(self.root, image_path, (300, 300), x=450, y=25)

        # Mapping modes and positions
        modes = ["axial", "biaxial", "simple_shear", "pure_shear"]
        labels = ["Axial Data", "Biaxial Data", "Simple Shear", "Pure Shear"]
        base_x = 90
        spacing = 260
        y_label = 105
        y_textbox = 130
        y_button = 600

        # Create widgets for each mode
        for i, mode in enumerate(modes):
            x_pos = base_x + i * spacing
            self.display_data_mode(mode, labels[i], x_pos, y_label, y_textbox, y_button)

        # Label with note about how to handle data
        noteLabel = tk.Label(self.root, text="Note: the copied data is best handled by text editors that "
                             "work well with basic .txt files, such as Windows Notepad, Notepad++, Visual Studio Code, PSPad, etc.", 
                             font=("TkDefaultFont", 11), fg="black", bg="white")
        noteLabel.place(x=10, y=670)

        # Add "plot_graphs" button
        plt_graph_button = tk.Button(self.root, text="Plot Data", command=lambda: self.proceed_callback_graph_plt(self.selected_data))
        plt_graph_button.place(x=1130, y=665)

        # Add "Back" button
        back_button = tk.Button(self.root, text="Back", command=self.proceed_callback_back)
        back_button.place(x=1090, y=665)

    def display_data_mode(self, mode, label_text, label_x, label_y, text_box_y, button_y):
        data = self.selected_data.get("data", {}).get(mode, None)

        # Label
        label = tk.Label(self.root, text=label_text, font=("Arial", 12, "bold"), bg="white")
        label.place(x=label_x + 40, y=label_y)

        if data:
            # Try to get the x-axis with different names
            x_vals = (
                data.get("stretch") or
                data.get("strain") or
                data.get("gamma") or
                data.get("shear_parameter") or
                []
            )
            y_vals = data.get("stress", [])

            # Textbox
            text_box = scrolledtext.ScrolledText(self.root, width=20, height=28, font=("Courier", 10))
            for x, y in zip(x_vals, y_vals):
                try:
                    text_box.insert(tk.END, f"{float(x):.5f}\t{float(y):.5f}\n")
                except ValueError:
                    continue
            text_box.configure(state='normal')
            text_box.place(x=label_x, y=text_box_y)

            # "Copy" button
            copy_button = tk.Button(self.root, text="Copy", command=lambda box=text_box: self.copy_text(box))
            copy_button.place(x=label_x + 65, y=button_y)

            # Context Menu
            self.add_context_menu(text_box)
        else:
            no_data_label = tk.Label(self.root, text="No data available for this mode.", fg="red", font=("Arial", 10, "italic"))
            no_data_label.place(x=label_x, y=text_box_y + 10)

    def copy_text(self, text_widget):
        self.root.clipboard_clear()
        self.root.clipboard_append(text_widget.get("1.0", tk.END))
        self.root.update()  # Ensures content is available on the clipboard

    def add_context_menu(self, widget):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Copy", command=lambda: widget.event_generate("<<Copy>>"))

        def show_context_menu(event):
            widget.focus()
            menu.post(event.x_root, event.y_root)

        widget.bind("<Button-3>", show_context_menu)  # Right button of the mouse

    