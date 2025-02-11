'''
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def get_details(self):
        return f"The book '{self.title}' was written by {self.author}."

class Library:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def __str__(self):
        return f"Library '{self.name}' contains {len(self.books)} books " + ", ".join([book.title for book in self.books]) 

    

book1 = Book("Caminho", "Josemaria Escriva")
book2 = Book("Sobre a China", "Henry Kissinger")
book3 = Book("O Capital", "Karl Marx")

book1.get_details()
print(book1.get_details())

list_1 = Library("Library 1")
list_1.add_book(book1)
list_1.add_book(book2)
list_1.add_book(book3)

print(list_1)

import tkinter as tk

root = tk.Tk()  # Create the main window
root.title("My First Tkinter App")
root.geometry("300x200")  # Set window size

label = tk.Label(root, text="Welcome to Tkinter!")
label.pack()

root.mainloop()  # Start the application loop
'''
import customtkinter
print("CustomTkinter installed successfully!")