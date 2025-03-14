import tkinter as tk
from tkinter import messagebox
import requests

# redirection components


# FastAPI API URLs
REGISTER_API_URL = "http://127.0.0.1:8000/faculty/register"
LOGIN_API_URL = "http://127.0.0.1:8000/faculty/login"

# Function to Open Faculty Registration Window
# def open_register(root):
#     import facultyreg as f  
#     f.facultyregistration(root)


# Function to Open Faculty Login Window
def open_login():
    import facultylogin as fl
    root.destroy()
    fl.facultylogin()

def open_student_login():
    import studentlogin as sl
    root.destroy()
    sl.studentlogin()

# Main Application Window
root = tk.Tk()
root.title("Assignment management system")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
root.resizable(False, False)

tk.Label(root, text="Welcome to Faculty Management", font=("Arial", 14, "bold")).pack(pady=20)

tk.Button(root, text="Faculty Login", width=20, command=lambda: open_login()).pack(pady=10)
tk.Button(root, text="Student Login", width=20, command=lambda: open_student_login()).pack(pady=10)

root.mainloop()
