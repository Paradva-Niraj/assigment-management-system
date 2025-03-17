import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import requests
from fastapi import FastAPI, Form, UploadFile, File, Depends
from sklearn import tree



API_URL = "http://127.0.0.1:8000"
access_token = None

def facultylogin():
    login_window = tk.Tk()
    login_window.title("Faculty Login")
    login_window.geometry(f"{login_window.winfo_screenwidth()}x{login_window.winfo_screenheight()}+0+0")

    tk.Label(login_window, text="Faculty Login", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(login_window, text="Email:").pack(anchor="w", padx=20)
    email_entry = tk.Entry(login_window, width=40)
    email_entry.pack(pady=5, padx=20)

    tk.Label(login_window, text="Password:").pack(anchor="w", padx=20)
    password_entry = tk.Entry(login_window, width=40, show="*")
    password_entry.pack(pady=5, padx=20)

    def login_faculty():
        global access_token
        email = email_entry.get()
        password = password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        if email=="admin" and password=="admin123":
            # Function to Open Faculty Registration Window
            import facultyreg as f  
            f.facultyregistration(login_window)
        else:
            response = requests.post(f"{API_URL}/faculty/login", json={"email": email, "password": password})
        
            try:
                result = response.json()
            except requests.exceptions.JSONDecodeError:
                messagebox.showerror("Error", "Invalid server response")
                return
            
            if response.status_code == 200 and "access_token" in result:
                access_token = result["access_token"]
                login_window.destroy()
                faculty_dashboard(email)
            else:
                messagebox.showerror("Error", result.get("detail", "Invalid Credentials!"))

    tk.Button(login_window, text="Login", width=20, command=login_faculty).pack(pady=20)
    login_window.mainloop()

from tkinter import ttk

def faculty_dashboard(email):
    dashboard_window = tk.Tk()
    dashboard_window.title("Dashboard")
    dashboard_window.geometry(f"{dashboard_window.winfo_screenwidth()}x{dashboard_window.winfo_screenheight()}+0+0")   

    tk.Label(dashboard_window, text=f"Welcome {email}", font=("Arial", 14, "bold")).pack(pady=10)

    # Create Treeview with 3 columns (ID, Title, Delete Button)
    columns = ("ID", "Title", "Subject", "Delete")
    tree = ttk.Treeview(dashboard_window, columns=columns, show="headings")

    tree.heading("ID", text="ID")
    tree.column("ID", width=50)
    tree.heading("Title", text="Title")
    tree.column("Title", width=200)
    tree.heading("Subject", text="Subject")
    tree.column("Subject", width=150)
    tree.heading("Delete", text="Action")
    tree.column("Delete", width=100)

    tree.pack(pady=10)

    # Function to populate the Treeview
    def fetch_assignments():
        response = requests.get(f"{API_URL}/faculty/{email}/assignments")

        try:
            assignments = response.json()
        except requests.exceptions.JSONDecodeError:
            messagebox.showerror("Error", "Invalid server response")
            return

        tree.delete(*tree.get_children())  # Clear previous entries

        if isinstance(assignments, list):
            for assignment in assignments:
                if "id" in assignment and "title" in assignment and "subject" in assignment:
                    tree.insert("", tk.END, values=(assignment['id'], assignment['title'], assignment['subject'], "Delete"))
                else:
                    tree.insert("", tk.END, values=("N/A", "Invalid assignment data", "N/A", "N/A"))
        else:
            messagebox.showerror("Error", assignments.get("message", "No assignments found"))

    fetch_assignments()

    # Function to delete an assignment
    def delete_selected_assignment():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an assignment to delete")
            return

        assignment_id = tree.item(selected_item)["values"][0]  # Get ID from selected row

        response = requests.delete(f"{API_URL}/faculty/delete_assignment/{assignment_id}")
        
        if response.status_code == 200:
            messagebox.showinfo("Success", "Assignment deleted successfully")
            fetch_assignments()  # Refresh after deletion
        else:
            messagebox.showerror("Error", "Failed to delete assignment")

    def view_assignment():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select an assignment to view submissions")
            return

        assignment_id = tree.item(selected_item)['values'][0]
        response = requests.get(f"{API_URL}/faculty/assignment/{assignment_id}/submissions")

        if response.status_code == 200:
            submissions = response.json()

            # Create new window for submissions
            submissions_window = tk.Toplevel(dashboard_window)
            submissions_window.title(f"Submissions for Assignment {assignment_id}")

            # Create Treeview for submissions
            submissions_tree = ttk.Treeview(submissions_window, columns=("ID", "Student PRN", "File Path", "Submitted At", "Download"), show="headings")

            submissions_tree.heading("ID", text="ID")
            submissions_tree.column("ID", width=50)
            submissions_tree.heading("Student PRN", text="Student PRN")
            submissions_tree.column("Student PRN", width=100)
            submissions_tree.heading("File Path", text="File Path")
            submissions_tree.column("File Path", width=200)
            submissions_tree.heading("Submitted At", text="Submitted At")
            submissions_tree.column("Submitted At", width=150)
            submissions_tree.heading("Download", text="Download Submission")
            submissions_tree.column("Download", width=150)

            submissions_tree.pack(fill="both", expand=True)

            # Function to download submission
            def download_submission(event):
                selected = submissions_tree.selection()
                if not selected:
                    messagebox.showerror("Error", "Select a submission to download")
                    return

                submission_id = submissions_tree.item(selected)["values"][0]  # Get submission ID
                file_response = requests.get(f"{API_URL}/faculty/assignment/submission/{submission_id}/download", stream=True)

                if file_response.status_code == 200:
                    # Extract filename from Content-Disposition header
                    content_disposition = file_response.headers.get("Content-Disposition", "")
                    filename = "submission.pdf"  # Default filename
                    
                    if "filename=" in content_disposition:
                        filename = content_disposition.split("filename=")[-1].strip().replace('"', '')

                    # Ask where to save, setting the default filename
                    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile=filename, filetypes=[("PDF files", "*.pdf"), ("All Files", "*.*")])
                    
                    if file_path:
                        with open(file_path, "wb") as file:
                            file.write(file_response.content)
                        
                        messagebox.showinfo("Success", f"File downloaded successfully!\nSaved at: {file_path}")
                else:
                    messagebox.showerror("Error", "Failed to download file")


            # Insert submissions into Treeview
            for sub in submissions:
                submissions_tree.insert("", "end", values=(sub["id"], sub["student_prn"], sub["file_path"], sub["submitted_at"], "Download"))

            # Bind double-click to download submission
            submissions_tree.bind("<Double-1>", download_submission)

        else:
            messagebox.showerror("Error", "Failed to fetch assignment submissions")


    def logout():
        dashboard_window.destroy()
        facultylogin()

    # Add Delete Button
    delete_button = tk.Button(dashboard_window, text="Delete Selected Assignment", command=delete_selected_assignment)
    delete_button.pack(pady=5)

    # Add Refresh Button
    tk.Button(dashboard_window, text="Refresh", command=fetch_assignments).pack(pady=5)
    tk.Button(dashboard_window, text="Upload Assignment", command=lambda: upload_assignment(email, dashboard_window)).pack(pady=5)
    tk.Button(dashboard_window, text="View Submissions", command=view_assignment).pack(pady=5)
    tk.Button(dashboard_window, text="Logout", command=logout).pack(pady=5)
    dashboard_window.mainloop()

def upload_assignment(email, parent_window):
    upload_window = tk.Toplevel(parent_window)
    upload_window.title("Upload Assignment")
    upload_window.geometry(f"{upload_window.winfo_screenwidth()}x{upload_window.winfo_screenheight()}+0+0")


    tk.Label(upload_window, text="Title:").pack(anchor="w", padx=20)
    title_entry = tk.Entry(upload_window, width=40)
    title_entry.pack(pady=5, padx=20)

    tk.Label(upload_window, text="Description:").pack(anchor="w", padx=20)
    desc_entry = tk.Entry(upload_window, width=40)
    desc_entry.pack(pady=5, padx=20)

    tk.Label(upload_window, text="Semester:").pack(anchor="w", padx=20)
    sem_entry = tk.Entry(upload_window, width=40)
    sem_entry.pack(pady=5, padx=20)

    tk.Label(upload_window, text="Subject:").pack(anchor="w", padx=20)
    sub_entry = tk.Entry(upload_window, width=40)
    sub_entry.pack(pady=5, padx=20)

    file_path = tk.StringVar()

    def choose_file():
        path = filedialog.askopenfilename()
        file_path.set(path)

    tk.Button(upload_window, text="Choose File", command=choose_file).pack(pady=5)

    def submit_assignment():
        if not (title_entry.get() and desc_entry.get() and sem_entry.get() and sub_entry.get() and file_path.get()):
            messagebox.showerror("Error", "All fields are required!")
            return

        files = {"file": open(file_path.get(), "rb")}
        data = {
            "title": title_entry.get(),
            "description": desc_entry.get(),
            "semester": sem_entry.get(),
            "subject": sub_entry.get(),
            "uploaded_by": email
        }

        response = requests.post(f"{API_URL}/faculty/upload_assignment", data=data, files=files)
        
        try:
            result = response.json()
        except requests.exceptions.JSONDecodeError:
            messagebox.showerror("Error", "Invalid server response")
            return

        if response.status_code == 200:
            messagebox.showinfo("Success", "Assignment uploaded successfully!")
            upload_window.destroy()
        else:
            messagebox.showerror("Error", result.get("message", "Upload failed!"))

    tk.Button(upload_window, text="Upload", command=submit_assignment).pack(pady=10)