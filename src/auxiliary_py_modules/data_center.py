# data_center.py
import numpy as np

class ExperimentalData:
    def __init__(self):
        # Initialize a string for the name of the material
        self.material_name = ""

        # Initialize the vectors that will receive experimental data
        self.sae_stretch = np.array([])
        self.sae_stress = np.array([])
        self.ebl_stretch = np.array([])
        self.ebl_stress = np.array([])
        self.ss_shear_parameter = np.array([])
        self.ss_stress = np.array([])
        self.ps_shear_parameter = np.array([])
        self.ps_stress = np.array([])

        # Stress Information
        self.stress_measure = 0     # Nominal as default -> stress_measure = 0, Cauchy -> stress_measure = 1

        # Initialize the material constants of the hyperelastic model
        self.a1 = 0         
        self.a2 = 0         
        self.a3 = 0
        self.a4 = 0
        self.a5 = 0
        self.a6 = 0
        self.a7 = 0
        self.a8 = 0
        self.a9 = 0
        self.a10 = 0
        self.a11 = 0
        self.a12 = 0

    # Method to assign experimental data input to the np.arrays 
    def assign_vector(self, vector_name, values):
        if hasattr(self, vector_name):
            setattr(self, vector_name, np.array(values))
        else:
            print(f"Vector '{vector_name}' does not exist")
    
    # Get method to use the np.arrays (experimental data)
    def get_vector(self, vector_name):
        return getattr(self, vector_name, None)

    # Mehtod to assign experimental data input to the material constants
    def assign_constant(self, constant_name, value):
        if hasattr(self, constant_name):
            setattr(self, constant_name, value)
        else:
            print(f"Constant '{constant_name}' does not exist")

    # Method to assign value to the constant that define the stress measure 
    def assign_stress_measure(self, stress_constant, value):
        setattr(self, stress_constant, value)

    # Get method to use the constant values (material parameters)
    def get_constant(self, constant_name):
        return getattr(self, constant_name, None)

    # Method to assign the material name given by the user
    def assign_material_name(self, name):
        self.material_name = name

    # Get method to use the material name given by user
    def get_material_name(self):
        return self.material_name

    # Get method to use the stress measure constant
    def get_stress_constant(self):
        return self.stress_measure
