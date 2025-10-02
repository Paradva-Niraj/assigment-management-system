

# <img src="/frontend/icon.ico" alt="App Icon" width="25">  Assignment Management System (AMS)

### **Desktop Application for Academic Assignment Management**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange)](https://docs.python.org/3/library/tkinter.html)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Streamline academic workflows with an offline-first assignment management solution**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage-guide) • [Build](#-build-instructions) • [Contributing](#-contributing)

---

</div>

## 📖 Overview

**Assignment Management System (AMS)** is a powerful desktop application designed to simplify the management of academic assignments in educational institutions [attached_file:1]. Built with Python and Tkinter, AMS provides an intuitive graphical interface for both faculty and students to handle assignment creation, submission, and tracking—all in an offline environment [attached_file:1].

The system eliminates the need for constant internet connectivity while maintaining robust functionality for assignment workflows, making it ideal for institutions with limited connectivity or those preferring secure, local data management [attached_file:1].

---

## ✨ Features

### 🎓 Role-Based Functionality

<table>
<tr>
<td width="50%" valign="top">

#### 👨‍🏫 Faculty Features

- ✅ **Secure Authentication** - Register and log in with encrypted credentials [attached_file:1]
- ✅ **Assignment Creation** - Create detailed assignments with deadlines and requirements [attached_file:1]
- ✅ **Assignment Distribution** - Assign tasks to specific students or groups [attached_file:1]
- ✅ **Submission Management** - View and track all student submissions [attached_file:1]
- ✅ **Status Monitoring** - Real-time tracking of submission status
- ✅ **Grading System** - Evaluate and provide feedback on submissions

</td>
<td width="50%" valign="top">

#### 👨‍🎓 Student Features

- ✅ **User Registration** - Create accounts and manage profiles [attached_file:1]
- ✅ **Secure Login** - Access personalized dashboard securely [attached_file:1]
- ✅ **Assignment Overview** - View all assigned tasks and deadlines [attached_file:1]
- ✅ **Digital Submission** - Submit assignments digitally through the interface [attached_file:1]
- ✅ **Submission Tracking** - Monitor submission status in real-time [attached_file:1]
- ✅ **Deadline Reminders** - Never miss a submission deadline
- ✅ **Submission History** - Access past submissions and feedback

</td>
</tr>
</table>

### 🌟 System Highlights

- 💾 **Local Data Storage** - Secure data management on local systems
- 🎨 **Intuitive GUI** - User-friendly interface built with Tkinter [attached_file:1]
- ⚡ **Lightweight** - Minimal system resource requirements
- 🚀 **Portable** - Run directly from executable without installation [attached_file:1]
- 🔐 **Secure** - Protected user authentication and data handling

---

## 🛠 Technologies Used

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Language** | Python 3.8+ (100%) [attached_file:1] | Core application logic |
| **GUI Framework** | Tkinter [attached_file:1] | Desktop interface development |
| **Backend** | FastAPI [attached_file:1] | API and data processing |
| **Packaging** | PyInstaller [attached_file:1] | Executable generation |
| **Database** | SQLite (implied) | Local data persistence |

---

## 📂 Project Structure

```
assigment-management-system/
│
├── 📁 src/                          # Source code directory
│   ├── 📁 gui/                      # Tkinter GUI components
│   │   ├── login_screen.py          # Login interface
│   │   ├── faculty_dashboard.py     # Faculty main interface
│   │   ├── student_dashboard.py     # Student main interface
│   │   ├── assignment_form.py       # Assignment creation form
│   │   └── submission_view.py       # Submission viewer
│   │
│   ├── 📁 backend/                  # FastAPI backend
│   │   ├── auth.py                  # Authentication logic
│   │   ├── assignments.py           # Assignment management
│   │   ├── submissions.py           # Submission handling
│   │   └── database.py              # Database operations
│   │
│   ├── 📁 models/                   # Data models
│   │   ├── user.py                  # User model
│   │   ├── assignment.py            # Assignment model
│   │   └── submission.py            # Submission model
│   │
│   └── main.py                      # Application entry point
│
├── 📁 assets/                       # Application resources
│   ├── icon.ico                     # Application icon
│   └── images/                      # UI images and icons
│
├── 📁 dist/                         # Compiled executables
│   └── AMS.exe                      # Windows executable
│
├── 📁 docs/                         # Documentation
│   └── user_manual.pdf              # User guide
│
├── requirements.txt                 # Python dependencies
├── build.spec                       # PyInstaller configuration
├── LICENSE                          # License file
└── README.md                        # This file
```

---

## 🚀 Installation

### Option 1: Download Pre-built Executable (Recommended)

1. **Download the latest release:**
   - Visit the [Releases](https://github.com/Paradva-Niraj/assigment-management-system/releases) section [attached_file:1]
   - Download the latest `.exe` file [attached_file:1]

2. **Run the application:**
   - Double-click `AMS.exe` to launch—no installation needed! [attached_file:1]
   - Ensure all supporting files (icons, assets) are in the same directory [attached_file:1]

3. **First-time setup:**
   - Create admin/faculty accounts on first launch
   - Configure initial settings

> **Note:** Windows Defender may show a warning for unsigned executables. Click "More info" → "Run anyway" to proceed.

---

### Option 2: Run from Source (For Developers)

#### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

#### Installation Steps

1. **Clone the repository:**

```
git clone https://github.com/Paradva-Niraj/assigment-management-system.git
cd assigment-management-system
```

2. **Create virtual environment (recommended):**

```
python -m venv venv
```

On Windows:
```
venv\Scripts\activate
```

On macOS/Linux:
```
source venv/bin/activate
```

3. **Install dependencies:**

```
pip install -r requirements.txt
```

4. **Run the application:**

```
python main.py
```

---

## 📖 Usage Guide

### For Faculty

1. **Login/Register:**
   - Launch the application
   - Select "Faculty" role
   - Register (first time) or login with credentials

2. **Create Assignment:**
   - Navigate to "Create Assignment"
   - Fill in assignment details (title, description, deadline, attachments)
   - Select target students/groups
   - Click "Assign"

3. **View Submissions:**
   - Go to "Submissions" tab
   - Filter by assignment, student, or status
   - Review submitted work
   - Provide grades and feedback

4. **Manage Assignments:**
   - Edit existing assignments
   - Extend deadlines
   - Send reminders to students

---

### For Students

1. **Login/Register:**
   - Launch the application
   - Select "Student" role
   - Register (first time) or login with credentials

2. **View Assignments:**
   - Access dashboard to see all assigned tasks [attached_file:1]
   - Sort by deadline, subject, or status [attached_file:1]
   - Click on any assignment for detailed requirements

3. **Submit Assignment:**
   - Open the assignment
   - Click "Submit"
   - Attach files or enter text response
   - Confirm submission [attached_file:1]

4. **Track Status:**
   - View submission status (Pending, Submitted, Graded) [attached_file:1]
   - Check grades and feedback once evaluated
   - Review submission history

---

## 🔧 Build Instructions

### Building the Executable

For developers who want to create their own `.exe` file [attached_file:1]:

1. **Install PyInstaller:**

```
pip install pyinstaller
```

2. **Build the executable:**

```
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

3. **Find the output:**
   - The executable will be in the `dist/` folder
   - Copy necessary assets (icons, config files) to the same directory

### Build Options Explained

| Flag | Purpose |
|------|---------|
| `--onefile` | Package everything into a single executable [attached_file:1] |
| `--windowed` | Hide the console window (GUI only) [attached_file:1] |
| `--icon=icon.ico` | Set custom application icon [attached_file:1] |
| `--name=AMS` | Specify output executable name |

### Advanced Build Configuration

For customized builds, edit `build.spec`:

```
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets')],  # Include assets folder
    hiddenimports=['tkinter', 'fastapi'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AMS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'
)
```

Then build using:

```
pyinstaller build.spec
```

---

## 🎯 Key Features Explained

### Assignment Lifecycle

```
┌─────────────────┐
│ Faculty Creates │
│   Assignment    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Students Receive│
│   Notification  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Students View & │
│ Work on Task    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Digital Submit  │
│ Before Deadline │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Faculty Reviews │
│ & Grades Work   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Students View   │
│ Feedback/Grades │
└─────────────────┘
```

---

## 🔐 Security Features

- **Encrypted Authentication** - Secure password storage with hashing
- **Session Management** - Automatic logout after inactivity
- **Role-Based Access** - Strict permission controls
- **Local Data Protection** - No data transmitted over networks
- **Audit Logging** - Track all system activities

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Application won't start** | Ensure all asset files are in the same folder as the `.exe` [attached_file:1] |
| **Login fails** | Check database file permissions; try resetting credentials |
| **Submissions not saving** | Verify write permissions in the application directory |
| **Missing icons** | Re-download the complete package with all assets |

### System Requirements

- **OS:** Windows 7/8/10/11, macOS 10.12+, Linux (Ubuntu 18.04+)
- **RAM:** Minimum 2GB (4GB recommended)
- **Storage:** 100MB free space
- **Display:** 1024x768 minimum resolution

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**

```
git clone https://github.com/Paradva-Niraj/assigment-management-system.git
```

2. **Create a feature branch**

```
git checkout -b feature/AmazingFeature
```

3. **Commit your changes**

```
git commit -m 'Add some AmazingFeature'
```

4. **Push to the branch**

```
git push origin feature/AmazingFeature
```

5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guide for Python code
- Add docstrings to all functions and classes
- Include unit tests for new features
- Update documentation as needed

---

## 📋 Requirements

### Python Dependencies

```
tkinter>=8.6
fastapi>=0.95.0
uvicorn>=0.21.0
pydantic>=1.10.0
sqlalchemy>=2.0.0
python-multipart>=0.0.6
pyinstaller>=5.10.0
```

Install all dependencies:

```
pip install -r requirements.txt
```

---

## 🗺️ Roadmap

### Upcoming Features

- [ ] **Email Notifications** - Automated deadline reminders
- [ ] **File Versioning** - Track submission revisions
- [ ] **Plagiarism Checker** - Integrated content verification
- [ ] **Analytics Dashboard** - Visual insights for faculty
- [ ] **Mobile Companion App** - iOS/Android support
- [ ] **Cloud Sync** - Optional backup to cloud storage
- [ ] **Multi-language Support** - Internationalization
- [ ] **Dark Mode** - UI theme options

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details [attached_file:1].

```
MIT License

Copyright (c) 2025 Niraj Paradva

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Author

**Niraj Paradva**

- GitHub: [@Paradva-Niraj](https://github.com/Paradva-Niraj) [attached_file:1]
- Repository: [Assignment Management System](https://github.com/Paradva-Niraj/assigment-management-system) [attached_file:1]
- LinkedIn: [Connect with me](#)

---

## 📞 Support

Need help? Here's how to get support:

- **Issues:** Report bugs on [GitHub Issues](https://github.com/Paradva-Niraj/assigment-management-system/issues)
- **Discussions:** Join conversations in [GitHub Discussions](https://github.com/Paradva-Niraj/assigment-management-system/discussions)
- **Email:** [Contact via GitHub profile]

---

## 🌟 Acknowledgments

- Built with [Python](https://www.python.org/) [attached_file:1]
- GUI powered by [Tkinter](https://docs.python.org/3/library/tkinter.html) [attached_file:1]
- Backend framework: [FastAPI](https://fastapi.tiangolo.com/) [attached_file:1]
- Packaging: [PyInstaller](https://pyinstaller.org/) [attached_file:1]

Special thanks to all contributors and the open-source community!

---

## 📊 Project Stats

![Python](https://img.shields.io/badge/Python-100%25-blue)
![Stars](https://img.shields.io/github/stars/Paradva-Niraj/assigment-management-system?style=social)
![Forks](https://img.shields.io/github/forks/Paradva-Niraj/assigment-management-system?style=social)
![Watchers](https://img.shields.io/github/watchers/Paradva-Niraj/assigment-management-system?style=social)

---

## 📸 Screenshots

### Login Screen
```
[Login Interface Screenshot]
- Clean, modern design
- Role selection (Faculty/Student)
- Secure authentication
```

### Faculty Dashboard
```
[Faculty Dashboard Screenshot]
- Assignment creation panel
- Submission overview
- Quick statistics
```

### Student Dashboard
```
[Student Dashboard Screenshot]
- Assignment list with deadlines
- Submission status
- Grade viewer
```

---


```bash
pyinstaller --onefile --windowed --icon=icon.ico main.py
