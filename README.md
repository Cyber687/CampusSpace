# CampusSpace — complete local MVP

**Your Campus. Smarter. Simpler.** Responsive campus assistance prototype built from the updated project documents and the supplied SQLite seed schema.

## Included capabilities

- Sign in, student registration, department field, PBKDF2 password hashing, signed expiring bearer tokens, role-based permissions.
- One shared responsive interface with student, maintenance, and admin navigation.
- Blocks/floors/classrooms loaded from the SQL seed database (4 blocks, 8 floors per block, 10 rooms per floor; 320 rooms total).
- Classroom search by block/floor/room, room details, amenities, timetable conflict status, and time-stamped student verification with expiry.
- Classroom booking with basic timetable/booking overlap validation.
- Fault reports with unique ticket IDs, duplicate warning, urgent flag, status history, student-owned ticket privacy, staff-only updates, and 7-day escalation on request processing.
- Canteen crowd estimate from active QR registrations, configurable per-canteen duration, duplicate active check-in prevention, early checkout, and expiry checks.
- Maintenance desk, admin user role/account/password management, admin overview, and timetable CSV import.
- API documentation at `/docs`, database initialization script, starter test, and setup notes.

## Requirements

Python 3.11+ recommended. Windows PowerShell commands are shown below. Python 3.13 should also work with compatible current dependencies.

## Setup (Windows PowerShell)

```powershell
cd "E:\Sem3_Work\Design Thinking Project\Project_Prototype"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Before using outside a local demo, edit `.env` and replace `JWT_SECRET_KEY` with a long random secret. The default is only for local development.

Initialize the database once:

```powershell
python scripts\init_db.py
```

To discard local changes and rebuild from the supplied seed schema, use the destructive reset command only when you intend to delete the current database:

```powershell
python scripts\init_db.py --reset
```

Start the application:

```powershell
python run.py
```

Open **http://127.0.0.1:8000/static/index.html** for the web app, or **http://127.0.0.1:8000/docs** for the API documentation.

Alternative frontend server (if you prefer separate frontend/backend terminals):

```powershell
python -m http.server 5500 --directory frontend
```

Then open `http://127.0.0.1:5500`. The API CORS settings already allow this local origin.

## Demo accounts

Seeded accounts from the SQL file use this demo password: `CampusDemo123!`

| Role | Email |
|---|---|
| Admin | `karan@campusspace.edu` |
| Admin | `aniket@campusspace.edu` |
| Admin | `shreyansh@campusspace.edu` |
| Maintenance | `rajesh.maint@campusspace.edu` |
| Maintenance | `suresh.maint@campusspace.edu` |
| Maintenance | `amit.maint@campusspace.edu` |
| Student | `rohan@student.campusspace.edu` |
| Student | `priya@student.campusspace.edu` |

Change demo passwords before showing this outside a controlled prototype. Newly registered users receive the student role; admins can promote users to maintenance/admin.

## Database notes

- `data/schema/Campus_Space_Dummy_Data.sql` is the provided schema and seed dataset. `scripts/init_db.py` loads it without using SQLAlchemy ORM metadata creation.
- The initializer adds `user_credentials`, `maintenance_updates`, `classroom_bookings`, and `admin_audit_log` supporting tables. Passwords are stored as PBKDF2 hashes; the app never returns password hashes to the browser.
- Seeded timetable data is illustrative and mostly Monday-only. Import an authorized CSV for real scheduling.
- The initial schema has no department column on `users`, so department and account-active status are kept in `user_credentials`.

## Timetable CSV format

Required headers: `classroom_id,subject_name,day_of_week,start_time,end_time`. Optional header: `is_break_slot` (`0` or `1`). Times should use `HH:MM:SS` or compatible time strings. Import from the admin console or POST a multipart CSV to `/api/v1/admin/timetable/import`.

## Important behaviour and limitations

- **Availability is not a guarantee of physical vacancy.** The API first checks current-day timetable entries, then recent verification reports; rooms without a current class and without fresh verification are labelled `No scheduled class` with `unconfirmed` confidence.
- Verification reports expire from status consideration after the configured `VERIFICATION_TTL_MINUTES` (default 60). Conflicting reports are not yet combined into a sophisticated confidence score; the latest fresh report is used.
- Walking routes are not fabricated. Building coordinates and pathway data were not provided, so the map section explains that routes are not configured.
- Canteen active registrations are estimates, not a physical headcount or reliable waiting-time prediction. Server-side expiry checks exclude expired visits even before a background cleanup task exists.
- A scheduled request on any API call applies the 7-day escalation rule to overdue unresolved reports; no background scheduler is required for the prototype.
- The fault photo upload workflow is not yet enabled in this MVP; reports are text-based. Do not upload sensitive or identifying information.
- Classroom booking is a prototype reservation workflow, not an official university room-access authorization.
- The current seed data contains a single Monday sample timetable. Don't interpret absent entries for other days as verified availability.

## API routes

- `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me`
- `GET /api/v1/blocks`
- `GET /api/v1/classrooms`, `GET /api/v1/classrooms/available`, `GET /api/v1/classrooms/{id}`
- `POST /api/v1/classrooms/{id}/verifications`, `POST /api/v1/classrooms/{id}/bookings`
- `GET /api/v1/timetable`, `POST /api/v1/admin/timetable/import`
- `GET /api/v1/fault-reports`, `POST /api/v1/fault-reports`, `GET /api/v1/fault-reports/{id}`, `PATCH /api/v1/fault-reports/{id}`
- `GET /api/v1/canteens`, `POST /api/v1/canteens/check-in`, `GET /api/v1/canteen-visits/mine`, `POST /api/v1/canteen-visits/{id}/checkout`
- `GET /api/v1/maintenance/summary`
- `GET /api/v1/admin/overview`, `GET /api/v1/admin/users`, `PATCH/DELETE /api/v1/admin/users/{id}`
- `GET /health/live`

## Tests

```powershell
pytest -q
```

## Security scope

This is an educational local MVP, not a production-ready university deployment. Before production, use HTTPS, rotate secrets, implement rate limits and email verification/password reset, add protected file storage, audit/review retention policies, configure backups/monitoring, and validate access rules with the university. Do not expose the demo credentials publicly.


## Bootstrap administrator
The bundled database and database initialization script include a bootstrap administrator account:
- Email: `anonymous1@campusspace.edu.in`
- Initial password: `campusspace1234`

The password is stored as a salted PBKDF2 hash, not as plaintext. Sign in and change this initial password before sharing the project. Any authenticated administrator can create additional admin accounts from **Admin console → Create account**, select the Administrator role, and manage users. The API restricts account creation and role changes to admins.
