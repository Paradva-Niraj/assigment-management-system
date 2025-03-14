import tkinter as tk
from tkinter import messagebox
import requests

# FastAPI URL
API_URL = "http://127.0.0.1:8000/faculty/register"

# Create GUI Window

def facultyregistration(r):
    root = tk.Toplevel(r)
    # root = tk.  Tk()
    root.title("Faculty Registration")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    root.resizable(False, False)


    # Function to Handle Faculty Registration
    def register_faculty():
        email = email_entry.get()
        password = password_entry.get()
        
        # Check if fields are empty
        if not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Prepare the request payload
        payload = {"email": email, "password": password}
        
        try:
            # Send POST request to API with JSON body
            response = requests.post(API_URL, json=payload)
            
            # Check Response
            if response.status_code == 200:
                # messagebox.showinfo("Success", "Faculty registered successfully!")
                email_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
            elif response.status_code == 400:
                messagebox.showerror("Error", "Email already registered!")
                root.destroy()
            else:
                messagebox.showerror("Error", "Failed to register faculty!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong!\n{e}")

    # GUI Design
    tk.Label(root, text="Faculty Registration Form", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(root, text="Email:").pack(anchor="w", padx=20)
    email_entry = tk.Entry(root, width=40)
    email_entry.pack(pady=5, padx=20)

    tk.Label(root, text="Password:").pack(anchor="w", padx=20)
    password_entry = tk.Entry(root, width=40, show="*")
    password_entry.pack(pady=5, padx=20)

    # Register Button
    register_button = tk.Button(root, text="Register Faculty", width=20, command=register_faculty)
    register_button.pack(pady=20)

    # Run the GUI
    root.mainloop()
