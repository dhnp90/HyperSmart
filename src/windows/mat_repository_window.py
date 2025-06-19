# mat_repository_window.py

import tkinter as tk
from tkinter import messagebox
import os
import yaml
from helpers.image_display import ImageDisplay
from helpers.hover_over_btn import Tooltip
import helpers.geometry_manager as gm
from helpers.path_helpers import resolve_path

VALID_CLASSES_AND_SUBCLASSES = {
    "Elastomers": [
        "Natural Rubber (NR)",
        "Synthetic Rubbers",
        "Silicone Rubbers (Q)",
        "Polyurethanes (PU)",
        "Thermoplastic Elastomers (TPE)",
        "Others/Hybrid/Specialty Elastomers"
    ],
    "Foams": [
        "Polymeric Open-Cell Foams",
        "Polymeric Closed-Cell Foams",
        "Others"
    ],
    "Soft Biological Tissues": [
        "Human",
        "Animal",
        "Others"
    ],
    "Gels & Hydrogels": [
        "Natural Polymer-Based",
        "Synthetic Polymer-Based",
        "Composite/Hybrid",
        "Others"
    ]
}

class MatRepositoryWindow:
    def __init__(self, root, proceed_callback_back, proceed_callback_next, proceed_callback_info):
        self.root = root
        self.proceed_callback_back = proceed_callback_back
        self.proceed_callback_next = proceed_callback_next  
        self.proceed_callback_info = proceed_callback_info  
        self.root.title("Repository of Experimental Data")

        # Restore previous geometry 
        geom = gm.get_centered_geometry(gm.get_last_geometry(), 500, 700)
        self.root.geometry(geom)

        # Display the main logo
        image_path = resolve_path("assets/logos/Logo_HyperSmart.png")             
        ImageDisplay(self.root, image_path, (300, 300), x=100, y=25)

        custom_font = "TkDefaultFont"
        bold_font = (custom_font, 10, 'bold')

        ask_to_choose = tk.Label(self.root, text="Click the chosen experimental data:", font=bold_font, fg="black", bg="white")
        ask_to_choose.place(x=48, y=128)

        # Dropdown for material class
        self.class_var = tk.StringVar()
        self.class_menu = tk.OptionMenu(self.root, self.class_var, *VALID_CLASSES_AND_SUBCLASSES.keys(), command=self.update_subclass_menu)
        self.class_var.set("Select Material Class")
        self.class_menu.place(x=50, y=150)

        # Dropdown for material subclass
        self.subclass_var = tk.StringVar()
        self.subclass_menu = tk.OptionMenu(self.root, self.subclass_var, '')
        self.subclass_var.set("Select Material Subclass")
        self.subclass_menu.place(x=250, y=150)

        # Frame for listbox and scrollbar
        frame = tk.Frame(self.root)
        frame.place(x=50, y=200)

        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(frame, width=66, height=26, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.materials = {}
        self.grouped_materials = {}
        self.load_materials()

        # Trace selection changes to update the listbox
        self.class_var.trace("w", lambda *args: self.filter_materials())
        self.subclass_var.trace("w", lambda *args: self.filter_materials())

        # Add Buttons
        done_button = tk.Button(self.root, text="Done!", command=self.proceed_callback_next)
        done_button.place(x=445, y=665)
        Tooltip(done_button, text="Click here if you want to use the selected experimental data on the calibration.")

        view_data_button = tk.Button(self.root, text="View Data Info", command=self.view_selected_data)
        view_data_button.place(x=355, y=665)
        Tooltip(view_data_button, text="Click to see detailed information about the selected experimental data.")

        back_button = tk.Button(self.root, text="Back", command=self.proceed_callback_back)
        back_button.place(x=315, y=665)

    def update_subclass_menu(self, selected_class):
        menu = self.subclass_menu['menu']
        menu.delete(0, 'end')
        for subclass in VALID_CLASSES_AND_SUBCLASSES[selected_class]:
            menu.add_command(label=subclass, command=tk._setit(self.subclass_var, subclass))
        self.subclass_var.set("Select Material Subclass")

    def load_materials(self):
        repo_path = resolve_path("material_repository")
        if not os.path.exists(repo_path):
            return

        for filename in os.listdir(repo_path):
            if filename.endswith((".yaml", ".yml")):
                filepath = os.path.join(repo_path, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    try:
                        data = yaml.safe_load(file)
                        material = data.get("material", "Unknown Material")
                        author = data.get("author", "Unknown Author")
                        year = data.get("year", "Unknown Year")
                        mclass = data.get("material_class")
                        msubclass = data.get("material_subclass")

                        # Validate class and subclass
                        if mclass not in VALID_CLASSES_AND_SUBCLASSES:
                            raise ValueError(f"Invalid material_class: {mclass}")
                        if msubclass not in VALID_CLASSES_AND_SUBCLASSES[mclass]:
                            raise ValueError(f"Invalid material_subclass '{msubclass}' for class '{mclass}'")

                        entry = f"{material} [{author}] ({year})"
                        self.grouped_materials.setdefault((mclass, msubclass), []).append((entry, data))
                    except Exception as e:
                        messagebox.showerror("YAML Error", f"Error in file: {filename}\n{e}\n\nValid material classes:\n" +
                                             "\n".join([f"- {cls}: {', '.join(subs)}" for cls, subs in VALID_CLASSES_AND_SUBCLASSES.items()]))

    def filter_materials(self):
        self.listbox.delete(0, tk.END)
        selected_class = self.class_var.get()
        selected_subclass = self.subclass_var.get()

        key = (selected_class, selected_subclass)
        if key in self.grouped_materials:
            for entry, data in sorted(self.grouped_materials[key]):
                self.listbox.insert(tk.END, entry)
                self.materials[entry] = data

    def view_selected_data(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_text = self.listbox.get(selected_index)
            selected_data = self.materials.get(selected_text)
            if selected_data:
                self.proceed_callback_info(selected_data)
