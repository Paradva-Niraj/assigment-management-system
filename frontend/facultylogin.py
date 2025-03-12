import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000/faculty/login"


def facultylogin(r):
    login_window = tk.Toplevel(r)
    login_window.title("Faculty Login")
    login_window.geometry("600x600")
    login_window.resizable(False, False)

    tk.Label(login_window, text="Faculty Login", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(login_window, text="Email:").pack(anchor="w", padx=20)
    email_entry = tk.Entry(login_window, width=40)
    email_entry.pack(pady=5, padx=20)

    tk.Label(login_window, text="Password:").pack(anchor="w", padx=20)
    password_entry = tk.Entry(login_window, width=40, show="*")
    password_entry.pack(pady=5, padx=20)

    # Faculty Login Function
    def login_faculty():
        email = email_entry.get()
        password = password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Prepare the request payload
        payload = {"email": email, "password": password}
        
        try:
            headers = {"Content-Type": "application/json"}  # REQUIRED for JSON requests
            response = requests.post(API_URL, json=payload, headers=headers)

            if response.status_code == 200:
                result = response.json()
                messagebox.showinfo("Success", f"Login Successful!\nAccess Token:\n{result['access_token']}")
                email_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
            elif response.status_code == 400:
                messagebox.showerror("Error", "Invalid Credentials!")
            else:
                messagebox.showerror("Error", "Login Failed!")

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong!\n{e}")


    tk.Button(login_window, text="Login", width=20, command=login_faculty).pack(pady=20)
