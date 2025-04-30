# exp_data_opt_window.py
import tkinter as tk
import auxiliary_py_modules.geometry_manager as gm
from auxiliary_py_modules.image_display import ImageDisplay

class ExpDataOptions:
    def __init__(self, root, proceed_callback_input, proceed_callback_repository, proceed_callback_back):
        self.root = root
        self.proceed_callback_input = proceed_callback_input
        self.proceed_callback_repository = proceed_callback_repository
        self.proceed_callback_back = proceed_callback_back
        self.root.title("Experimental Data Options")

        # Restore previous geometry 
        geom = gm.get_centered_geometry(gm.get_last_geometry(), 500, 700)
        self.root.geometry(geom)

        # # Store the applied geometry for reuse
        # self.root.update_idletasks()
        # gm.set_last_geometry(self.root.geometry())

        # Display the main logo
        ImageDisplay(self.root, 'Logo_HyperSmart.png', (300, 300), x=100, y=25)

        # Input Experimental Data Directly Button
        input_data_button = tk.Button(self.root, text='Input Experimental Data', width=55, height=1, justify="center", command=self.proceed_callback_input)
        input_data_button.place(x=54, y=300)

        # Use Experimental Data Repository
        use_reposit_button = tk.Button(self.root, text='Use the Experimental Data Repository', width=55, height=1, justify="center", command=self.proceed_callback_repository)
        use_reposit_button.place(x=54, y=360)

        # Create button to go back to previous window
        go_back_button = tk.Button(self.root, text='Back', command=self.proceed_callback_back)
        go_back_button.place(x=450, y=665)