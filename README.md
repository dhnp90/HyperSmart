1	HyperSmart

HyperSmart is a scientific software tool designed for the automated or semi-automated selection of hyperelastic models and calibration of their material parameters based on experimental data.
It also centralizes experimental datasets from various scientific publications into a single, well-structured repository, facilitating comparison and reuse by researchers.


2	📖 About HyperSmart Software

HyperSmart assists scientists and engineers working with hyperelastic materials such as rubber, silicone, soft biological tissues, and foam.

Its main objectives are:

- Model Selection: Suggest the most suitable hyperelastic model for the given material and experimental data.
- Parameter Calibration: Estimate material parameters using numerical methods, including Enumeration and Bayesian Updating with Structural Reliability Methods (BUS).
- Data Repository: Aggregate experimental mechanical testing data from the literature into a centralized, standardized format (YAML).
- Educational Tool: Serve as a platform for teaching concepts in material modeling and data fitting.
    
The program provides a graphical user interface (GUI) developed in Python with Tkinter, enabling easy navigation between the experimental data repository, model library, and calibration tools.


3	🏗️ Software Framework

HyperSmart is structured around three core components:
1.	Experimental Data Repository
•	Stores data in YAML format for four main deformation modes: Uniaxial Tension, Biaxial Tension, Simple Shear, Pure Shear
•	Includes metadata such as material class, subclass, source, and citations.
•	Supports visualization of data and export for external analysis.
3.	Hyperelastic Model Library
•	Organizes isotropic, incompressible hyperelastic models into categories: Phenomenological and Micromechanical models.
•	Stores model definitions, equations, parameters, and reference sources in YAML.
•	Enables equation display and parameter selection in the GUI.
4.	Numerical Methods
•  	Enumeration Method: Brute-force search across parameter ranges.
•	BUS Method: Bayesian inference approach for parameter updating and model selection.
•	Both methods are integrated with the repository and model library for seamless workflow.


4	🖥️ Technical Details

- Language: Python
- GUI Framework: Tkinter
- Data Format: YAML
- Numerical Libraries: NumPy, SciPy
- Plotting: Matplotlib
- Version Control: Git / GitHub
