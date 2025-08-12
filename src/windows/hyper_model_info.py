# hyper_model_info.py

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
from helpers.image_display import ImageDisplay
import helpers.geometry_manager as gm
from helpers.path_helpers import resolve_path

class ModelInfoWindow:
    def __init__(self, root, material, model_data, proceed_callback_back):
        self.root = root
        self.material = material
        self.model_data = model_data
        self.proceed_callback_back = proceed_callback_back
        self.root.title("Chosen Hyperelastic Model Info")

        # Set fixed size and center
        width, height = 500, 700
        geom = gm.get_centered_geometry(gm.get_last_geometry(), width, height)
        self.root.geometry(geom)
        self.root.configure(bg='white')

        # Display the main logo image
        image_path = resolve_path("assets/logos/Logo_HyperSmart.png")
        ImageDisplay(self.root, image_path, (300, 300), x=100, y=25)

        # Title
        tk.Label(self.root, text="Model:", font=("Arial", 11, "bold"), bg="white").place(x=20, y=100)
        tk.Label(self.root, text=model_data.get("model_name", "Unknown"), font=("Arial", 11), bg="white").place(x=80, y=100)

        # Model class
        tk.Label(self.root, text="Class:", font=("Arial", 11, "bold"), bg="white").place(x=20, y=125)
        tk.Label(self.root, text=model_data.get("model_class", "Unknown"), font=("Arial", 11), bg="white").place(x=80, y=125)

        # Description
        if "description" in model_data:
            tk.Label(self.root, text="Description:", font=("Arial", 11, "bold"), bg="white").place(x=20, y=150)
            desc = ScrolledText(self.root, wrap=tk.WORD, font=("Arial", 10), bg='white')
            desc.insert(tk.END, model_data["description"])
            desc.config(state='disabled')
            desc.place(x=20, y=175, width=460, height=80)

        # Start y-position for dynamic placing
        y_cursor = 260

        # Render LaTeX equation (strain_energy_function or strain_measure)
        if "strain_energy_function" in model_data or "strain_measure" in model_data:
            eq_type = "Strain Energy Function" if "strain_energy_function" in model_data else "Strain Measure"
            eq_text = model_data.get("strain_energy_function", model_data.get("strain_measure", ""))
            eq_text = eq_text.replace('\n', ' ')  # Handle multiline LaTeX

            tk.Label(self.root, text=f"{eq_type}:", font=("Arial", 11, "bold"), bg="white").place(x=20, y=y_cursor)
            y_cursor += 25

            if r"\begin{cases}" in eq_text and r"\end{cases}" in eq_text:
                eq_parts = split_cases_equation(eq_text)
            else:
                eq_parts = [eq_text]

            for part in eq_parts:
                img = ImageTk.PhotoImage(render_latex_to_image(part, fontsize=7))
                label = tk.Label(self.root, image=img, bg='white')
                label.image = img
                label.place(x=20, y=y_cursor)
                y_cursor += img.height() + 10

        # Material parameters
        if "material_constants" in model_data:
            tk.Label(self.root, text="Material Parameters:", font=("Arial", 11, "bold"), bg="white").place(x=20, y=y_cursor)
            y_cursor += 30
            for param in model_data["material_constants"]:
                name = param.get("display_format", param.get("name", ""))
                bounds = param.get("bounds", ["-", "-"])
                latex_param = f"{name} \\in [{bounds[0]}, {bounds[1]}]"
                img_param = ImageTk.PhotoImage(render_latex_to_image(latex_param, fontsize=6))
                label = tk.Label(self.root, image=img_param, bg='white')
                label.image = img_param
                label.place(x=25, y=y_cursor)
                y_cursor += img_param.height() + 10

        # References
        if "references" in model_data:
            tk.Label(self.root, text="References:", font=("Arial", 11, "bold"), bg="white").place(x=20, y=y_cursor)
            y_cursor += 20
            text_box = ScrolledText(self.root, wrap=tk.WORD, font=("Arial", 10), bg='white')
            text_box.place(x=20, y=y_cursor, width=460, height=100)
            refs = model_data["references"]
            if isinstance(refs, dict):
                for _, citation in refs.items():
                    text_box.insert(tk.END, f"- {citation.strip()}\n")
            elif isinstance(refs, list):
                for ref in refs:
                    for _, citation in ref.items():
                        text_box.insert(tk.END, f"- {citation.strip()}\n")
            text_box.config(state='disabled')

        # Back Button — fixed at bottom
        tk.Button(self.root, text="Back", command=lambda: self.proceed_callback_back(self.material)).place(x=450, y=665)


def render_latex_to_image(latex_str, dpi=150, fontsize=7):
    fig = plt.figure(figsize=(2, 1), dpi=dpi)
    fig.patch.set_facecolor('white')
    text = fig.text(0, 0, f"${latex_str}$", fontsize=fontsize)
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    bbox = text.get_window_extent(renderer=canvas.get_renderer())
    plt.close(fig)

    width_in = bbox.width / dpi
    height_in = bbox.height / dpi

    fig = plt.figure(figsize=(width_in, height_in), dpi=dpi)
    fig.patch.set_facecolor('white')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.text(0, 0, f"${latex_str}$", fontsize=fontsize, ha='left', va='bottom')

    canvas = FigureCanvasAgg(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    buf.seek(0)
    img = Image.open(buf)
    plt.close(fig)

    return img


def split_cases_equation(equation):
    """
    Splits a LaTeX \begin{cases} expression into individual lines for rendering,
    removing ampersands (&) and aligning properly.
    """
    before_cases = equation.split(r"\begin{cases}")[0].strip()
    inside = equation.split(r"\begin{cases}")[1].split(r"\end{cases}")[0].strip()
    cases = [case.strip() for case in inside.split(r"\\") if case.strip()]

    expressions = []
    for case in cases:
        if "&" in case:
            left, right = case.split("&", 1)
            clean = f"{before_cases} = {left.strip()} \\quad {right.strip()}"
        else:
            clean = f"{before_cases} = {case.strip()}"
        expressions.append(clean)

    return expressions






