import tkinter as tk
from tkinter import messagebox
import numpy as np
from data_center import ExperimentalData

class ExperimentalDataInputWindow:
    def __init__(self, root, material, vector_names, on_assign_callback):
        self.root = root
        self.material = material
        self.vector_names = vector_names
        self.on_assign_callback = on_assign_callback  # Store the callback function

        self.root.title("Excel to NumPy Vectors")
        self.root.geometry("450x600")

        # Create a label with instructions
        instructions = tk.Label(self.root, text="Data Input \n(Excel Copy/Paste Available)", font=("Helvetica", 11), wraplength=500)
        instructions.pack(pady=12)

        # Add labels
        if vector_names == ("sae_stretch", "sae_stress"):
            label_x = tk.Label(self.root, text="Stretch (λ₁)", font=("Segoe UI Symbol", 9, "bold"))
            label_x.place(x=80, y=62)
            label_y = tk.Label(self.root, text="Axial Stress (σ₁₁)", font=("Segoe UI Symbol", 9, "bold"))
            label_y.place(x=260, y=62)
        elif vector_names == ("ebl_stretch", "ebl_stress"):
            label_x = tk.Label(self.root, text="Stretch (λ₁)", font=("Segoe UI Symbol", 9, "bold"))
            label_x.place(x=80, y=62)
            label_y = tk.Label(self.root, text="Axial Stress (σ₁₁)", font=("Segoe UI Symbol", 9, "bold"))
            label_y.place(x=260, y=62)
        elif vector_names == ("ss_shear_parameter", "ss_stress"):
            label_x = tk.Label(self.root, text="Shear Paramenter (γ₁₂)", font=("Segoe UI Symbol", 9, "bold"))
            label_x.place(x=45, y=62)
            label_y = tk.Label(self.root, text="Shear Stress (σ₁₂)", font=("Segoe UI Symbol", 9, "bold"))
            label_y.place(x=256, y=62)
        elif vector_names == ("ps_shear_parameter", "ps_stress"):
            label_x = tk.Label(self.root, text="Shear Paramenter (γ₁₂)", font=("Segoe UI Symbol", 9, "bold"))
            label_x.place(x=45, y=62)
            label_y = tk.Label(self.root, text="Shear Stress (σ₁₂)", font=("Segoe UI Symbol", 9, "bold"))
            label_y.place(x=256, y=62)

        # Create a frame for the text widgets and scrollbars
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        # Create text widgets for input
        # Left text widget and scrollbar
        self.text_widget1 = tk.Text(frame, height=28, width=18)
        self.text_widget1.pack(side=tk.LEFT, padx=10)  # Keep existing padding
        scrollbar1 = tk.Scrollbar(frame, command=self.text_widget1.yview)
        self.text_widget1.config(yscrollcommand=scrollbar1.set)
        scrollbar1.pack(side=tk.LEFT, fill=tk.Y)

        # Add a spacer frame to increase distance
        spacer = tk.Frame(frame, width=12)  # Adjust the width for the desired spacing
        spacer.pack(side=tk.LEFT)

        # Right text widget and scrollbar
        self.text_widget2 = tk.Text(frame, height=28, width=18)
        self.text_widget2.pack(side=tk.LEFT, padx=10)  # Keep existing padding
        scrollbar2 = tk.Scrollbar(frame, command=self.text_widget2.yview)
        self.text_widget2.config(yscrollcommand=scrollbar2.set)
        scrollbar2.pack(side=tk.LEFT, fill=tk.Y)

        # Create a button to convert input to NumPy vectors
        convert_button = tk.Button(self.root, text="Assign Values", command=self.convert_to_vectors)
        convert_button.pack(pady=6)

    def convert_to_vectors(self):
        try:
            input_text1 = self.text_widget1.get("1.0", tk.END).strip().replace(',', '.')
            input_values1 = [float(x) for x in input_text1.split()]
            vector1 = np.array(input_values1)

            input_text2 = self.text_widget2.get("1.0", tk.END).strip().replace(',', '.')
            input_values2 = [float(x) for x in input_text2.split()]
            vector2 = np.array(input_values2)

            # Assign values dynamically based on vector_names
            self.material.assign_vector(self.vector_names[0], vector1)
            self.material.assign_vector(self.vector_names[1], vector2)

            # Call the callback function to update the status labels
            self.on_assign_callback()

            # Close the window after assigning values
            self.root.destroy()

            messagebox.showinfo("Success", "Values assigned successfully!")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers separated by spaces.")
