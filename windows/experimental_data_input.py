import tkinter as tk
from image_display import ImageDisplay

class ExperimentalDataInputWindow:
    def __init__(self, root, material):
        self.root = root
        self.root.title("Experimental Data Input")
        self.root.geometry("500x700")

        # Display the main logo image
        ImageDisplay(self.root, 'Logo_HyperSmart.png', (300, 300), x=100, y=25)

        # Display labels
        labels = ["Uniaxial Tension/Compression", "Equi-Biaxial Loading", "Simple Shear","Pure Shear"]
        for i, text in enumerate(labels):
            label = tk.Label(self.root, text=text, font=("Helvetica", 10), anchor='w')
            label.place(x=20, y=300 + i * 50, width=250, height=25)

        # Display the "Add data" buttons
        add_data_button1 = tk.Button(self.root, text="Add Data", command=self.add_uniaxial)
        add_data_button1.place(x=280, y=300 , width=100, height=25)

        add_data_button2 = tk.Button(self.root, text="Add Data")
        add_data_button2.place(x=280, y=350 , width=100, height=25)

        add_data_button3 = tk.Button(self.root, text="Add Data")
        add_data_button3.place(x=280, y=400 , width=100, height=25)

        add_data_button4 = tk.Button(self.root, text="Add Data")
        add_data_button4.place(x=280, y=450 , width=100, height=25)

    # def add_uniaxial(self.material):


 # Test script
if __name__ == "__main__":
    root = tk.Tk()
    material = None  # Placeholder, replace with an actual ExperimentalData object if needed
    app = ExperimentalDataInputWindow(root, material)
    root.mainloop()