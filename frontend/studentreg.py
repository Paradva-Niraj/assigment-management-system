import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000/student/register"

def studentregistration(r):
    root = tk.Toplevel(r)
    root.title("Student Registration")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    root.resizable(False, False)

    def register_student():
        # prn = prn_entry.get()
        name = name_entry.get()
        semester = semester_entry.get()
        password = password_entry.get()
        
        if not name or not semester or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        payload = {"name": name, "semester": semester, "password": password}
        
        try:
            response = requests.post(API_URL, json=payload)
            data = response.json()  # Convert response to dictionary

            if response.status_code == 200:
                prn = data.get("prn", "N/A")  # Extract PRN safely
                messagebox.showinfo("Success", f"Student registered successfully!\nPRN: {prn}")
                root.destroy()
            elif response.status_code == 400:
                messagebox.showerror("Error", "PRN already registered!")
            else:
                messagebox.showerror("Error", "Registration failed!")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong!\n{e}")

    tk.Label(root, text="Student Registration Form", font=("Arial", 14, "bold")).pack(pady=10)

    # tk.Label(root, text="PRN:").pack(anchor="w", padx=20)
    # prn_entry = tk.Entry(root, width=40)
    # prn_entry.pack(pady=5, padx=20)

    tk.Label(root, text="Name:").pack(anchor="w", padx=20)
    name_entry = tk.Entry(root, width=40)
    name_entry.pack(pady=5, padx=20)

    tk.Label(root, text="Semester:").pack(anchor="w", padx=20)
    semester_entry = tk.Entry(root, width=40)
    semester_entry.pack(pady=5, padx=20)

    tk.Label(root, text="Password:").pack(anchor="w", padx=20)
    password_entry = tk.Entry(root, width=40, show="*")
    password_entry.pack(pady=5, padx=20)

    tk.Button(root, text="Register Student", width=20, command=register_student).pack(pady=20)

    root.mainloop()
