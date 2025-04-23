import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import requests
import openpyxl
import os

# FastAPI URL local
# API_URL = "http://127.0.0.1:8000/faculty/register"
API_URL = "https://assigment-management-system.onrender.com/faculty/register"

# Create GUI Window
EXCEL_FILE = "faculty_records.xlsx"

if not os.path.exists(EXCEL_FILE):
        # Create a new workbook and sheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Faculty Data"

        # Add headers
        sheet.append(["Email", "Password"])

        # Save the file
        workbook.save(EXCEL_FILE)

def facultyregistration(r):
    root = tk.Toplevel(r)
    # root = tk.  Tk()
    root.title("Faculty Registration")
    # i dont want that because its hide behind of main win
    # root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    root.geometry("600x400") 
    root.resizable(False, False)


    # Function to Handle Faculty Registration
    def register_faculty():
        email = email_entry.get()
        password = password_entry.get()
        
        # Check if fields are empty
        if not email or not password:
            messagebox.showerror("Error", "All fields are required!", parent=root)
            return
        
        # Prepare the request payload
        payload = {"email": email, "password": password}
        
        try:
            # Send POST request to API with JSON body
            response = requests.post(API_URL, json=payload)
            
            # Check Response
            if response.status_code == 200:
                messagebox.showinfo("Success", "Faculty registered successfully!", parent=root)
                wb = openpyxl.load_workbook("faculty_records.xlsx")
                sheet = wb.active

# Add new data
                sheet.append([email, password])
                wb.save("faculty_records.xlsx")
                email_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
            elif response.status_code == 400:
                messagebox.showerror("Error", "Email already registered!", parent=root)
                root.destroy()
            else:
                messagebox.showerror("Error", "Failed to register faculty!", parent=root)
        
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong!\n{e}", parent=root)

    def download_excel():
        if not os.path.exists('faculty_records.xlsx'):
            messagebox.showerror("Error", "Excel file not found.", parent=root)
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel Files", "*.xlsx")],
                                                 title="Save Faculty Records As", parent=root)
        if save_path:
            try:
                shutil.copy(EXCEL_FILE, save_path)
                messagebox.showinfo("Success", "File downloaded successfully!", parent=root)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}", parent=root)

    # GUI Design
    tk.Label(root, text="Faculty Registration Form", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
   
    tk.Label(root, text="Email:").grid(row=1, column=1, sticky="w", pady=5)
    email_entry = tk.Entry(root, width=40)
    email_entry.grid(row=1, column=2, pady=5)

    tk.Label(root, text="Password:").grid(row=2, column=1, sticky="w", pady=5)
    password_entry = tk.Entry(root, width=40, show="*")
    password_entry.grid(row=2, column=2, pady=5)

    # Register Button
    register_button = tk.Button(root, text="Register Faculty", width=20, command=register_faculty)
    register_button.grid(row=4, column=2, padx=10, pady=5)

    download_button = tk.Button(root, text="Download Faculty Excel", width=25, command=download_excel)
    download_button.grid(row=6, column=2, padx=10, pady=5)

    # Run the GUI
    root.mainloop()
