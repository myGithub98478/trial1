# Automated Attendance & Student Management System

A full-featured Django web application for automated attendance using MAC address detection, student management, notes sharing, and assignment workflow for teachers and students.

---

## ⚠️ Changing Your Router? Read This!

If you change your WiFi router (or connect to a new router/network), you may need to update the following in your project:

- **Router IP Address:**
  - The MAC detection and ARP scan logic assumes your router's gateway IP (e.g., `192.168.101.1`).
  - If your new router uses a different gateway (e.g., `192.168.0.1` or `192.168.1.1`), update the default IP in your code.
  - **Where to change:**
    - In `router_devices.py` (if you use it standalone):
      ```python
      # Change this line if your router IP changes
      def __init__(self, router_ip="192.168.101.1", ...):
      ```
    - In Django integration (if you use ARP scan in views):
      - The ARP scan uses your system's ARP table, so as long as your computer is connected to the new router and can see the devices, it will work automatically.
      - If you hardcoded the router IP anywhere, update it to match your new router's gateway IP.

- **MAC Address Registration:**
  - No change needed! As long as students' devices connect to the new router, their MAC addresses will still be detected and matched.

- **DHCP/Network Settings:**
  - Make sure your new router is not isolating clients (some routers have "AP isolation" or "client isolation" which prevents devices from seeing each other on the network). This will break MAC detection.

- **Troubleshooting:**
  - If attendance scanning stops working after changing routers, check:
    - Your computer is connected to the new router.
    - The ARP table (`arp -a` in command prompt) shows all connected devices.
    - The router is not blocking device-to-device communication.

**Tip:**
- You do NOT need to change any student MAC addresses in the database when changing routers.
- If you use a different network segment (e.g., `10.0.0.x`), just make sure your computer is on the same network and can see all devices.

---

## 🚀 Features

- **Automated Attendance:**
  - Detects devices on the local network and marks student attendance based on registered MAC addresses.
  - Logs device connections and attendance records.
- **Student Management:**
  - Add, edit, and view student profiles.
  - View attendance logs and device logs per student.
- **Role-Based Access:**
  - **Admin:** Full access to all features, user and data management.
  - **Teacher:** Post assignments, upload notes, grade submissions, view attendance.
  - **Student:** View assignments, submit work, download/upload notes, view attendance.
- **Notes Sharing:**
  - Students and teachers can upload and download notes (PDF, DOCX, etc.).
- **Assignment Workflow:**
  - Teachers post assignments with deadlines and files.
  - Students submit assignments online.
  - Teachers grade and provide feedback on submissions.
- **Dashboard & Analytics:**
  - Visual graphs for attendance trends.
  - Quick stats for students, attendance, and device logs.
- **Search & Filtering:**
  - Search assignments by title.
- **Modern UI:**
  - Responsive, Bootstrap 5-based interface.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.13, Django 5.x
- **Frontend:** Django Templates, Bootstrap 5, Chart.js
- **Database:** SQLite (default, can be swapped for PostgreSQL/MySQL)
- **Other:**
  - django-crispy-forms, crispy-bootstrap5 (for beautiful forms)
  - BeautifulSoup, requests (for MAC detection)

---

## 📂 Project Structure

```
attendance_system/         # Django project root
├── attendance/            # Main app (models, views, templates)
│   ├── models.py          # All models (Student, Attendance, DeviceLog, Note, Assignment, Submission, UserProfile)
│   ├── views.py           # All views (dashboard, attendance, notes, assignments, etc.)
│   ├── forms.py           # All forms (StudentForm, NoteForm, AssignmentForm, etc.)
│   ├── templates/         # All HTML templates
│   └── ...
├── db.sqlite3             # SQLite database
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd <project-folder>
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
7. **Access the app:**
   - Main site: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 📝 Usage Guide

- **Login:** Use your superuser or assigned credentials.
- **Dashboard:** View stats, attendance trends, and recent device logs.
- **Students:** Add/view students, see their attendance and device logs.
- **Attendance:** Scan devices to mark attendance automatically.
- **Notes:** Upload/download notes. Teachers and students can share files.
- **Assignments:**
  - Teachers: Post assignments, view and grade submissions.
  - Students: View assignments, submit work, see marks and feedback.
- **Device Log:** View all detected devices and their status (known/unknown).

---

## 🔒 Security & Roles
- Only authenticated users can access the system.
- Role-based access (admin, teacher, student) enforced throughout.
- File uploads are restricted to allowed types and stored securely.

---

## 📈 Extending the System
- Add more analytics (attendance per class, student performance, etc.)
- Integrate with external APIs or mobile apps (Django REST Framework recommended)
- Add email notifications (configure SMTP in Django settings)
- Switch to PostgreSQL/MySQL for production

---

## 🤝 Contributing
Pull requests and suggestions are welcome! Please open an issue or submit a PR.

---

## 📄 License
This project is for educational/demo purposes. Please adapt for production use as needed. 