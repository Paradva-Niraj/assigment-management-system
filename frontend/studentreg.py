import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import requests
import openpyxl
import os

# local
# API_URL = "http://127.0.0.1:8000/student/register"
API_URL = "https://assigment-management-system.onrender.com/student/register"

EXCEL_FILE = "student_records.xlsx"

if not os.path.exists(EXCEL_FILE):
        # Create a new workbook and sheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Student Data"

        # Add headers
        sheet.append(["prn","name", "Password"])

        # Save the file
        workbook.save(EXCEL_FILE)

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
                wb=openpyxl.load_workbook("student_records.xlsx")
                sheet = wb.active

                sheet.append([prn,name,password])
                wb.save("student_records.xlsx")
                messagebox.showinfo("Success", f"Student registered successfully!\nPRN: {prn}")
                root.destroy()
            elif response.status_code == 400:
                messagebox.showerror("Error", "PRN already registered!")
            else:
                messagebox.showerror("Error", "Registration failed!")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong!\n{e}")

    def download_excel():
        if not os.path.exists('./student_records.xlsx'):
            messagebox.showerror("Error", "Excel file not found.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel Files", "*.xlsx")],
                                                 title="Save Faculty Records As")
        if save_path:
            try:
                shutil.copy(EXCEL_FILE, save_path)
                messagebox.showinfo("Success", "File downloaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")

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

    download_button = tk.Button(root, text="Download SWtudent Excel", width=25, command=download_excel)
    download_button.pack(pady=5)

    root.mainloop()
