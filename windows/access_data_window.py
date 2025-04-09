# access_data_window.py

import tkinter as tk
from tkinter import scrolledtext
from image_display import ImageDisplay


class AccessExpDataWindow:
    def __init__(self, root, selected_data):
        self.root = root
        self.selected_data = selected_data
        self.root.title("Material Experimental Data to be Accessed")
        self.center_window(1200, 700)

        # Logo ajustado
        ImageDisplay(self.root, 'Logo_HyperSmart.png', (300, 300), x=450, y=25)

        # Mapeamento de modos e posições
        modes = ["axial", "biaxial", "simple_shear", "pure_shear"]
        labels = ["Axial Data", "Biaxial Data", "Simple Shear", "Pure Shear"]
        base_x = 90
        spacing = 260
        y_label = 105
        y_textbox = 130
        y_button = 600

        # Criar widgets para cada modo
        for i, mode in enumerate(modes):
            x_pos = base_x + i * spacing
            self.display_data_mode(mode, labels[i], x_pos, y_label, y_textbox, y_button)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - width / 2)
        center_y = int(screen_height / 2 - ((height + 80) / 2))
        self.root.geometry(f'{width}x{height}+{center_x}+{center_y}')

    def display_data_mode(self, mode, label_text, label_x, label_y, text_box_y, button_y):
        data = self.selected_data.get("data", {}).get(mode, None)

        # Label
        label = tk.Label(self.root, text=label_text, font=("Arial", 12, "bold"), bg="white")
        label.place(x=label_x + 40, y=label_y)

        if data:
            # Tenta pegar o eixo-x com diferentes possíveis nomes
            x_vals = (
                data.get("stretch") or
                data.get("strain") or
                data.get("gamma") or
                data.get("shear_parameter") or
                []
            )
            y_vals = data.get("stress", [])

            # Caixa de texto
            text_box = scrolledtext.ScrolledText(self.root, width=20, height=28, font=("Courier", 10))
            for x, y in zip(x_vals, y_vals):
                try:
                    text_box.insert(tk.END, f"{float(x):.5f}\t{float(y):.5f}\n")
                except ValueError:
                    continue
            text_box.configure(state='normal')
            text_box.place(x=label_x, y=text_box_y)

            # Botão "Copy"
            copy_button = tk.Button(self.root, text="Copy", command=lambda box=text_box: self.copy_text(box))
            copy_button.place(x=label_x + 65, y=button_y)

            # Menu de contexto
            self.add_context_menu(text_box)
        else:
            no_data_label = tk.Label(self.root, text="No data available for this mode.", fg="red", font=("Arial", 10, "italic"))
            no_data_label.place(x=label_x, y=text_box_y + 10)

    def copy_text(self, text_widget):
        self.root.clipboard_clear()
        self.root.clipboard_append(text_widget.get("1.0", tk.END))
        self.root.update()  # Garante que o conteúdo fique disponível na área de transferência

    def add_context_menu(self, widget):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Copy", command=lambda: widget.event_generate("<<Copy>>"))

        def show_context_menu(event):
            widget.focus()
            menu.post(event.x_root, event.y_root)

        widget.bind("<Button-3>", show_context_menu)  # Botão direito do mouse
