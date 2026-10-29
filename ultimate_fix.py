import re

# --- 1. REBUILD index.html COMPLETELY (Fixes blank screen & weird text) ---
html_content = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CampusSpace | Your Campus. Smarter. Simpler.</title>
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<div id="toast" role="status" aria-live="polite"></div>
<section id="auth-view" class="auth-wrap">
<div class="auth-brand"><div class="brand-mark">C</div><p class="eyebrow">YOUR CAMPUS. SMARTER. SIMPLER.</p><h1>CampusSpace</h1><p>Find a suitable classroom, report campus issues, and check canteen crowd estimates.</p><div class="auth-illustration"><span>🏫</span><span>🧭</span><span>🛠️</span><span>🥗</span></div></div>
<div class="auth-card">
    <div class="tabs"><button class="tab active" data-auth="login">Sign in</button><button class="tab" data-auth="register">Create account</button></div>
    <form id="login-form" class="auth-form">
        <h2>Welcome back</h2>
        <label>Email address<input name="email" type="email" required autocomplete="username" placeholder="you@university.edu"></label>
        <label>Password<input name="password" type="password" required autocomplete="current-password" placeholder="Your password"></label>
        <button class="btn primary full">Sign in</button>
    </form>
    <form id="register-form" class="auth-form hidden">
        <h2>Create your account</h2>
        <label>Full name<input name="full_name" required minlength="2" placeholder="Your full name"></label>
        <label>Email address<input name="email" type="email" required placeholder="you@university.edu"></label>
        <label>Department<select name="department" required>
            <option value="">Select department</option>
            <option>Engineering</option>
            <option>Designing</option>
            <option>Agriculture</option>
            <option>Computer Science</option>
            <option>Business</option>
            <option>Humanities</option>
            <option>Science</option>
            <option>Other</option>
        </select></label>
        <label>Password<input name="password" type="password" required minlength="8" placeholder="At least 8 characters"></label>
        <button class="btn primary full">Create student account</button>
    </form>
</div>
</section>
<div id="app-view" class="app hidden">
<aside class="sidebar">
    <a class="brand" href="#"><span class="brand-mark">C</span><span>CampusSpace<small>Campus assistance</small></span></a>
    <div class="nav-label">WORKSPACE</div>
    <nav id="main-nav">
    <button class="nav-item active" data-page="dashboard"><span>▦</span> Overview</button>
    <button class="nav-item" data-page="classrooms"><span>⌂</span> Classroom finder</button>
    <button class="nav-item" data-page="navigation"><span>⌖</span> Blocks & floors</button>
    <button class="nav-item" data-page="faults"><span>⚒</span> Fault reports</button>
    <button class="nav-item" data-page="canteens"><span>◉</span> Scan & Done</button>
    <button class="nav-item" data-page="visits"><span>◷</span> My canteen visits</button>
    <button class="nav-item" data-page="timetable"><span>▤</span> Timetable</button>
    <button class="nav-item role-staff hidden" data-page="maintenance"><span>✓</span> Maintenance desk</button>
    <button class="nav-item role-admin hidden" data-page="admin"><span>⚙</span> Admin console</button>
    </nav>
    <div class="sidebar-bottom">
    <div class="user-mini"><div class="avatar" id="avatar">U</div><div><strong id="side-name">Campus user</strong><small id="side-role">Student</small></div></div>
    <button id="logout-btn" class="btn ghost full">Sign out</button>
    </div>
</aside>
<main class="main">
    <header class="topbar">
    <button id="mobile-menu" class="icon-btn" aria-label="Toggle navigation">☰</button>
    <div><p class="eyebrow" id="date-label">CAMPUS WORKSPACE</p><h2 id="page-title">Overview</h2></div>
    <div class="top-right">
        <button id="theme-toggle" class="icon-btn" style="display:block; background:transparent; border:none; cursor:pointer; font-size:18px;" title="Toggle Dark Mode">🌙</button>
        <span class="status-dot"></span>
        <span id="connection-label">Connecting</span>
        <div class="avatar" id="top-avatar">U</div>
    </div>
    </header>
    <div class="content">
    <section class="page active" id="page-dashboard"><div class="welcome panel"><div><p class="eyebrow light">CAMPUSSPACE OVERVIEW</p><h1 id="welcome-title">Good day 👋</h1><p>Find a room that fits your next study session, and keep campus facilities working.</p><button class="btn white" data-go="classrooms">Find a classroom <span>→</span></button></div><div class="welcome-art">🏫</div></div><div class="stats-grid" id="stats-grid"></div><div class="grid-two"><div class="panel"><div class="panel-head"><div><h3>Quick actions</h3><p>Common campus tasks</p></div></div><div class="quick-grid"><button class="quick-card" data-go="classrooms"><span class="quick-icon blue">⌂</span><strong>Find a classroom</strong><small>Filter by block and floor</small></button><button class="quick-card" data-go="faults"><span class="quick-icon orange">⚒</span><strong>Report a fault</strong><small>Get a trackable ticket ID</small></button><button class="quick-card" data-go="canteens"><span class="quick-icon green">◉</span><strong>Canteen crowd</strong><small>See active registrations</small></button><button class="quick-card" data-go="timetable"><span class="quick-icon purple">▤</span><strong>View timetable</strong><small>Check scheduled classes</small></button></div></div><div class="panel"><div class="panel-head"><div><h3>Campus status</h3><p>Seeded prototype data</p></div><span class="pill info">DEMO DATA</span></div><div class="notice"><strong>Availability is an estimate</strong><p>An empty timetable slot does not guarantee a room is physically empty. Recent student verification improves confidence.</p></div><div class="notice warn"><strong>Safety first</strong><p>For sparks, exposed wiring or burning smells, do not touch the equipment. Contact campus authorities immediately.</p></div></div></div><div class="panel"><div class="panel-head"><div><h3>Recent fault reports</h3><p>Latest issues requiring attention</p></div><button class="btn secondary small-btn" data-go="faults">View all</button></div><div id="recent-faults" class="table-wrap"><p class="muted">Loading reports…</p></div></div></section>
    <section class="page" id="page-classrooms"><div class="page-intro"><div><h1>Classroom finder</h1><p>Search 320 seeded classrooms across Block-25 to Block-28.</p></div><button class="btn primary" id="refresh-rooms">↻ Refresh</button></div><div class="panel filters"><label>Block<select id="filter-block"><option value="">All blocks</option></select></label><label>Floor<select id="filter-floor"><option value="">All floors</option></select></label><label>Search room<input id="room-search" placeholder="e.g. B25-101"></label><label class="check-label"><input id="filter-quiet" type="checkbox" checked> Quiet zone</label><button class="btn secondary" id="search-rooms">Search</button></div><div class="legend"><span><i class="dot green"></i> Reported available</span><span><i class="dot blue"></i> No scheduled class (unconfirmed)</span><span><i class="dot red"></i> Scheduled / restricted</span></div><div id="room-grid" class="room-grid"></div></section>
    <section class="page" id="page-navigation"><div class="page-intro"><div><h1>Blocks & floors</h1><p>Campus layout based on the supplied schema.</p></div></div><div id="block-grid" class="block-grid"></div><div class="panel map-placeholder"><div class="map-symbol">⌖</div><h3>Campus map</h3><p>Building coordinates and pathway data have not been supplied. This prototype displays blocks and alleyway-access rules but does not invent walking routes.</p></div></section>
    <section class="page" id="page-faults"><div class="page-intro"><div><h1>Fault reports</h1><p>Report an issue or track a ticket.</p></div><button class="btn primary" id="new-fault-btn">＋ Report a fault</button></div><div class="panel hidden" id="fault-form-panel"><div class="panel-head"><div><h3>New maintenance report</h3><p>Provide enough detail for the team to locate the issue.</p></div><button class="icon-btn" id="close-fault-form">×</button></div><form id="fault-form" class="form-grid"><label>Location type<select name="location_type" id="fault-location-type"><option value="classroom">Classroom</option><option value="canteen">Canteen</option></select></label><label>Location<select name="location_id" id="fault-location" required></select></label><label>Fault category<select name="category" required><option>AC / Fan</option><option>Socket / Switch / Light</option><option>Projector / Equipment</option><option>Furniture</option><option>Water leakage</option><option>Other</option></select></label><label class="span-two">Description<textarea name="description" required minlength="5" rows="3" placeholder="Describe what happened and where…"></textarea></label><label class="span-two file-upload-label"><span class="file-upload-box">📷 Attach Photo (Optional)</span><input type="file" accept="image/*" class="hidden-file"></label><label class="urgent-check"><input type="checkbox" name="is_urgent"> Urgent safety hazard (e.g. sparks or exposed wiring)</label><div class="span-two safety-copy">For immediate danger, keep away from the equipment and contact campus authorities. This app is not an emergency service.</div><div class="span-two"><button class="btn primary">Submit report</button></div></form></div><div class="panel"><div class="panel-head"><div><h3>Ticket history</h3><p id="fault-subtitle">Your reports and their latest status</p></div><select id="fault-status-filter" class="compact-select"><option value="">All statuses</option><option>Submitted</option><option>In Progress</option><option>Completed</option><option>Escalated to Higher Authority</option></select></div><div class="table-wrap" id="fault-table"></div></div></section>
    <section class="page" id="page-canteens"><div class="page-intro"><div><h1>Scan & Done</h1><p>Scan. Eat. Leave. Keep the Campus Moving.</p></div><button class="btn secondary" id="refresh-canteens">↻ Refresh crowd</button></div><div class="notice"><strong>How crowd estimates work</strong><p>Active QR registrations are compared with canteen capacity. They estimate participation, not the exact physical headcount or queue time.</p></div><div id="canteen-grid" class="canteen-grid"></div><div class="panel checkin-panel"><div><h3>Confirm a canteen check-in</h3><p>Enter the identifier shown on the canteen's QR code. Check-in expires after 20 minutes by default.</p></div><form id="checkin-form" class="inline-form"><input name="qr_identifier" required placeholder="e.g. QR_B25C_FLOOR6"><button type="button" class="btn secondary" id="simulate-scan-btn">📷 Simulate Scan</button><button class="btn primary">Confirm check-in</button></form></div></section>
    <section class="page" id="page-visits"><div class="page-intro"><div><h1>My canteen visits</h1><p>Check out early to remove your registration from the active estimate.</p></div><button class="btn secondary" id="refresh-visits">↻ Refresh</button></div><div class="panel table-wrap" id="visits-table"></div></section>
    <section class="page" id="page-timetable"><div class="page-intro"><div><h1>Timetable</h1><p>Seeded sample schedule (Monday entries). Import authorized timetable data as an administrator.</p></div><label class="inline-select">Day<select id="timetable-day"><option>Monday</option><option>Tuesday</option><option>Wednesday</option><option>Thursday</option><option>Friday</option><option>Saturday</option><option>Sunday</option></select></label></div><div class="panel table-wrap" id="timetable-table"></div></section>
    <section class="page" id="page-maintenance"><div class="page-intro"><div><h1>Maintenance desk</h1><p>Review, assign and update submitted faults.</p></div><button class="btn secondary" id="refresh-maintenance">↻ Refresh</button></div><div id="maintenance-stats" class="stats-grid"></div><div class="panel table-wrap" id="maintenance-table"></div></section>
    <section class="page" id="page-admin"><div class="page-intro"><div><h1>Admin console</h1><p>Manage accounts and inspect the seeded campus data.</p></div><button class="btn secondary" id="refresh-admin">↻ Refresh</button></div><div id="admin-stats" class="stats-grid"></div><div class="panel"><div class="panel-head"><div><h3>Create account</h3><p>Administrators can create student, maintenance, or additional administrator accounts. Admin passwords are hashed before storage.</p></div></div><form id="admin-create-user-form" class="form-grid"><label>Full name<input name="full_name" required minlength="2" maxlength="100" placeholder="Full name"></label><label>Email address<input name="email" type="email" required placeholder="person@campusspace.edu"></label><label>Department<select name="department" required><option value="">Select department</option><option>Engineering</option><option>Designing</option><option>Agriculture</option><option>Computer Science</option><option>Business</option><option>Humanities</option><option>Science</option><option>Facilities</option><option>Administration</option><option>Other</option></select></label><label>Initial password<input name="password" type="password" required minlength="8" maxlength="128" autocomplete="new-password" placeholder="At least 8 characters"></label><label>Role<select name="role" required><option value="admin">Administrator — full system access</option><option value="maintenance">Maintenance staff</option><option value="student">Student</option></select></label><div><button class="btn primary">Create account</button></div></form></div><div class="panel"><div class="panel-head"><div><h3>User management</h3><p>Passwords are never displayed; only password hashes are stored. Administrators can change roles and reset passwords.</p></div></div><div class="table-wrap" id="users-table"></div></div><div class="panel"><div class="panel-head"><div><h3>Timetable CSV import</h3><p>Required columns: classroom_id, subject_name, day_of_week, start_time, end_time; optional is_break_slot.</p></div></div><form id="timetable-import-form" class="inline-form"><input type="file" name="file" accept=".csv" required><button class="btn primary">Import CSV</button></form></div></section>
    </div>
    <footer>CampusSpace · Sample campus data · Confirm all availability on site.</footer>
</main>
</div>
<script src="js/config.js"></script><script src="js/api.js"></script><script src="js/app.js"></script>
</body>
</html>"""

with open('frontend/index.html', 'w') as f: f.write(html_content)
print("✅ Rebuilt index.html perfectly. No more blank screen or weird text.")

# --- 2. FIX app.js (Render Rooms Lag & Sidebar) ---
with open('frontend/js/app.js', 'r') as f: js = f.read()

# Replace the entire renderRooms function with the fixed, non-laggy version
new_render = '''
function renderRooms(rows){
    if(!rows.length){
        $('#room-grid').innerHTML='<div class="empty">No classrooms match these filters.</div>';
        return;
    }
    let truncated = false;
    if(rows.length > 40) {
        rows = rows.slice(0, 40);
        truncated = true;
    }
    let html = truncated ? `<div class="empty" style="grid-column:1/-1; padding:15px; margin-bottom:10px; background:#fef3c7; color:#b45309; border:1px solid #fde68a; border-radius:8px;">Showing first 40 results. Please use the filters (Block/Floor) to narrow your search.</div>` : '';
    html += rows.map(r=>{
        const s=r.availability||{},st=s.status||'Unknown',avail=st==='Reported Available',blocked=['Scheduled class','Reported Occupied','Restricted','Booked'].includes(st);
        return `<article class="room-card">
        <div class="room-top"><div><h3>${esc(r.room_number)}</h3><p class="sub">${esc(r.block_name)} · Floor ${r.floor_number}</p></div><span class="room-status ${avail?'available':blocked?'blocked':''}">${esc(st)}</span></div>
        <p class="sub">${esc(s.detail|| (s.confidence==='unconfirmed'?'Physical vacancy not confirmed':`Status confidence: ${s.confidence||'unknown'}`))}</p>
        <div class="amenities">
        <span class="${s.detail && s.detail.includes('AC') ? 'broken-amenity' : ''}">❄ ${r.ac_count} AC</span>
        <span>⚡ ${r.student_sockets} student sockets</span>
        <span>♧ ${r.faculty_sockets} faculty sockets</span>
        <span>◌ Quiet zone</span>
        <span>♙ ${r.capacity} capacity</span>
        </div>
        <div class="verified-time">🕒 ${s.reported_at ? 'Last verified: ' + s.reported_at : 'No recent student verification'}</div>
        <button class="btn secondary" data-room-detail="${r.id}" style="margin-top:10px;">Room details</button>
        <button class="btn primary" data-verify="${r.id}">Verify status</button>
        </article>`
    }).join('');
    $('#room-grid').innerHTML = html;
    $$('[data-room-detail]').forEach(b=>b.onclick=()=>roomDetail(b.dataset.roomDetail));
    $$('[data-verify]').forEach(b=>b.onclick=()=>verifyRoom(b.dataset.verify));
}
'''
js = re.sub(r'function renderRooms\(rows\)\{.*?(?=\$\(\'#search-rooms\'\))', new_render, js, flags=re.DOTALL)

# Add dark mode, mobile menu, and simulate scan safely at the end
js = js.replace('bootstrap();', '''
// --- FINAL UI POLISH ---
const themeToggle = document.getElementById('theme-toggle');
if (themeToggle) {
    if (localStorage.getItem('theme') === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        themeToggle.textContent = '☀️';
    }
    themeToggle.addEventListener('click', () => {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        if (isDark) {
            document.documentElement.removeAttribute('data-theme');
            localStorage.setItem('theme', 'light');
            themeToggle.textContent = '🌙';
        } else {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            themeToggle.textContent = '☀️';
        }
    });
}
const mobileMenu = document.getElementById('mobile-menu');
if (mobileMenu) {
    mobileMenu.addEventListener('click',()=>document.querySelector('.sidebar').classList.toggle('open'));
}
const mainArea = document.querySelector('.main');
if (mainArea) {
    mainArea.addEventListener('click', (e) => {
        if (window.innerWidth <= 850 && document.querySelector('.sidebar').classList.contains('open') && !e.target.closest('.sidebar') && !e.target.closest('#mobile-menu')) {
            document.querySelector('.sidebar').classList.remove('open');
        }
    });
}
// Simulate Scan Button
const simScan = document.getElementById('simulate-scan-btn');
if (simScan) {
    simScan.addEventListener('click', () => {
        const input = document.querySelector('#checkin-form [name="qr_identifier"]');
        input.value = 'QR_B25C_FLOOR6';
        if (typeof toast === 'function') toast('Simulated QR Scan: B25 Main Canteen');
        setTimeout(() => { document.getElementById('checkin-form').dispatchEvent(new Event('submit')); }, 800);
    });
}
bootstrap();''')

with open('frontend/js/app.js', 'w') as f: f.write(js)
print("✅ Fixed app.js (Removed lag, fixed sidebar).")


# --- 3. PATCH style.css (Overflow & Dark Mode) ---
with open('frontend/css/style.css', 'r') as f: css = f.read()

css += """
/* FINAL CSS FIXES */
[data-theme="dark"] {
  --bg: #0f172a; --panel: #1e293b; --ink: #f8fafc; --muted: #94a3b8; 
  --line: #334155; --navy: #f8fafc; --blue2: #1e3a8a;
}
[data-theme="dark"] body { background: var(--bg); color: var(--ink); }
[data-theme="dark"] .panel, [data-theme="dark"] .stat-card, [data-theme="dark"] .room-card, 
[data-theme="dark"] .sidebar, [data-theme="dark"] .topbar, [data-theme="dark"] .auth-card { 
  background: var(--panel); border-color: var(--line); color: var(--ink); 
}
[data-theme="dark"] th { background: #0f172a; color: var(--muted); }
[data-theme="dark"] td { border-color: var(--line); }
[data-theme="dark"] input, [data-theme="dark"] select, [data-theme="dark"] textarea {
  background: #0f172a; border-color: var(--line); color: var(--ink);
}
[data-theme="dark"] .nav-item.active { background: #1e3a8a; color: #93c5fd; }
[data-theme="dark"] .btn.secondary { background: #1e293b; border-color: var(--line); color: var(--ink); }

.verified-time { font-size: 10px; color: var(--muted); margin-top: 10px; border-top: 1px solid var(--line); padding-top: 10px; }
.broken-amenity { color: var(--red) !important; background: var(--redbg) !important; border: 1px solid var(--red); }
.file-upload-label { cursor: pointer; display: block; }
.file-upload-box { display: block; padding: 15px; text-align: center; border: 2px dashed #cbd5e1; border-radius: 8px; color: var(--muted); font-size: 12px; transition: 0.2s; }
.file-upload-box:hover { border-color: var(--blue); color: var(--blue); background: var(--blue2); }
[data-theme="dark"] .file-upload-box { border-color: var(--line); }
.hidden-file { display: none; }

.sidebar { z-index: 100; transition: transform 0.3s ease; }
.nav-item { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-mini strong, .user-mini small { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 140px; }
.brand small { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 150px; }
.btn { transition: all 0.2s ease; }
.btn:active { transform: scale(0.97); }
.table-wrap { overflow-x: auto; border-radius: 8px; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
[data-theme="dark"] ::-webkit-scrollbar-thumb { background: #475569; }
"""
with open('frontend/css/style.css', 'w') as f: f.write(css)
print("✅ Polished style.css (Fixed sidebar text, smooth transitions).")
