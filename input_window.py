import tkinter as tk
from tkinter import messagebox
import numpy as np

def convert_to_vectors():
    try:
        # Get the input text from the first text widget
        input_text1 = text_widget1.get("1.0", tk.END).strip()
        # Replace commas with dots
        input_text1 = input_text1.replace(',', '.')
        # Split the input text into values
        input_values1 = [float(x) for x in input_text1.split()]
        # Create a NumPy array from the input values
        vector1 = np.array(input_values1)
        
        # Get the input text from the second text widget
        input_text2 = text_widget2.get("1.0", tk.END).strip()
        # Replace commas with dots
        input_text2 = input_text2.replace(',', '.')
        # Split the input text into values
        input_values2 = [float(x) for x in input_text2.split()]
        # Create a NumPy array from the input values
        vector2 = np.array(input_values2)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers separated by spaces.")

def main():
    global text_widget1, text_widget2, result_label1, result_label2
    
    # Create the main window
    root = tk.Tk()
    root.title("Excel to NumPy Vectors")
    root.geometry("450x600")  # Increase width for better input space
    
    # Create a label with instructions
    instructions = tk.Label(root, text="Data Input \n(Excel Copy/Paste Avaiable)", font=("Helvetica", 10), wraplength=500)
    instructions.pack(pady=10)

    # Create a frame for labels and text widgets
    frame = tk.Frame(root)
    frame.pack(pady=10)
    
    # Create a sub-frame for column labels
    label_frame = tk.Frame(frame)
    label_frame.pack()

    # Add "x" and "y" labels with precise positioning using place()
    label_x = tk.Label(root, text="x", font=("Arial", 12, "bold"))
    label_x.place(x=130, y=60)  # Adjust x and y as needed

    label_y = tk.Label(root, text="y", font=("Arial", 12, "bold"))
    label_y.place(x=285, y=60)  # Adjust x and y as needed
    
    # Create a frame for the text widgets and scrollbars
    frame = tk.Frame(root)
    frame.pack(pady=10)
    
    # Create the first text widget for input with increased height
    text_widget1 = tk.Text(frame, height=28, width=15)
    text_widget1.pack(side=tk.LEFT, padx=10)
    
    # Add a scrollbar to the first text widget
    scrollbar1 = tk.Scrollbar(frame, command=text_widget1.yview)
    text_widget1.config(yscrollcommand=scrollbar1.set)
    scrollbar1.pack(side=tk.LEFT, fill=tk.Y)
    
    # Create the second text widget for input with increased height
    text_widget2 = tk.Text(frame, height=28, width=15)
    text_widget2.pack(side=tk.LEFT, padx=10)
    
    # Add a scrollbar to the second text widget
    scrollbar2 = tk.Scrollbar(frame, command=text_widget2.yview)
    text_widget2.config(yscrollcommand=scrollbar2.set)
    scrollbar2.pack(side=tk.LEFT, fill=tk.Y)
    
    # Create a button to convert input to NumPy vectors
    convert_button = tk.Button(root, text="Assign Values", command=convert_to_vectors)
    convert_button.pack(pady=10)
    
    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()










