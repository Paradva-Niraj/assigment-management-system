import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import requests

API_URL = "http://127.0.0.1:8000"
access_token = None

def facultylogin(r):
    login_window = tk.Toplevel(r)
    login_window.title("Faculty Login")
    login_window.geometry("400x300")

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

        response = requests.post(f"{API_URL}/faculty/login", json={"email": email, "password": password})
        if response.status_code == 200:
            result = response.json()
            access_token = result["access_token"]
            # messagebox.showinfo("Success", "Login Successful!")
            login_window.destroy()
            faculty_dashboard()
        else:
            messagebox.showerror("Error", "Invalid Credentials!")

    tk.Button(login_window, text="Login", width=20, command=login_faculty).pack(pady=20)
    login_window.mainloop()


def faculty_dashboard():
    dashboard = tk.Toplevel()
    dashboard.title("Faculty Dashboard")
    dashboard.geometry("500x500")

    def upload_assignment(
        title: str = Form(...), 
        description: str = Form(...), 
        semester: str = Form(...), 
        subject: str = Form(...),
        file: UploadFile = File(...),
        faculty: dict = Depends(get_current_user),  # Assuming get_current_user returns user info
        db: Session = Depends(get_db)
    ):
        file_location = f"{UPLOAD_DIR}/{file.filename}"

        # Save the uploaded file
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Create assignment entry in DB
        new_assignment = Assignment(
            title=title,
            description=description,
            file_path=file_location,
            semester=semester,
            subject=subject,
            uploaded_by=faculty["id"]  # Assuming faculty is a dictionary
        )
        db.add(new_assignment)
        db.commit()
        db.refresh(new_assignment)

        return {"message": "Assignment uploaded successfully!", "file_path": file_location}

    def view_assignments():
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{API_URL}/assignments/view", headers=headers)
        if response.status_code == 200:
            assignments = response.json()

            view_window = tk.Toplevel(dashboard)
            view_window.title("View Assignments")
            view_window.geometry("500x400")

            tree = ttk.Treeview(view_window, columns=("ID", "Title", "Subject"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Title", text="Title")
            tree.heading("Subject", text="Subject")
            tree.pack(fill="both", expand=True)

            for assignment in assignments:
                tree.insert("", "end", values=(assignment["id"], assignment["title"], assignment["subject"]))

            def delete_assignment():
                selected_item = tree.selection()
                if selected_item:
                    assignment_id = tree.item(selected_item, "values")[0]
                    response = requests.delete(f"{API_URL}/assignments/delete/{assignment_id}", headers=headers)
                    if response.status_code == 200:
                        messagebox.showinfo("Success", "Assignment deleted successfully!")
                        tree.delete(selected_item)
                    else:
                        messagebox.showerror("Error", "Deletion failed!")

            delete_button = tk.Button(view_window, text="Delete Selected", command=delete_assignment)
            delete_button.pack(pady=10)

    def logout():
        global access_token
        access_token = None
        messagebox.showinfo("Logged Out", "You have been logged out!")
        dashboard.destroy()

    tk.Button(dashboard, text="Upload Assignment", width=30, command=upload_assignment).pack(pady=10)
    tk.Button(dashboard, text="View Assignments", width=30, command=view_assignments).pack(pady=10)
    tk.Button(dashboard, text="Logout", width=30, command=logout, fg="red").pack(pady=10)

    dashboard.mainloop()

