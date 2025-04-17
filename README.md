

# <img src="/frontend/icon.ico" alt="App Icon" width="25">  Assignment Management System (AMS)

The **Assignment Management System (AMS)** is a desktop application built with **Tkinter (Python)** for students and faculty to easily manage academic assignments in an offline environment.

---

## 🚀 Features

### 👨‍🏫 Faculty:
- Register and log in securely
- Create and assign assignments
- View student submissions

### 👨‍🎓 Students:
- Register and log in
- View assignments and deadlines
- Submit assignments digitally
- Track submission status 
---

## 🖥️ Technologies Used

- Python 🐍
- Tkinter for GUI 🖼️
- FastAPI (backend)
- PyInstaller (for .exe packaging)

---

## 🧾 Installation

1. Download the latest `.exe` file from the [Releases](https://github.com/Paradva-Niraj/assigment-management-system/releases/tag/V1.0) section.
2. Double-click to run — no installation needed!
3. Make sure all supporting files (icons, etc.) are in the same directory (if required).

---

## 📦 Build Instructions (For Developers)

To generate the `.exe` file locally:

```bash
pyinstaller --onefile --windowed --icon=icon.ico main.py
