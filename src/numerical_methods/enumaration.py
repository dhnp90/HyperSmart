# numerical_methods/enumeration.py
import math, itertools
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText     # (unused but left intact)
import matplotlib.pyplot as plt                   # (unused but left intact)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # idem

import helpers.geometry_manager as gm
from helpers.path_helpers import resolve_path
from helpers.image_display import ImageDisplay


class MethodWindow:
    def __init__(self, root, material, model_data, proceed_callback_back):
        self.root = root
        self.material = material          # ExperimentalData instance
        self.model = model_data           # YAML dict of the chosen model
        self.proceed_callback_back = proceed_callback_back

        # ---------- window geometry ----------
        self.root.title("Enumeration Method")
        geom = gm.get_centered_geometry(gm.get_last_geometry(), 500, 700)
        self.root.geometry(geom)
        self.root.configure(bg="white")

        # ---------- logo ----------
        ImageDisplay(self.root,
                     resolve_path("assets/logos/Logo_HyperSmart.png"),
                     (300, 300), x=100, y=25)

        # Storage
        self.bound_entries = {}   # param_name -> (low, high, step) Entry widgets
        self.mode_vars = {}       # mode -> IntVar for check-box (0/1)

        # Build UI
        self.input_window_ui()

    # ------------------------------------------------------------------ #
    def input_window_ui(self):
        # ------------------ parameter grid ------------------------------
        tk.Label(self.root, text="Grid-search limits",
                 font=("TkDefaultFont", 12, "bold"),
                 bg="white").place(x=20, y=200)

        frame = tk.Frame(self.root, bg="white", relief="groove", bd=1)
        frame.place(x=100, y=230, width=300, height=220)

        headers = ["Parameter", "Lower", "Upper", "Δ step"]
        for j, h in enumerate(headers):
            tk.Label(frame, text=h, bg="white",
                     font=("Arial", 10, "bold"))\
              .grid(row=0, column=j, padx=5, pady=5)

        # helper: YAML 'inf'/'-inf' → float
        def _to_float(val):
            if isinstance(val, str):
                low = val.lower()
                if low.startswith("inf"):
                    return float("inf")
                if low.startswith("-inf"):
                    return float("-inf")
                return float(low)
            return float(val)

        for i, const in enumerate(self.model["material_constants"], start=1):
            name = const["name"]
            lb_raw, ub_raw = const.get("bounds", [-math.inf, math.inf])
            lb_def, ub_def = _to_float(lb_raw), _to_float(ub_raw)

            tk.Label(frame, text=name, bg="white")\
              .grid(row=i, column=0, padx=5)

            e_low  = tk.Entry(frame, width=10)
            e_high = tk.Entry(frame, width=10)
            e_step = tk.Entry(frame, width=10)

            if not math.isinf(lb_def):
                e_low.insert(0, str(lb_def))
            if not math.isinf(ub_def):
                e_high.insert(0, str(ub_def))

            e_low .grid(row=i, column=1)
            e_high.grid(row=i, column=2)
            e_step.grid(row=i, column=3)

            self.bound_entries[name] = (e_low, e_high, e_step)

        # ----------------- deformation-mode selector --------------------
        tk.Label(self.root, text="Choose deformation modes to calibrate:",
                 font=("TkDefaultFont", 11, "bold"),
                 bg="white").place(x=20, y=470)

        modes_frame = tk.Frame(self.root, bg="white")
        modes_frame.place(x=20, y=500)

        data_available = {
            "uniaxial"    : self.material.sae_stretch.size  > 1,
            "biaxial"     : self.material.ebl_stretch.size  > 1,
            "pure_shear"  : self.material.ps_shear_parameter.size > 1,
            "simple_shear": self.material.ss_shear_parameter.size > 1,
        }
        nice = {"uniaxial": "Uniaxial",
                "biaxial": "Biaxial",
                "pure_shear": "Pure shear",
                "simple_shear": "Simple shear"}

        col = 0
        for mode, has in data_available.items():
            var = tk.IntVar(value=1 if has else 0)
            chk = tk.Checkbutton(modes_frame, text=nice[mode],
                                 variable=var, bg="white")
            chk.grid(row=0, column=col, padx=10)
            if not has:
                chk.config(state="disabled")
            self.mode_vars[mode] = var
            col += 1

        # ----------------- navigation buttons (unchanged) --------------
        tk.Button(self.root, text="Run Calibration",
                  command=self._run_placeholder).place(x=350, y=665)
        tk.Button(self.root, text="Back",
                  command=self.proceed_callback_back).place(x=450, y=665)

    # ========== helper to clean exotic characters & new-lines ========= #
    @staticmethod
    def _sanitize_formula(txt: str) -> str:
        """
        Replace exotic characters that confuse Python's parser and squash
        line-breaks into spaces.
        """
        return txt.replace("\u2212", "-").replace("\n", " ")

    # ------------------------------------------------------------------ #
    @staticmethod
    def _select_expression(expr_block, param_dict=None):
        """Return a single formula string (handles conditionals)."""
        if isinstance(expr_block, str):
            chosen = expr_block
        else:
            if param_dict is None:
                param_dict = {}
            if not isinstance(expr_block, list):
                raise ValueError("Unknown expression block type.")

            safe_ctx = {k: float(v) for k, v in param_dict.items()}
            for item in expr_block:
                cond = item.get("condition")
                if cond is None:
                    chosen = item["formula"]; break
                try:
                    if eval(cond, {"__builtins__": {}}, safe_ctx):
                        chosen = item["formula"]; break
                except Exception:
                    pass
            else:
                chosen = expr_block[0]["formula"]

        return MethodWindow._sanitize_formula(chosen)

    # ------------------------------------------------------------------ #
    def _run_placeholder(self):
        # ---- collect modes & expressions ------------------------------
        if not any(v.get() for v in self.mode_vars.values()):
            messagebox.showwarning("Select mode",
                                   "Please choose at least one deformation mode.")
            return

        sm_flag  = getattr(self.material, "stress_measure", 0)
        expr_key = "expression_nominal" if sm_flag == 0 else "expression_cauchy"

        self.selected_modes   = []
        self.mode_expressions = {}

        for mode, var in self.mode_vars.items():
            if var.get() != 1:
                continue
            block = self.model["deformation_modes"][mode].get(expr_key)
            if block is None:
                messagebox.showerror("Error",
                                     f"No '{expr_key}' for mode '{mode}'.")
                return
            self.mode_expressions[mode] = block
            self.selected_modes.append(mode)

        if not self.selected_modes:
            messagebox.showwarning("Select mode",
                                   "No deformation modes selected.")
            return

        # ---------- Step-3: enumeration --------------------------------
        try:
            best_params, best_reqmn = self._run_enumeration()
        except Exception as err:
            messagebox.showerror("Error during enumeration", str(err))
            return

        txt = "\n".join(f"{k} = {v:g}" for k, v in best_params.items())
        messagebox.showinfo("Enumeration finished",
                            f"Best REQMN = {best_reqmn:.4g}\n\n{txt}")

    # ------------------------------------------------------------------ #
    def _compute_global_defs(self, param_dict):
        """
        Evaluate 'global_definitions' (if present in YAML) with the current
        parameter set and return a dict of the resulting symbols.
        """
        defs = self.model.get("global_definitions", {})
        if not defs:
            return {}

        ns = {**param_dict, "np": np, "math": math,
              "log": math.log, "sqrt": math.sqrt}
        out = {}
        for sym, formula in defs.items():
            try:
                out[sym] = eval(self._sanitize_formula(formula),
                                {"__builtins__": {}}, ns)
            except Exception as err:
                raise ValueError(f"Failed global definition '{sym}': {err}")
        return out

    # ------------------------------------------------------------------ #
    def _run_enumeration(self):
        # -------- build parameter grid ----------------------------------
        param_names = [c["name"] for c in self.model["material_constants"]]
        grid_values = []

        for name in param_names:
            e_low, e_high, e_step = self.bound_entries[name]
            try:
                low  = float(e_low.get())
                high = float(e_high.get())
                step = float(e_step.get())
            except ValueError:
                raise ValueError(f"Bounds/step for {name} are invalid.")

            if step <= 0 or high < low:
                raise ValueError(f"Check bounds/step for {name}.")

            n_pts = int(round((high - low) / step)) + 1
            grid_values.append([low + i*step for i in range(n_pts)])

        total_comb = np.prod([len(v) for v in grid_values])
        if total_comb > 2e5:   # arbitrary safety limit
            raise ValueError(f"Grid has {int(total_comb):,} combinations – too large.")

        # -------- mapping exp data & variable names ---------------------
        exp_map = {
            "uniaxial":    ("lamb",  self.material.sae_stretch,        self.material.sae_stress),
            "biaxial":     ("lamb",  self.material.ebl_stretch,        self.material.ebl_stress),
            "pure_shear":  ("lamb",  self.material.ps_shear_parameter, self.material.ps_stress),
            "simple_shear":("gamma", self.material.ss_shear_parameter, self.material.ss_stress),
        }

        # -------- iterate ------------------------------------------------
        best_reqmn   = float("inf")
        best_params  = None
        math_ns_base = {
            "np": np, "math": math,
            "sin": np.sin, "cos": np.cos, "sinh": np.sinh, "cosh": np.cosh,
            "log": np.log, "exp": np.exp, "sqrt": np.sqrt,
            "atan": np.arctan, "asinh": np.arcsinh,
        }

        for values in itertools.product(*grid_values):
            param_dict = dict(zip(param_names, values))

            # ----- add global_definitions (L1, L2, …) ------------------
            try:
                global_defs = self._compute_global_defs(param_dict)
            except ValueError as err:
                print(err); continue

            all_err2 = []
            all_abs  = []

            for mode in self.selected_modes:
                varname, x_exp, y_exp = exp_map[mode]
                if x_exp.size == 0:
                    continue

                formula = self._select_expression(
                    self.mode_expressions[mode], param_dict)

                local_ns = {**math_ns_base, **param_dict,
                            **global_defs,
                            varname: x_exp}

                try:
                    y_pred = eval(formula, {"__builtins__": {}}, local_ns)
                except Exception as err:
                    print(f"Combo failed: {param_dict} | mode: {mode} | reason: {err}")
                    all_err2 = None
                    break

                residual = y_exp - y_pred
                all_err2.append(np.square(residual))
                all_abs .append(np.abs(y_exp))

            if all_err2 is None:
                continue

            err2   = np.concatenate(all_err2)
            absSig = np.concatenate(all_abs)

            reqmn = math.sqrt(np.mean(err2)) / np.mean(absSig)

            if reqmn < best_reqmn:
                best_reqmn  = reqmn
                best_params = param_dict.copy()

        if best_params is None:
            print("DEBUG: Enumeration found no valid combination.")
            raise RuntimeError("No valid combination found.")

        return best_params, best_reqmn





