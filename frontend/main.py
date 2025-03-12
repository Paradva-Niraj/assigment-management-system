import tkinter as tk
from tkinter import messagebox
import requests

# redirection components
import facultyreg as f
import facultylogin as fl


# FastAPI API URLs
REGISTER_API_URL = "http://127.0.0.1:8000/faculty/register"
LOGIN_API_URL = "http://127.0.0.1:8000/faculty/login"

# Function to Open Faculty Registration Window
def open_register(root):
    f.facultyregistration(root)


# Function to Open Faculty Login Window
def open_login(root):
    fl.facultylogin(root)


# Main Application Window
root = tk.Tk()
root.title("Faculty Management System")
root.geometry("600x600")
root.resizable(False, False)

tk.Label(root, text="Welcome to Faculty Management", font=("Arial", 14, "bold")).pack(pady=20)

tk.Button(root, text="Faculty Login", width=20, command=lambda: open_login(root)).pack(pady=10)
tk.Button(root, text="Faculty Register", width=20, command=lambda: open_register(root)).pack(pady=10)

root.mainloop()
