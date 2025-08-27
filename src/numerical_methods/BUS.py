# numerical_methods/BUS.py
import math, random, itertools
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import helpers.geometry_manager as gm
from helpers.path_helpers import resolve_path
from helpers.image_display import ImageDisplay


# ──────────────────────────────────────────────────────────────────────────
#  Small utility used by Enumeration – we reuse it here
# ──────────────────────────────────────────────────────────────────────────
def select_expression(expr_block, param_dict=None):
    """
    Return a single formula string from a YAML entry
    that might be a list of {'condition','formula'} dicts.
    """
    if isinstance(expr_block, str):
        return expr_block
    if param_dict is None:
        param_dict = {}
    safe = {k: float(v) for k, v in param_dict.items()}
    for item in expr_block:
        cond = item.get("condition")
        if cond is None:
            return item["formula"]
        try:
            if eval(cond, {"__builtins__": {}}, safe):
                return item["formula"]
        except Exception:
            pass
    return expr_block[0]["formula"]


# ──────────────────────────────────────────────────────────────────────────
#  BUS Solver (very small 2-level Subset Simulation)
# ──────────────────────────────────────────────────────────────────────────
def run_bus_solver(material, model_yaml, priors, sigma, modes,
                   nsamples=2000, p0=0.1, max_levels=2):
    """
    Very small BUS implementation.

    Parameters
    ----------
    material   : ExperimentalData
    model_yaml : dict  (chosen hyperelastic model)
    priors     : {name: ("uniform", a, b) or ("normal", μ, σ)}
    sigma      : float (Gaussian noise)
    modes      : list[str]  deformation modes to use
    nsamples   : samples per level
    p0         : target conditional probability per level
    max_levels : number of BUS levels (>=2)

    Returns
    -------
    map_params    : dict  best (MAP) parameters
    post_samples  : ndarray [N, n_par] posterior draws
    """

    # ----------- helpers to compute stress and likelihood --------------
    param_names = [c["name"] for c in model_yaml["material_constants"]]

    # map from mode → (independent-variable name, exp-x, exp-y)
    exp_map = {
        "uniaxial":    ("lamb",  material.sae_stretch,        material.sae_stress),
        "biaxial":     ("lamb",  material.ebl_stretch,        material.ebl_stress),
        "pure_shear":  ("lamb",  material.ps_shear_parameter, material.ps_stress),
        "simple_shear":("gamma", material.ss_shear_parameter, material.ss_stress),
    }

    sm_flag  = getattr(material, "stress_measure", 0)
    expr_key = "expression_nominal" if sm_flag == 0 else "expression_cauchy"
    raw_expr = {m: model_yaml["deformation_modes"][m][expr_key] for m in modes}

    math_ns = {
        "np": np, "sin": np.sin, "cos": np.cos,
        "sinh": np.sinh, "cosh": np.cosh,
        "log": np.log, "exp": np.exp,
        "sqrt": np.sqrt, "atan": np.arctan, "asinh": np.arcsinh,
    }

    def predict_stress(param_vec, mode):
        """Return model stress (array) for given mode."""
        p_dict = dict(zip(param_names, param_vec))
        var, x_exp, _ = exp_map[mode]
        local = {**math_ns, **p_dict, var: x_exp}
        formula = select_expression(raw_expr[mode], p_dict)
        return eval(formula, {"__builtins__": {}}, local)  # may raise!

    def log_prior(theta):
        lp = 0.0
        for val, name in zip(theta, param_names):
            kind, a, b = priors[name]
            if kind == "uniform":
                if not (a <= val <= b):
                    return -np.inf
                lp += -math.log(b - a)
            else:  # normal
                lp += -0.5 * ((val - a) / b) ** 2 - math.log(b * math.sqrt(2 * math.pi))
        return lp

    all_y_exp = np.concatenate([exp_map[m][2] for m in modes])

    def log_likelihood(theta):
        try:
            preds = np.concatenate([predict_stress(theta, m) for m in modes])
        except Exception:
            return -np.inf
        resid = all_y_exp - preds
        return -0.5 * np.sum(resid**2) / sigma**2 - len(resid) * math.log(math.sqrt(2 * math.pi)*sigma)

    # ----------- initialise with prior samples -------------------------
    n_par = len(param_names)
    def sample_prior(size):
        out = np.zeros((size, n_par))
        for j, name in enumerate(param_names):
            kind, a, b = priors[name]
            if kind == "uniform":
                out[:, j] = np.random.uniform(a, b, size)
            else:
                out[:, j] = np.random.normal(a, b, size)
        return out

    samples = sample_prior(nsamples)
    logpost = np.array([log_prior(s) + log_likelihood(s) for s in samples])

    # ----------- subset-simulation loop --------------------------------
    level = 0
    while level < max_levels - 1:
        level += 1
        thresh = np.quantile(logpost, 1 - p0)  # keep top p0
        keep_idx = logpost >= thresh
        seeds = samples[keep_idx]

        # Transitional MCMC around each seed
        new_samples = []
        for seed in seeds:
            theta = seed.copy()
            for _ in range(int(nsamples / seeds.shape[0])):
                prop = theta + np.random.normal(0, 0.2, n_par)  # fixed small proposal
                if log_prior(prop) == -np.inf:
                    continue
                lp_prop = log_prior(prop) + log_likelihood(prop)
                lp_curr = log_prior(theta) + log_likelihood(theta)
                if math.log(random.random()) < lp_prop - lp_curr:
                    theta = prop
                new_samples.append(theta.copy())

        samples = np.array(new_samples)[:nsamples]
        logpost = np.array([log_prior(s) + log_likelihood(s) for s in samples])

    # ----------- outputs -----------------------------------------------
    best_idx   = int(np.argmax(logpost))
    map_params = dict(zip(param_names, samples[best_idx]))
    return map_params, samples


# ──────────────────────────────────────────────────────────────────────────
#                     GUI  (similar style to Enumeration)
# ──────────────────────────────────────────────────────────────────────────
class MethodWindow:  # noqa: E306  (re-declared, hides earlier import)
    def __init__(self, root, material, model_data, proceed_callback_back):
        self.root   = root
        self.mat    = material
        self.model  = model_data
        self._back  = proceed_callback_back

        # window --------------------------------------------------------
        self.root.title("BUS Method")
        geom = gm.get_centered_geometry(gm.get_last_geometry(), 500, 700)
        self.root.geometry(geom)
        self.root.configure(bg="white")

        ImageDisplay(self.root,
                     resolve_path("assets/logos/Logo_HyperSmart.png"),
                     (300, 300), x=100, y=25)

        self.prior_type, self.prior_low, self.prior_high = {}, {}, {}
        self.mode_vars = {}
        self._build_ui()

    # ------------------------------------------------------------------ #
    def _build_ui(self):
        # ------------- parameter priors table --------------------------
        tk.Label(self.root, text="Parameter priors",
                 bg="white", font=("TkDefaultFont", 12, "bold"))\
          .place(x=20, y=200)

        tbl = tk.Frame(self.root, bg="white", relief="groove", bd=1)
        tbl.place(x=20, y=230, width=460, height=240)

        for j, h in enumerate(["Parameter", "Prior", "Low / μ", "High / σ"]):
            tk.Label(tbl, text=h, bg="white",
                     font=("Arial", 10, "bold")).grid(row=0, column=j,
                                                      padx=5, pady=5)

        def _finite(x):
            try:
                v = float(x); return v if math.isfinite(v) else ""
            except Exception:
                return ""

        for i, c in enumerate(self.model["material_constants"], start=1):
            name = c["name"]
            tk.Label(tbl, text=name, bg="white").grid(row=i, column=0, padx=4)
            v = tk.StringVar(value="Uniform")
            ttk.Combobox(tbl, textvariable=v, width=7,
                         values=["Uniform", "Normal"],
                         state="readonly").grid(row=i, column=1)
            e1, e2 = tk.Entry(tbl, width=10), tk.Entry(tbl, width=10)
            lo, hi = map(_finite, c.get("bounds", ["", ""]))
            e1.insert(0, lo); e2.insert(0, hi)
            e1.grid(row=i, column=2); e2.grid(row=i, column=3)
            self.prior_type[name]  = v
            self.prior_low [name]  = e1
            self.prior_high[name]  = e2

        # ------------- σ and subset-sim settings -----------------------
        tk.Label(self.root, text="Experimental noise σ :", bg="white")\
          .place(x=20, y=485)
        self.sigma_e = tk.Entry(self.root, width=8); self.sigma_e.place(x=170, y=485)
        self.sigma_e.insert(0, "0.05")

        tk.Label(self.root, text="Samples / level :", bg="white")\
          .place(x=250, y=485)
        self.ns_e = tk.Entry(self.root, width=6); self.ns_e.place(x=370, y=485)
        self.ns_e.insert(0, "2000")

        tk.Label(self.root, text="Target p₀ :", bg="white")\
          .place(x=20, y=510)
        self.p0_e = tk.Entry(self.root, width=6); self.p0_e.place(x=100, y=510)
        self.p0_e.insert(0, "0.1")

        # ------------- deformation-mode selector -----------------------
        tk.Label(self.root, text="Deformation modes:", bg="white")\
          .place(x=20, y=545)

        frame = tk.Frame(self.root, bg="white"); frame.place(x=20, y=570)
        avail = {
            "uniaxial": self.mat.sae_stretch.size > 1,
            "biaxial":  self.mat.ebl_stretch.size > 1,
            "pure_shear":  self.mat.ps_shear_parameter.size > 1,
            "simple_shear": self.mat.ss_shear_parameter.size > 1,
        }
        nice = {"uniaxial": "Uniaxial", "biaxial": "Biaxial",
                "pure_shear": "Pure shear", "simple_shear": "Simple shear"}
        for col, (m, ok) in enumerate(avail.items()):
            var = tk.IntVar(value=1 if ok else 0)
            ck  = tk.Checkbutton(frame, text=nice[m], variable=var, bg="white")
            ck.grid(row=0, column=col, padx=8);  ck.config(state=("normal" if ok else "disabled"))
            self.mode_vars[m] = var

        # ------------- buttons ----------------------------------------
        tk.Button(self.root, text="Run BUS", command=self._run_bus)\
          .place(x=385, y=665)
        tk.Button(self.root, text="Back", command=self._back)\
          .place(x=450, y=665)

    # ------------------------------------------------------------------ #
    def _parse_inputs(self):
        priors = {}
        for name, vtyp in self.prior_type.items():
            typ = vtyp.get()
            lo  = self.prior_low [name].get().strip()
            hi  = self.prior_high[name].get().strip()
            if typ == "Uniform":
                lo, hi = float(lo), float(hi)
                if hi <= lo:
                    raise ValueError(f"{name}: upper ≤ lower.")
                priors[name] = ("uniform", lo, hi)
            else:
                mu, sd = float(lo), float(hi)
                if sd <= 0:
                    raise ValueError(f"{name}: σ must be >0.")
                priors[name] = ("normal", mu, sd)

        sigma = float(self.sigma_e.get());  ns = int(self.ns_e.get())
        p0    = float(self.p0_e.get())
        if sigma <= 0 or ns < 100 or not (0 < p0 < 1):
            raise ValueError("σ>0, ns>=100, 0<p₀<1 required.")

        modes = [m for m,v in self.mode_vars.items() if v.get()==1]
        if not modes: raise ValueError("Select at least one mode.")

        return priors, sigma, ns, p0, modes

    # ------------------------------------------------------------------ #
    def _run_bus(self):
        try:
            priors, sigma, ns, p0, modes = self._parse_inputs()
        except ValueError as err:
            messagebox.showerror("Input error", str(err));  return

        try:
            map_params, post_samp = run_bus_solver(
                self.mat, self.model, priors, sigma,
                modes, nsamples=ns, p0=p0)
        except Exception as err:
            messagebox.showerror("BUS failed", str(err));   return

        txt = "\n".join(f"{k} = {v:g}" for k,v in map_params.items())
        messagebox.showinfo("BUS finished",
                            f"MAP parameters:\n{txt}\n\n"
                            f"Posterior samples: {post_samp.shape[0]} rows")

