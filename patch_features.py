import os

# --- 1. PATCH app.js (Corrected Path) ---
js_path = 'frontend/js/app.js'
if os.path.exists(js_path):
    with open(js_path, 'r') as f: js = f.read()

    # Add Dark Mode Logic
    js = js.replace(
        "bootstrap();",
        """
// Dark Mode Logic
const themeToggle = $('#theme-toggle');
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

// Simulate Scan Button Logic
$('#simulate-scan-btn').onclick = () => {
    const input = $('#checkin-form [name="qr_identifier"]');
    input.value = 'QR_B25C_FLOOR6';
    toast('Simulated QR Scan: B25 Main Canteen');
    setTimeout(() => { $('#checkin-form').dispatchEvent(new Event('submit')); }, 800);
};

bootstrap();
"""
    )

    # Add Last Verified Timestamp & Color Coding to Rooms
    old_amenities = '<div class="amenities"><span>❄ ${r.ac_count} AC</span><span>⚡ ${r.student_sockets} student sockets</span><span>♧ ${r.faculty_sockets} faculty sockets</span><span>◌ Quiet zone</span><span>♙ ${r.capacity} capacity</span></div>'
    new_amenities = '''<div class="amenities">
<span class="${s.detail && s.detail.includes('AC') ? 'broken-amenity' : ''}">❄ ${r.ac_count} AC</span>
<span>⚡ ${r.student_sockets} student sockets</span>
<span>♧ ${r.faculty_sockets} faculty sockets</span>
<span>◌ Quiet zone</span>
<span>♙ ${r.capacity} capacity</span></div>
<div class="verified-time">🕒 ${s.reported_at ? 'Last verified: ' + s.reported_at : 'No recent student verification'}</div>'''

    js = js.replace(old_amenities, new_amenities)
    with open(js_path, 'w') as f: f.write(js)
    print("✅ Successfully patched frontend/js/app.js")
else:
    print(f"❌ Could not find {js_path}")

# --- 2. PATCH style.css (Corrected Path) ---
css_path = 'frontend/css/style.css'
if os.path.exists(css_path):
    with open(css_path, 'r') as f: css = f.read()

    css += """
/* --- NEW IMPROVEMENTS & DARK MODE --- */
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

@media(max-width: 560px) {
  .inline-form { flex-direction: column; align-items: stretch; }
  .inline-form button { width: 100%; margin-top: 8px; }
  .file-upload-box { padding: 10px; }
  .top-right { gap: 5px; }
}
"""
    with open(css_path, 'w') as f: f.write(css)
    print("✅ Successfully patched frontend/css/style.css")
else:
    print(f"❌ Could not find {css_path}")

