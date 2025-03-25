# mat_repository_window.py

import tkinter as tk
import os
import yaml
from image_display import ImageDisplay

class MatRepositoryWindow:
    def __init__(self, root, proceed_callback_next, proceed_callback_info):
        self.root = root
        self.proceed_callback_next = proceed_callback_next  
        self.proceed_callback_info = proceed_callback_info  
        self.root.title("Repository of Experimental Data")
        self.root.geometry("500x700")

        # Display the main logo
        ImageDisplay(self.root, 'Logo_HyperSmart.png', (300, 300), x=100, y=25)

        # Display text that asks for the user to choose experimental data
        ask_to_choose = tk.Label(self.root, text="Click the chosen experimental data", font=("Arial", 13), fg="black", bg="white")
        ask_to_choose.place(x=120, y=120)

        # Frame for listbox and scrollbar
        frame = tk.Frame(self.root)
        frame.place(x=50, y=150)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        
        # Create a listbox to display available materials
        self.listbox = tk.Listbox(frame, width=66, height=28, yscrollcommand=scrollbar.set)
        
        # Configure scrollbar
        scrollbar.config(command=self.listbox.yview)
        
        # Pack listbox and scrollbar
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Load the YAML files and display available materials
        self.load_materials()

        # Add "Done" button
        done_button = tk.Button(self.root, text="Done!", command=self.proceed_callback_next)
        done_button.place(x=445, y=665)

        # Add "View Data Info" button
        view_data_button = tk.Button(self.root, text="View Data Info", command=self.view_selected_data)
        view_data_button.place(x=350, y=665)

    def load_materials(self):
        """Load materials from YAML files in the 'material_repository' folder and display them."""
        repo_path = "material_repository"
        
        if not os.path.exists(repo_path):
            return

        self.materials = {}

        for filename in os.listdir(repo_path):
            if filename.endswith((".yaml", ".yml")):
                filepath = os.path.join(repo_path, filename)
                
                with open(filepath, "r", encoding="utf-8") as file:
                    try:
                        data = yaml.safe_load(file)
                        material = data.get("material", "Unknown Material")
                        author = data.get("author", "Unknown Author")
                        year = data.get("year", "Unknown Year")
                        
                        material_entry = f"{material} [{author}] ({year})"
                        
                        self.listbox.insert(tk.END, material_entry)
                        self.materials[material_entry] = data
                    except yaml.YAMLError:
                        pass
                    except Exception:
                        pass

        self.listbox.update_idletasks()

    def view_selected_data(self):
        """Handle selection and open the experimental data window."""
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_text = self.listbox.get(selected_index)
            selected_data = self.materials[selected_text]
            
            # Pass selected data to the main controller
            self.proceed_callback_info(selected_data)
