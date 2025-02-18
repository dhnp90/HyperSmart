import tkinter as tk
from image_display import ImageDisplay
from data_center import ExperimentalData
from windows.input_window import ExperimentalDataInputWindow

class ExperimentalDataWindow:
    def __init__(self, root, material):
        self.root = root
        self.material = material
        self.root.title("Experimental Data Input")
        self.root.geometry("500x700")

        # Dictionary to track input status for each data type
        self.input_status = {
            "sae_stretch": False,
            "ebl_stretch": False,
            "ss_shear_parameter": False,
            "ps_shear_parameter": False,
        }

        # Display the main logo image
        ImageDisplay(self.root, 'Logo_HyperSmart.png', (300, 300), x=100, y=25)

        # Display labels
        labels = ["Uniaxial Tension/Compression", "Equi-Biaxial Loading", "Simple Shear","Pure Shear"]
        for i, text in enumerate(labels):
            label = tk.Label(self.root, text=text, font=("Helvetica", 10), anchor='w')
            label.place(x=20, y=300 + i * 50, width=250, height=25)

        # Add Data buttons and status labels
        self.add_data_button1 = tk.Button(self.root, text="Add Data", 
                                         command=lambda: self.open_data_input_window(("sae_stretch", "sae_stress")))
        self.add_data_button1.place(x=280, y=300, width=100, height=25)
        self.status_label1 = tk.Label(self.root, text="❌", fg="red", font=("Helvetica", 12))
        self.status_label1.place(x=390, y=300, width=20, height=25)

        self.add_data_button2 = tk.Button(self.root, text="Add Data", 
                                         command=lambda: self.open_data_input_window(("ebl_stretch", "ebl_stress")))
        self.add_data_button2.place(x=280, y=350, width=100, height=25)
        self.status_label2 = tk.Label(self.root, text="❌", fg="red", font=("Helvetica", 12))
        self.status_label2.place(x=390, y=350, width=20, height=25)

        self.add_data_button3 = tk.Button(self.root, text="Add Data", 
                                         command=lambda: self.open_data_input_window(("ss_shear_parameter", "ss_stress")))
        self.add_data_button3.place(x=280, y=400, width=100, height=25)
        self.status_label3 = tk.Label(self.root, text="❌", fg="red", font=("Helvetica", 12))
        self.status_label3.place(x=390, y=400, width=20, height=25)

        self.add_data_button4 = tk.Button(self.root, text="Add Data", 
                                         command=lambda: self.open_data_input_window(("ps_shear_parameter", "ps_stress")))
        self.add_data_button4.place(x=280, y=450, width=100, height=25)
        self.status_label4 = tk.Label(self.root, text="❌", fg="red", font=("Helvetica", 12))
        self.status_label4.place(x=390, y=450, width=20, height=25)

        # Update status labels initially
        self.update_status_labels()

    def open_data_input_window(self, vector_names):
        """Opens the ExperimentalDataInputWindow and passes the material object along with vector names."""
        new_window = tk.Toplevel(self.root)  # Create a new window
        ExperimentalDataInputWindow(new_window, self.material, vector_names)

        # Assume data is input after the window is closed
        # Update the input status for the corresponding data type
        data_type = vector_names[0]  # e.g., "sae_stretch"
        self.input_status[data_type] = True

        # Update the status labels
        self.update_status_labels()

    def update_status_labels(self):
        """Updates the status labels based on the input status."""
        if self.input_status["sae_stretch"]:
            self.status_label1.config(text="✔️", fg="green")
        else:
            self.status_label1.config(text="❌", fg="red")

        if self.input_status["ebl_stretch"]:
            self.status_label2.config(text="✔️", fg="green")
        else:
            self.status_label2.config(text="❌", fg="red")

        if self.input_status["ss_shear_parameter"]:
            self.status_label3.config(text="✔️", fg="green")
        else:
            self.status_label3.config(text="❌", fg="red")

        if self.input_status["ps_shear_parameter"]:
            self.status_label4.config(text="✔️", fg="green")
        else:
            self.status_label4.config(text="❌", fg="red")

#  # Test script
# if __name__ == "__main__":
#     root = tk.Tk()
#     material = None  # Placeholder, replace with an actual ExperimentalData object if needed
#     app = ExperimentalDataInputWindow(root, material)
#     root.mainloop()