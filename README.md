# 🏫 CampusSpace
### Smart Campus Assistance & Resource Management Platform
**Tagline:** *Your Campus. Smarter. Simpler.*

**Developed by:**
- Karan Kr.
- Aniket Nanda
- Shreyansh D. Prajapati

---

## 📖 Executive Summary
CampusSpace is a full-stack web application designed to reduce everyday friction for university students, faculty, and maintenance staff. It brings together classroom discovery, infrastructure fault reporting, and canteen crowd estimation into one responsive, easy-to-use platform. 

The system is built as an **API-first microservice**, meaning it can be easily integrated into an existing University Management System (UMS) in the future.

## ✨ Key Features
- **Smart Classroom Finder:** Live timetable checks combined with time-stamped student verifications (with expiry rules). Includes a "Book 1hr" feature for empty rooms.
- **Infrastructure Fault Reporting:** 10-second reporting system for broken ACs, sockets, or projectors with trackable Ticket IDs and a 7-day auto-escalation rule.
- **Scan & Done (Canteen):** QR-based check-in system with a 20-minute auto-expiry to estimate live canteen crowd levels.
- **Admin & Maintenance Dashboards:** Role-based access control, user management, QR code generation, and ticket resolution tracking.
- **Premium UI/UX:** Includes Dark Mode, mobile-responsive layout, skeleton loading states, and keyboard shortcuts.

## 🛠️ Tech Stack
- **Frontend:** HTML5, Vanilla CSS3, Vanilla JavaScript (No heavy frameworks, fully responsive).
- **Backend:** Python 3, FastAPI.
- **Database:** SQLite (PostgreSQL-ready for production).
- **Security:** PBKDF2 password hashing, JWT (JSON Web Tokens) for authentication.

---

## 🚀 Quick Start (1-Click Setup)

We have provided automated setup scripts for both Windows and Linux/macOS to make installation seamless.

### For Windows Users:
1. Open the project folder and double-click **`setup.bat`** (This creates the virtual environment, installs dependencies, and seeds the database).
2. Double-click **`run.bat`** to start the server.
3. Open your browser and go to: `http://127.0.0.1:8000/static/index.html`

### For Linux / macOS Users:
1. Open the terminal in the project folder and run: `chmod +x setup.sh && ./setup.sh`
2. Run: `./run.sh` to start the server.
3. Open your browser and go to: `http://127.0.0.1:8000/static/index.html`

---

## 🔐 Demo Accounts for Evaluation
Use the following credentials to test the different role-based permissions. 
*All demo accounts use the password: `CampusDemo123!`*

| Role | Email | Access Level |
| :--- | :--- | :--- |
| **Student** | `rohan@student.campusspace.edu` | Book rooms, report faults, scan QR codes. |
| **Maintenance** | `rajesh.maint@campusspace.edu` | View and update fault ticket statuses. |
| **Admin** | `karan@campusspace.edu` | Full access: Manage users, view QR codes, import timetables. |

*(Note: There is also a hidden Bootstrap Admin account: `anonymous1@campusspace.edu.in` with password `campusspace1234`)*

---

## 🔗 College App Integration Strategy
CampusSpace is intentionally designed not as a silo, but as a modular service that the university can adopt:
1. **Swagger API Docs:** FastAPI automatically generates interactive API documentation at `/docs`. The university IT team can use this to connect their existing mobile app to our backend.
2. **SSO Ready:** The current JWT authentication can be swapped for University Single Sign-On (SSO) tokens.
3. **Webhooks:** Maintenance tickets can be configured to push webhooks directly into the university's ERP system.

## 📂 Project Structure
```text
CampusSpace/
├── backend/            # FastAPI backend logic and database connection
├── data/               # SQLite database and seed schema
├── frontend/           # HTML, CSS, JS interface
│   ├── css/
│   ├── js/
│   └── index.html
├── scripts/            # Database initialization and QR generation scripts
├── setup.sh / .bat     # 1-click installer
├── run.sh / .bat       # 1-click server starter
└── requirements.txt    # Python dependencies
