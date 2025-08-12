# ──────────────────────────────────────────────────────────────────────
# BUSforModels.py  (full file – replace the old one)
# ──────────────────────────────────────────────────────────────────────
import os, yaml, math, itertools
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

from helpers.image_display import ImageDisplay
import helpers.geometry_manager as gm
from helpers.path_helpers import resolve_path


# ------------------------------------------------------------------ #
def reqmn(exp, pred):
    """Normalised RMSE used throughout the project."""
    err = np.sqrt(np.mean((exp - pred)**2))
    denom = np.mean(np.abs(exp))
    return err / denom if denom > 0 else np.inf


# ------------------------------------------------------------------ #
def run_bus_for_models(model_yaml_list, material, bus_cfg):
    """
    *****  LIGHTWEIGHT STAND-IN  *****
    Real BUS would run many conditional levels; here we do *one* level of
    plain Monte-Carlo sampling to obtain an evidence proxy log Z.

    Returns a list of dicts (one per model) with:
        { "model": <yaml dict>,
          "logZ" : float,
          "best_params": {name: value},
          "best_reqmn" : float }
    """
    sigma       = bus_cfg["sigma"]
    N           = bus_cfg["n"]             # samples (>=100 checked already)
    rng         = np.random.default_rng()

    # Map exp. data vectors once
    exp_map = {
        "uniaxial":    ("lamb",  material.sae_stretch,        material.sae_stress),
        "biaxial":     ("lamb",  material.ebl_stretch,        material.ebl_stress),
        "pure_shear":  ("lamb",  material.ps_shear_parameter, material.ps_stress),
        "simple_shear":("gamma", material.ss_shear_parameter, material.ss_stress),
    }
    stress_key = "expression_nominal" if material.stress_measure == 0 else "expression_cauchy"

    results = []

    for mdl in model_yaml_list:
        p_defs   = mdl["material_constants"]
        names    = [p["name"] for p in p_defs]
        bounds   = []
        for p in p_defs:
            lo, hi = p.get("bounds", [-math.inf, math.inf])
            # convert string "inf" etc.
            lo = -np.inf if str(lo).lower().startswith("-inf") else float(lo)
            hi =  np.inf if str(hi).lower().startswith("inf")   else float(hi)
            bounds.append((lo, hi))

        # quick helper to unwrap conditional formula blocks
        def pick_formula(block, param_dict):
            if isinstance(block, str):
                return block
            ctx = {k: float(v) for k, v in param_dict.items()}
            for item in block:
                cond = item.get("condition")
                if cond is None:
                    return item["formula"]
                try:
                    if eval(cond, {"__builtins__": {}}, ctx):
                        return item["formula"]
                except Exception:
                    pass
            return block[0]["formula"]

        math_ns = {
            "np": np, "math": math,
            "sin": np.sin, "cos": np.cos,
            "sinh": np.sinh, "cosh": np.cosh,
            "log": np.log,  "exp": np.exp,
            "sqrt": np.sqrt, "atan": np.arctan, "asinh": np.arcsinh,
        }

        logL_vals   = []
        best_req    = np.inf
        best_param  = None

        # --- draw N samples ------------------------------------------
        for _ in range(N):
            sample = {}
            for (lo, hi), name in zip(bounds, names):
                if np.isinf(lo) or np.isinf(hi):
                    # broad normal prior if un-bounded
                    sample[name] = rng.normal(0.0, 1.0)
                else:
                    sample[name] = rng.uniform(lo, hi)

            total_ll = 0.0
            total_req = 0.0
            all_ok   = True

            # evaluate every mode available in exp data
            for mode, (var, x_exp, y_exp) in exp_map.items():
                if x_exp.size < 2:
                    continue
                block    = mdl["deformation_modes"][mode][stress_key]
                formula  = pick_formula(block, sample)
                local_ns = {**math_ns, **sample, var: x_exp}
                try:
                    y_model = eval(formula, {"__builtins__": {}}, local_ns)
                except Exception:
                    all_ok = False
                    break

                r  = reqmn(y_exp, y_model)
                total_req += r * len(x_exp)

                # Gaussian log-likelihood
                total_ll += -0.5 * np.sum((y_exp - y_model)**2) / sigma**2

            if not all_ok:
                continue

            logL_vals.append(total_ll)

            if total_req < best_req:
                best_req   = total_req
                best_param = sample.copy()

        if not logL_vals:          # every sample blew up
            results.append({"model": mdl,
                            "logZ": -np.inf,
                            "best_params": {},
                            "best_reqmn": np.inf})
            continue

        # crude evidence proxy
        logZ = np.logaddexp.reduce(logL_vals) - math.log(len(logL_vals))

        results.append({"model": mdl,
                        "logZ": logZ,
                        "best_params": best_param,
                        "best_reqmn": best_req / sum(v.size
                                                     for _, (_, _, v) in exp_map.items())})

    return results


# ======================================================================#
class BUSforModels:
    MODEL_DIR = "hyperelastic_models"     # relative to src/

    # ------------------------------------------------------------------ #
    def __init__(self, root, material, back_callback_back):
        self.root = root
        self.material = material
        self.back_callback_back = back_callback_back

        # ----- window geometry / look ----------------------------------
        self.root.title("BUS – Model Selection")
        geom = gm.get_centered_geometry(gm.get_last_geometry(), 500, 700)
        self.root.geometry(geom)
        self.root.configure(bg="white")

        # ----- logo ----------------------------------------------------
        ImageDisplay(self.root,
                     resolve_path("assets/logos/Logo_HyperSmart.png"),
                     (300, 300),
                     x=100, y=25)

        style = ttk.Style()
        style.configure("White.TCheckbutton", background="white",
                        foreground="black")

        tk.Label(self.root, text="Select models to compare:",
                 font=("TkDefaultFont", 14, "bold"), bg="white")\
          .place(x=20, y=110)

        self.model_vars = {}          # stem -> IntVar
        self.model_yaml = {}          # stem -> YAML dict
        self._build_model_frame()
        self._build_settings_frame()

        tk.Button(self.root, text="Run BUS Comparison",
                  command=self._run_pressed).place(x=320, y=665)
        tk.Button(self.root, text="Back",
                  command=self.back_callback_back).place(x=450, y=665)

    # ------------------------------------------------------------------ #
    def _build_model_frame(self):
        outer = tk.Frame(self.root, bg="white")
        outer.place(x=20, y=140, width=460, height=240)

        canvas = tk.Canvas(outer, bg="white", highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=frame, anchor="nw")
        frame.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        model_dir = resolve_path(self.MODEL_DIR)
        if not os.path.isdir(model_dir):
            messagebox.showerror("Error", f"No '{model_dir}' directory found.")
            return

        for fname in sorted(os.listdir(model_dir)):
            if not fname.endswith((".yaml", ".yml")):
                continue
            stem = fname.rsplit(".", 1)[0]
            path = os.path.join(model_dir, fname)
            try:
                with open(path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                disp = data.get("model_name", stem)
                var = tk.IntVar(value=0)
                ttk.Checkbutton(frame, text=disp,
                                variable=var,
                                style="White.TCheckbutton")\
                    .pack(anchor="w", padx=10, pady=2)
                self.model_vars[stem] = var
                self.model_yaml[stem] = data
            except Exception as err:
                print(f"Failed to read {fname}: {err}")

    # ------------------------------------------------------------------ #
    def _build_settings_frame(self):
        outer = tk.Frame(self.root, bg="white", relief="groove", bd=1)
        outer.place(x=20, y=390, width=460, height=200)

        tk.Label(outer, text="BUS settings (shared):",
                 font=("TkDefaultFont", 12, "bold"),
                 bg="white").grid(row=0, column=0, columnspan=2,
                                  sticky="w", pady=(5, 10), padx=5)

        tk.Label(outer, text="σ  (MPa or kPa):", bg="white")\
          .grid(row=1, column=0, sticky="e", padx=5, pady=3)
        self.sigma_entry = tk.Entry(outer, width=10)
        self.sigma_entry.insert(0, "0.1")
        self.sigma_entry.grid(row=1, column=1, sticky="w", pady=3)

        tk.Label(outer, text="Samples / level  N:", bg="white")\
          .grid(row=2, column=0, sticky="e", padx=5, pady=3)
        self.n_entry = tk.Entry(outer, width=10)
        self.n_entry.insert(0, "1000")
        self.n_entry.grid(row=2, column=1, sticky="w", pady=3)

        tk.Label(outer, text="Target p₀:", bg="white")\
          .grid(row=3, column=0, sticky="e", padx=5, pady=3)
        self.p0_entry = tk.Entry(outer, width=10)
        self.p0_entry.insert(0, "0.1")
        self.p0_entry.grid(row=3, column=1, sticky="w", pady=3)

    # ------------------------------------------------------------------ #
    def _run_pressed(self):
        stems = [s for s, v in self.model_vars.items() if v.get() == 1]
        if not stems:
            messagebox.showwarning("Select model(s)",
                                   "Please tick at least one model to compare.")
            return

        try:
            sigma = float(self.sigma_entry.get())
            n     = int(self.n_entry.get())
            p0    = float(self.p0_entry.get())
            if sigma <= 0 or n < 100 or not (0 < p0 < 1):
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input",
                                 "Make sure σ, N, and p₀ are positive numbers "
                                 "(N ≥ 100, 0 < p₀ < 1).")
            return

        models_yaml = [self.model_yaml[s] for s in stems]
        bus_cfg     = {"sigma": sigma, "n": n, "p0": p0}

        # ---------- run (placeholder) BUS -----------------------------
        results = run_bus_for_models(models_yaml, self.material, bus_cfg)
        results.sort(key=lambda d: d["logZ"], reverse=True)

        # ---------- pop-up with ranking -------------------------------
        win = tk.Toplevel(self.root)
        win.title("BUS ranking")
        win.geometry("500x400")
        win.configure(bg="white")

        txt = ScrolledText(win, wrap=tk.WORD, font=("Arial", 10), bg="white")
        txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for i, r in enumerate(results, 1):
            mname = r["model"]["model_name"]
            txt.insert(tk.END, f"{i}. {mname}\n")
            txt.insert(tk.END, f"   log Z    : {r['logZ']:.3f}\n")
            txt.insert(tk.END, f"   best REQMN: {r['best_reqmn']:.4g}\n")
            for k, v in r["best_params"].items():
                txt.insert(tk.END, f"      {k} = {v:.4g}\n")
            txt.insert(tk.END, "\n")

        txt.config(state="disabled")


