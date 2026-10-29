# CampusSpace MVP blueprint

## Roles
- Student: search rooms, submit verifications, make prototype bookings, report/track own faults, scan/check out canteen visits.
- Maintenance: see campus faults, update status and notes, see urgent/overdue work.
- Admin: maintenance permissions plus user role/account management, timetable CSV import, overview metrics.

## Data rules
- Blocks B25–B28; eight floors each; ten classrooms per floor; 320 classrooms total.
- Each room: 60 capacity, 60 student sockets, 2 faculty sockets, 2 AC units, quiet-zone flag.
- Alleyway access is seeded for floors 1–5; not floors 6–8.
- One canteen per block on floor 6; capacity varies from 100–200; 20-minute default visit.
- Classroom status combines schedule with a recent verification; no schedule does not imply physical vacancy.
- Faults unresolved for seven days are escalated on the next API request.

## Data honesty
Campus coordinates, walkable paths, real-time occupancy sensors, live university timetable integration, calibrated queue times, and photo upload are not supplied/enabled. UI/API should not claim those capabilities exist.
