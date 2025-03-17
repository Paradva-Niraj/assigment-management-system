import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import requests
import os

API_URL = "http://127.0.0.1:8000"
    
def studentlogin():
    login_window = tk.Tk()
    login_window.title("Student Login")
    login_window.geometry(f"{login_window.winfo_screenwidth()}x{login_window.winfo_screenheight()}+0+0")

    tk.Label(login_window, text="Student Login", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(login_window, text="PRN:").pack(anchor="w", padx=20)
    prn_entry = tk.Entry(login_window, width=40)
    prn_entry.pack(pady=5, padx=20)

    tk.Label(login_window, text="Password:").pack(anchor="w", padx=20)
    password_entry = tk.Entry(login_window, width=40, show="*")
    password_entry.pack(pady=5, padx=20)

    def login_student():
        prn = prn_entry.get()
        password = password_entry.get()
        
        if not prn or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Special credentials to open registration
        if prn == "admin" and password == "admin123":
            import studentreg as sr  
            sr.studentregistration(login_window)
        else:
            response = requests.post(f"{API_URL}/student/login", json={"prn": prn, "password": password})
        
            try:
                result = response.json()
            except requests.exceptions.JSONDecodeError:
                messagebox.showerror("Error", "Invalid server response")
                return
            
            if response.status_code == 200:
                login_window.destroy()
                student_dashboard(prn, result["semester"])
            else:
                messagebox.showerror("Error", result.get("detail", "Invalid Credentials!"))

    tk.Button(login_window, text="Login", width=20, command=login_student).pack(pady=20)
    login_window.mainloop()

def student_dashboard(prn, semester):
    dashboard_window = tk.Tk()  
    dashboard_window.title("Student Dashboard")
    dashboard_window.geometry(f"{dashboard_window.winfo_screenwidth()}x{dashboard_window.winfo_screenheight()}+0+0")

    tk.Label(dashboard_window, text=f"Welcome PRN: {prn}", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(dashboard_window, text=f"Semester: {semester}", font=("Arial", 12)).pack(pady=5)

    columns = ("ID", "Title", "Subject", "Description", "File")
    tree = ttk.Treeview(dashboard_window, columns=columns, show="headings")

    tree.heading("ID", text="ID")
    tree.column("ID", width=50)
    tree.heading("Title", text="Title")
    tree.column("Title", width=200)
    tree.heading("Subject", text="Subject")
    tree.column("Subject", width=150)
    tree.heading("Description", text="Description")
    tree.column("Description", width=300)
    tree.heading("File", text="File Path")
    tree.column("File", width=200)

    tree.pack(pady=10)

    def fetch_assignments():
        response = requests.get(f"{API_URL}/student/{semester}/assignments")  

        try:
            assignments = response.json()
        except requests.exceptions.JSONDecodeError:
            messagebox.showerror("Error", "Invalid server response")
            return

        tree.delete(*tree.get_children())

        if isinstance(assignments, list):
            for assignment in assignments:
                tree.insert("", tk.END, values=(
                    assignment['id'], 
                    assignment['title'], 
                    assignment['subject'], 
                    assignment['description'], 
                    assignment['file_path']
                ))
        else:
            messagebox.showerror("Error", "No assignments found")

    def download_assignment():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an assignment to download.")
            return

        item = tree.item(selected_item)
        file_path = item["values"][4]  # Extract file path from selected row
        
        if not file_path:
            messagebox.showerror("Error", "No file available for this assignment.")
            return

        file_name = os.path.basename(file_path)  
        save_location = filedialog.asksaveasfilename(
            initialfile=file_name,
            defaultextension="",
            filetypes=[("All Files", "*.*")]
        )

        if save_location:
            try:
                file_response = requests.get(f"{API_URL}/download/{file_name}", stream=True)
                if file_response.status_code == 200:
                    with open(save_location, "wb") as f:
                        for chunk in file_response.iter_content(chunk_size=1024):
                            f.write(chunk)
                    messagebox.showinfo("Success", "Assignment downloaded successfully!")
                else:
                    messagebox.showerror("Error", "Failed to download the file.")
            except Exception as e:
                messagebox.showerror("Error", f"Download failed: {e}")

    fetch_assignments()
    def logout():
        dashboard_window.destroy()  # Close the dashboard window
        studentlogin() 
    tk.Button(dashboard_window, text="Refresh", command=fetch_assignments).pack(pady=5)
    tk.Button(dashboard_window, text="Download Assignment", command=download_assignment).pack(pady=5)
    tk.Button(dashboard_window, text="Logout", command=logout).pack(pady=5)

    dashboard_window.mainloop()
