import tkinter as tk
from auxiliary_py_modules.image_display import ImageDisplay
from auxiliary_py_modules.data_center import ExperimentalData
from windows.input_window import ExperimentalDataInputWindow
import auxiliary_py_modules.geometry_manager as gm
from auxiliary_py_modules.path_helpers import resolve_path

class ExperimentalDataWindow:
    def __init__(self, root, material, proceed_callback_plot, proceed_callback_back, input_status):
        self.root = root
        self.proceed_callback_plot = proceed_callback_plot
        self.proceed_callback_back = proceed_callback_back
        self.material = material
        self.root.title("Experimental Data Input")

        # Restore previous geometry if available
        geom = gm.get_centered_geometry(gm.get_last_geometry(), 500, 700)
        self.root.geometry(geom)
        
        self.root.configure(bg='white')

        # Dictionary to track input status for each data type
        self.input_status = input_status

        # Dictionary to track buttons
        self.buttons = {}

        # Display the main logo
        image_path = resolve_path("assets/logos/Logo_HyperSmart.png")             
        ImageDisplay(self.root, image_path, (300, 300), x=100, y=25)

        # Display labels
        labels = ["Uniaxial Tension/Compression", "Equi-Biaxial Loading", "Simple Shear", "Pure Shear"]
        for i, text in enumerate(labels):
            label = tk.Label(self.root, text=text, font=("Helvetica", 10), anchor='w')
            label.place(x=20, y=300 + i * 50, width=325, height=25)

        # Add Data buttons and status labels
        self.add_data_button1 = tk.Button(self.root, text="Add Data", 
                                          command=lambda: self.open_data_input_window(("sae_stretch", "sae_stress")))
        self.add_data_button1.place(x=355, y=300, width=100, height=25)
        self.status_label1 = tk.Label(self.root, text="❌", fg="red", font=("Helvetica", 12))
        self.status_label1.place(x=465, y=300, width=20, height=25)
        self.buttons["sae_stretch"] = self.add_data_button1

        self.add_data_button2 = tk.Button(self.root, text="Add Data", 
                                          command=lambda: self.open_data_input_window(("ebl_stretch", "ebl_stress")))
        self.add_data_button2.place(x=355, y=350, width=100, height=25)
        self.status_label2 = tk.Label(self.root, text="❌", fg="red", font=("Helvetica", 12))
        self.status_label2.place(x=465, y=350, width=20, height=25)
        self.buttons["ebl_stretch"] = self.add_data_button2

        self.add_data_button3 = tk.Button(self.root, text="Add Data", 
                                          command=lambda: self.open_data_input_window(("ss_shear_parameter", "ss_stress")))
        self.add_data_button3.place(x=355, y=400, width=100, height=25)
        self.status_label3 = tk.Label(self.root, text="❌", fg="red", font=("Helvetica", 12))
        self.status_label3.place(x=465, y=400, width=20, height=25)
        self.buttons["ss_shear_parameter"] = self.add_data_button3

        self.add_data_button4 = tk.Button(self.root, text="Add Data", 
                                          command=lambda: self.open_data_input_window(("ps_shear_parameter", "ps_stress")))
        self.add_data_button4.place(x=355, y=450, width=100, height=25)
        self.status_label4 = tk.Label(self.root, text="❌", fg="red", font=("Helvetica", 12))
        self.status_label4.place(x=465, y=450, width=20, height=25)
        self.buttons["ps_shear_parameter"] = self.add_data_button4

        # Update status labels initially
        self.update_status_labels()

        # Add "Done" button
        done_button = tk.Button(self.root, text="Done!", command=lambda: self.proceed(material))
        done_button.place(x=450, y=665)

        # Add "Back" button
        back_button = tk.Button(self.root, text="Back", command=self.proceed_callback_back)
        back_button.place(x=410, y=665)

    def proceed(self, material):
        # Call the proceed callback to open the next window
        self.proceed_callback_plot(material)

    def open_data_input_window(self, vector_names):
        """Opens the ExperimentalDataInputWindow centered relative to the main window."""
        new_window = tk.Toplevel(self.root)  # Create a new window

        # Get main window position and dimensions
        self.root.update_idletasks()
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()

        # Define new window dimensions
        new_width = 450
        new_height = 600

        # Calculate center position
        new_x = main_x + (main_width // 2) - (new_width // 2)
        new_y = main_y + (main_height // 2) - (new_height // 2)

        # Set window position
        new_window.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}")

        # Define a callback function to update the status labels
        def on_assign_values():
            data_type = vector_names[0]  # e.g., "sae_stretch"
            self.input_status[data_type] = True  # Update the input status
            self.update_status_labels()  # Update the status labels

        # Pass the callback to the ExperimentalDataInputWindow
        ExperimentalDataInputWindow(new_window, self.material, vector_names, on_assign_values)

    def update_status_labels(self):
        """Updates the status labels based on the input status."""
        if self.input_status["sae_stretch"]:
            self.status_label1.config(text="✔️", fg="green")
            self.buttons["sae_stretch"].config(text="Change Data")
        else:
            self.status_label1.config(text="❌", fg="red")
            self.buttons["sae_stretch"].config(text="Add Data")

        if self.input_status["ebl_stretch"]:
            self.status_label2.config(text="✔️", fg="green")
            self.buttons["ebl_stretch"].config(text="Change Data")
        else:
            self.status_label2.config(text="❌", fg="red")
            self.buttons["ebl_stretch"].config(text="Add Data")

        if self.input_status["ss_shear_parameter"]:
            self.status_label3.config(text="✔️", fg="green")
            self.buttons["ss_shear_parameter"].config(text="Change Data")
        else:
            self.status_label3.config(text="❌", fg="red")
            self.buttons["ss_shear_parameter"].config(text="Add Data")

        if self.input_status["ps_shear_parameter"]:
            self.status_label4.config(text="✔️", fg="green")
            self.buttons["ps_shear_parameter"].config(text="Change Data")
        else:
            self.status_label4.config(text="❌", fg="red")
            self.buttons["ps_shear_parameter"].config(text="Add Data")
