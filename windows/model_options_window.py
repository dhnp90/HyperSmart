import tkinter as tk
from tkinter import ttk
from image_display import ImageDisplay

class OptionsOfModels:
    def __init__(self, root, material):
        self.root = root
        self.material = material
        self.root.title("Options of Hyperelastic Model")
        self.center_window(500, 700)
        self.root.configure(bg='white')

        # Configure style for radiobuttons to have a white background
        self.style = ttk.Style()
        self.style.configure("Custom.TRadiobutton", background="white", foreground="black")

        # Display the main logo image
        ImageDisplay(self.root, 'Logo_HyperSmart.png', (300, 300), x=100, y=25)

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

        # Variable to store the selected model
        self.selected_model = tk.StringVar(value="")  

        # Add section titles and options
        self.add_model_options(scrollable_frame)

        # Next Button
        next_button = tk.Button(self.root, text="Next", command=self.next_step)
        next_button.place(x=450, y=665)

    def add_model_options(self, parent):
        """Creates a structured list of hyperelastic models with selectable options."""
        
        sections = {
            "Hookean-type": [
                "Generalized Hyperbolic Sine family of strain measures",
                "Seth-Hill family of strain measures",
                "Curnier-Rakotomanana (Darijani-Naghdabadi) family of strain measures",
                "Curnier-Zysset family of metric strain measures",
                "Beex family of strain measures"
            ],
            "Series function based on invariants": [
                "Neo-Hookean",
                "Mooney-Rivlin",
                "Yeoh",
                "Hartmann-Neff"
            ],
            "Power law, exponential or logarithmic functions based on invariants": [
                "Yamashita-Kawabata",
                "Hartmann-Neff",
                "Hoss-Marczak",
                "Khajehsaeid",
                "Arruda-Boyce",
                "Yeoh-Fleming",
                "Gent"
            ],
            "Models based on stretch ratio": [
                "Ogden",
                "Valanis-Landel"
            ]
        }

        for category, models in sections.items():
            tk.Label(parent, text=category, font=("Arial", 10, "bold"), bg='white', anchor="w").pack(fill="x", pady=(10, 5))
            for model in models:
                ttk.Radiobutton(parent, text=model, variable=self.selected_model, value=model, style="Custom.TRadiobutton").pack(anchor="w", padx=20, pady=2)

    def next_step(self):
        """Function to handle when the Next button is clicked."""
        selected = self.selected_model.get()
        if selected:
            print(f"Selected model: {selected}")  # You can replace this with the actual next step
        else:
            print("No model selected. Please choose one.")

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - width / 2)
        center_y = int(screen_height / 2 - height / 2)
        self.root.geometry(f'{width}x{height}+{center_x}+{center_y}')
