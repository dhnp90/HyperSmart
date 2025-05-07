import tkinter as tk
from auxiliary_py_modules.image_display import ImageDisplay
from auxiliary_py_modules.hover_over_btn import Tooltip
import auxiliary_py_modules.geometry_manager as gm
from auxiliary_py_modules.path_helpers import resolve_path

class ChosenExpDataInfo:
    def __init__(self, root, proceed_callback_back, proceed_callback_access, selected_data=None):
        self.root = root
        self.selected_data = selected_data
        self.proceed_callback_back = proceed_callback_back
        self.proceed_callback_access = proceed_callback_access

        self.root.title("Material Experimental Data Information")
        
        # Restore previous geometry 
        geom = gm.get_centered_geometry(gm.get_last_geometry(), 500, 700)
        self.root.geometry(geom)
        self.root.configure(bg='white')

        # Use TkDefaultFont for consistency
        custom_font = "TkDefaultFont"
        bold_font = (custom_font, 10, 'bold')  # Make the font bold for headings
        
        # Frame for logo (Reserves space for the image)
        logo_frame = tk.Frame(self.root, bg="white", height=180)  # Adjust height as needed
        logo_frame.pack(fill="x")

        # Display the main logo
        image_path = resolve_path("assets/logos/Logo_HyperSmart.png")             
        ImageDisplay(self.root, image_path, (300, 300), x=100, y=25)

        # Frame to hold text and scrollbar (without expand=True)
        frame = tk.Frame(self.root, bg="white")
        frame.pack(pady=10, padx=10, fill="both", expand=False)

        # Create Text widget with fixed size
        text_widget = tk.Text(frame, wrap="word", height=28, width=75, bg="white", font=custom_font)
        text_widget.pack(side="left", fill="both", padx=5)

        # Add Scrollbar
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")

        # Link Scrollbar to Text widget
        text_widget.config(yscrollcommand=scrollbar.set)

        # Create a tag for bold headings
        text_widget.tag_configure("bold", font=bold_font)

        # Format and insert the material data into text
        if self.selected_data:
            material = self.selected_data.get("material", "Unknown")
            title = self.selected_data.get("publication_title", "Unknown")
            authors = self.selected_data.get("author", "Unknown")
            year = self.selected_data.get("year", "Unknown")
            description = self.selected_data.get("description", "Unknown")
            stress_measure = self.selected_data.get("stress_measure", "Unknown")

            # Deformation Modes Formatting
            deformation_modes = [
                mode.replace("_", " ").capitalize()
                for mode, tested in self.selected_data.get("deformation_modes", {}).items()
                if tested
            ]
            deformation_modes_text = ", ".join(deformation_modes) if deformation_modes else "None"

            # Unit of Measure Formatting
            unit_of_measure = [
                unit for mode, unit in self.selected_data.get("unit_of_measure", {}).items() if unit
            ]
            unit_text = ", ".join(set(unit_of_measure)) if unit_of_measure else "Not specified"

            # Data Acquisition Method
            acquisition_methods = {
                1: "The experimental data was published together with the Scientific Publication",
                2: "The data was extracted from graphs using an image extraction tool"
            }
            data_source = acquisition_methods.get(self.selected_data.get("data_source", 0), "Unknown method")

            # Citation & DOI
            citation = self.selected_data.get("citation", "No citation available")
            doi = self.selected_data.get("doi", "No DOI available")
            note = self.selected_data.get("note", "No additional notes")

            # Formatting text with bold headings
            info_text = f"""Material Name:\n{material}

Title of the Scientific Source:\n{title}

Authors:\n{authors}

Year of Publication:\n{year}

Description of the Experimental Data:\n{description}

Stress Measure:\n{stress_measure} Stress

Pure Deformation Modes Tested:\n{deformation_modes_text}

Unit of Measure of the Stress:\n{unit_text}

Method of Data Acquisition:\n{data_source}

How to Cite:\n{citation}

DOI:\n{doi}

Note:\n{note}
"""

            # Insert text and apply bold tags to headings
            text_widget.insert("1.0", info_text)

            # Apply bold formatting to headings
            for heading in ["Material Name:", "Title of the Scientific Source:", "Authors:", "Year of Publication:",
                            "Description of the Experimental Data:", "Stress Measure:", "Pure Deformation Modes Tested:",
                            "Unit of Measure of the Stress:", "Method of Data Acquisition:", "How to Cite:", "DOI:", "Note:"]:
                start_index = text_widget.search(heading, "1.0", stopindex=tk.END)
                if start_index:
                    end_index = f"{start_index}+{len(heading)}c"
                    text_widget.tag_add("bold", start_index, end_index)
        
        else:
            text_widget.insert("1.0", "No material data available.")

        # Disable editing
        text_widget.config(state="disabled")

        # Label
        label1 = tk.Label(self.root, text="Information About the Chosen Experimental Data:", font=bold_font, fg="black", bg="white")
        label1.place(x=12, y=168)

        # Add "access data" button
        access_data_button = tk.Button(self.root, text="Access Data", command=lambda: self.proceed_callback_access(self.selected_data))
        access_data_button.place(x=420, y=665)
        Tooltip(access_data_button, text="Click here to be able to see and copy the selected experimental data.")

        # Add "Back" button
        back_button = tk.Button(self.root, text="Back", command=self.proceed_callback_back)
        back_button.place(x=380, y=665)
