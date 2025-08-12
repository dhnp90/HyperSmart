import tkinter as tk
from tkinter import ttk
import os
import yaml
from helpers.image_display import ImageDisplay
import helpers.geometry_manager as gm
from helpers.path_helpers import resolve_path

class OptionsOfModels:
    def __init__(self, root, material, proceed_callback_info, proceed_callback_back, proceed_callback_next):
        self.root = root
        self.material = material
        self.proceed_callback_info = proceed_callback_info
        self.proceed_callback_back = proceed_callback_back
        self.proceed_callback_next = proceed_callback_next
        self.root.title("Options of Hyperelastic Model")

        # Restore previous geometry if available
        geom = gm.get_centered_geometry(gm.get_last_geometry(), 500, 700)
        self.root.geometry(geom)
        self.root.configure(bg='white')

        # Display the main logo image
        image_path = resolve_path("assets/logos/Logo_HyperSmart.png")             
        ImageDisplay(self.root, image_path, (300, 300), x=100, y=25)

        # Configure style for radiobuttons to have a white background
        self.style = ttk.Style()
        self.style.configure("Custom.TRadiobutton", background="white", foreground="black")

        # Label to instruct the user to choose the hyperelastic model
        label1 = tk.Label(self.root, text="Define the hyperelastic model to use:", font=("TkDefaultFont", 14), fg="black", bg="white")
        label1.place(x=20, y=110)

        # Create a frame with a scrollbar to hold all model options
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(pady=150, padx=20, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame, bg='white')
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Variable to store the selected model name
        self.selected_model = tk.StringVar(value="")

        # Dictionary to store the full content of each model YAML
        self.model_data_dict = {}

        # Dynamically add model options
        self.add_model_options(scrollable_frame)

        # Buttons
        next_button = tk.Button(self.root, text="Next", command=self.next_step)
        next_button.place(x=450, y=665)

        back_button = tk.Button(self.root, text="Back", command=lambda: self.proceed_callback_back(self.material))
        back_button.place(x=335, y=665)

        model_info_btn = tk.Button(self.root, text="Model Info", command=self.info_request)
        model_info_btn.place(x=375, y=665)

    def add_model_options(self, parent):
        """Reads .yaml files and adds model options grouped by model_class."""
        model_dir = resolve_path("hyperelastic_models")
        grouped_models = {}

        if os.path.isdir(model_dir):
            for filename in os.listdir(model_dir):
                if filename.endswith((".yaml", ".yml")):
                    file_path = os.path.join(model_dir, filename)
                    try:
                        with open(file_path, "r", encoding="utf-8") as file:
                            data = yaml.safe_load(file)
                            model_name = data.get("model_name")
                            model_class = data.get("model_class")

                            if model_name and model_class:
                                grouped_models.setdefault(model_class, []).append(model_name)
                                self.model_data_dict[model_name] = data
                    except Exception as e:
                        print(f"Failed to read {filename}: {e}")

        for category, models in grouped_models.items():
            tk.Label(parent, text=category, font=("Arial", 10, "bold"), bg='white', anchor="w").pack(fill="x", pady=(10, 5))
            for model in sorted(models):
                ttk.Radiobutton(
                    parent, text=model,
                    variable=self.selected_model,
                    value=model,
                    style="Custom.TRadiobutton"
                ).pack(anchor="w", padx=20, pady=2)

    def next_step(self):
        """Function to handle when the Next button is clicked."""
        selected = self.selected_model.get()
        if selected:
            model_data = self.model_data_dict.get(selected)
            if model_data:
                self.proceed_callback_next(self.material, model_data)
            else:
                print(f"Model data not found for: {selected}")
        else:
            print("No model selected. Please choose one.")

    def info_request(self):
        """Function to handle when the Model Info button is clicked."""
        selected = self.selected_model.get()
        if selected:
            model_data = self.model_data_dict.get(selected)
            if model_data:
                self.proceed_callback_info(self.material, model_data)
            else:
                print(f"Model data not found for: {selected}")
        else:
            print("No model selected.")
