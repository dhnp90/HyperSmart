# numerical_methods_options.py
import os
import yaml
import tkinter as tk
from tkinter import ttk
from helpers.image_display import ImageDisplay
import helpers.geometry_manager as gm
from helpers.path_helpers import resolve_path
from tkinter.scrolledtext import ScrolledText

class NumericalMethodOptions:
    """
    UI window to choose a numerical-calibration method (Enumeration, BUS, …)
    """

    METHOD_DIR = "numerical_methods"          # relative to src/

    def __init__(self, root, material, model_data, proceed_callback_back, proceed_callback_next):  
        self.root = root
        self.material = material
        self.model_data = model_data
        self.proceed_callback_back = proceed_callback_back
        self.proceed_callback_next = proceed_callback_next

        # ---------- window geometry ----------
        self.root.title("Options of Numerical Method")
        geom = gm.get_centered_geometry(gm.get_last_geometry(), 500, 700)
        self.root.geometry(geom)
        self.root.configure(bg="white")

        # ---------- logo ----------
        logo_path = resolve_path("assets/logos/Logo_HyperSmart.png")
        ImageDisplay(self.root, logo_path, (300, 300), x=100, y=25)

        # ---------- custom ttk style ----------
        style = ttk.Style()
        style.configure("Custom.TRadiobutton", background="white",
                        foreground="black")

        # ---------- heading ----------
        tk.Label(self.root, text="Choose the numerical method to use:",
                 font=("TkDefaultFont", 14), bg="white", fg="black")\
          .place(x=20, y=110)

        # ---------- scrollable radio-button frame ----------
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(pady=150, padx=20, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame, bg="white", highlightthickness=0)
        vscroll = ttk.Scrollbar(main_frame, orient="vertical",
                                command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="white")
        scrollable.bind("<Configure>",
                        lambda e: canvas.configure(
                            scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=vscroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        # ---------- radio-button variable & method-data dict ----------
        self.selected_stem = tk.StringVar(value="")
        self.method_data = {}      # stem → yaml dict

        self._populate_methods(scrollable)

        # ---------- bottom buttons ----------
        tk.Button(self.root, text="Next",
                  command=self._next_step).place(x=450, y=665)

        tk.Button(self.root, text="Back",
                  command=lambda: self.proceed_callback_back(self.material))\
          .place(x=330, y=665)

        tk.Button(self.root, text="Method Info",
                  command=self._info_request).place(x=370, y=665)

    # ------------------------------------------------------------------ #
    def _populate_methods(self, parent):
        """Load every *.yaml in METHOD_DIR and add radio buttons."""
        dir_path = resolve_path(self.METHOD_DIR)
        if not os.path.isdir(dir_path):
            print(f"No directory '{dir_path}' found for numerical methods.")
            return

        for fname in sorted(os.listdir(dir_path)):
            if fname.endswith((".yaml", ".yml")):
                stem = fname.rsplit(".", 1)[0]      # enumeration.yaml → enumeration
                path = os.path.join(dir_path, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                    display_name = data.get("method_name", stem)
                    ttk.Radiobutton(parent,
                                    text=display_name,
                                    variable=self.selected_stem,
                                    value=stem,
                                    style="Custom.TRadiobutton")\
                       .pack(anchor="w", padx=20, pady=2)
                    self.method_data[stem] = data
                except Exception as err:
                    print(f"Failed to read {fname}: {err}")

    # ------------------------------------------------------------------ #
    def _next_step(self):
        stem = self.selected_stem.get()
        if not stem:
            tk.messagebox.showwarning("Select a method",
                                      "Please select a numerical method.")
            return
        self.proceed_callback_next(self.material,
                                   self.model_data,
                                   stem)

    # ------------------------------------------------------------------ #
    def _info_request(self):
        stem = self.selected_stem.get()
        if not stem:
            tk.messagebox.showwarning("Select a method",
                                      "Please select a numerical method.")
            return

        data = self.method_data.get(stem)
        if not data:
            tk.messagebox.showerror("Error", f"No data for '{stem}'.")
            return

        # --- popup window with description ---
        win = tk.Toplevel(self.root)
        win.title(data.get("method_name", stem))
        win.geometry("500x300")
        win.configure(bg="white")

        txt = ScrolledText(win, wrap=tk.WORD, font=("Arial", 10), bg="white")
        txt.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        txt.insert(tk.END, data.get("description", "No description found."))
        txt.config(state="disabled")
