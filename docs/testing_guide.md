# Manual testing checklist

- [ ] Register a new student and sign in.
- [ ] Confirm a new student cannot open admin endpoints.
- [ ] Search classrooms by block/floor and verify room amenities.
- [ ] Verify a classroom as available/occupied/restricted and observe freshness.
- [ ] Try to book during a scheduled class; request should be rejected.
- [ ] Submit a fault report; check the returned ticket ID and duplicate warning.
- [ ] Sign in as maintenance and move a ticket to In Progress then Completed.
- [ ] Confirm a student cannot update official ticket status or view another student's ticket detail.
- [ ] Check into a canteen twice; second request should return the active visit instead of creating a duplicate.
- [ ] Check out early and confirm active registrations decrease.
- [ ] Admin changes a user's role and can import a timetable CSV.
- [ ] Confirm the UI labels timetable-only vacancy as unconfirmed.
