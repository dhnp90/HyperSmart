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
        
        # Display the NumPy arrays in the result labels
        result_label1.config(text=f"NumPy Vector 1: {vector1}")
        result_label2.config(text=f"NumPy Vector 2: {vector2}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers separated by spaces.")

def main():
    global text_widget1, text_widget2, result_label1, result_label2
    
    # Create the main window
    root = tk.Tk()
    root.title("Excel to NumPy Vectors")
    root.geometry("600x600")  # Increase width for better input space
    
    # Create a label with instructions
    instructions = tk.Label(root, text="Input each value in a new line (two columns):", wraplength=500)
    instructions.pack(pady=10)
    
    # Create a frame for the text widgets and scrollbars
    frame = tk.Frame(root)
    frame.pack(pady=10)
    
    # Create the first text widget for input with increased height
    text_widget1 = tk.Text(frame, height=20, width=15)
    text_widget1.pack(side=tk.LEFT, padx=10)
    
    # Add a scrollbar to the first text widget
    scrollbar1 = tk.Scrollbar(frame, command=text_widget1.yview)
    text_widget1.config(yscrollcommand=scrollbar1.set)
    scrollbar1.pack(side=tk.LEFT, fill=tk.Y)
    
    # Create the second text widget for input with increased height
    text_widget2 = tk.Text(frame, height=20, width=15)
    text_widget2.pack(side=tk.LEFT, padx=10)
    
    # Add a scrollbar to the second text widget
    scrollbar2 = tk.Scrollbar(frame, command=text_widget2.yview)
    text_widget2.config(yscrollcommand=scrollbar2.set)
    scrollbar2.pack(side=tk.LEFT, fill=tk.Y)
    
    # Create a button to convert input to NumPy vectors
    convert_button = tk.Button(root, text="Convert to NumPy Vectors", command=convert_to_vectors)
    convert_button.pack(pady=10)
    
    # Create labels to display the results
    result_label1 = tk.Label(root, text="NumPy Vector 1: ")
    result_label1.pack(pady=10)
    result_label2 = tk.Label(root, text="NumPy Vector 2: ")
    result_label2.pack(pady=10)
    
    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()










