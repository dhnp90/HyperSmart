# data_center.py
import numpy as np

class ExperimentalData:
    def __int__(self):
        self.sae_stretch = np.array([])
        self.sae_stress = np.array([])
        self.ebl_stretch = np.array([])
        self.ebl_stress = np.array([])
        self.ss_shear_parameter = np.array([])
        self.ss_stress = np.array([])
        self.ps_shear_parameter = np.array([])
        self.ps_stress = np.array([])

    def assign_values(self, vector_name, values):
        if hasattr(self, vector_name):
            setattr(self, vector_name, np.array(values))
        else:
            print(f"Vector '{vector_name}' does not exist")

    def get_vector(self, vector_name):
        return getattr(self, vector_name, None)
            