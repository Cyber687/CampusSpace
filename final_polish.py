import re

# --- 1. CLEAN UP index.html ---
with open('frontend/index.html', 'r') as f: html = f.read()

# Remove the demo text and bootstrap admin text
html = re.sub(r'<p class="muted small">Demo password for seeded accounts:.*?</p>', '', html, flags=re.DOTALL)
html = re.sub(r'<p class="muted small">Bootstrap admin:.*?</p>', '', html, flags=re.DOTALL)

# Force inject Dark Mode button into topbar (replace existing top-right div)
top_right_regex = r'<div class="top-right">.*?</div>'
new_top_right = '''<div class="top-right">
    <button id="theme-toggle" class="icon-btn" style="display:block; margin-right:15px; font-size:16px; background:transparent; border:none; cursor:pointer; color:var(--ink);" title="Toggle Dark Mode">🌙</button>
    <span class="status-dot"></span>
    <span id="connection-label">Connecting</span>
    <div class="avatar" id="top-avatar">U</div>
</div>'''
html = re.sub(top_right_regex, new_top_right, html, flags=re.DOTALL)

with open('frontend/index.html', 'w') as f: f.write(html)
print("✅ Cleaned up index.html (Removed demo credentials, forced Dark Mode button)")


# --- 2. ENSURE app.js has Dark Mode Logic ---
with open('frontend/js/app.js', 'r') as f: js = f.read()

if "themeToggle.addEventListener" not in js:
    js = js.replace(
        "bootstrap();",
        """
// Dark Mode Logic
const themeToggle = document.getElementById('theme-toggle');
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

bootstrap();
"""
    )
    with open('frontend/js/app.js', 'w') as f: f.write(js)
    print("✅ Added Dark Mode logic to app.js")
else:
    print("ℹ️ Dark Mode logic already exists in app.js")


# --- 3. ENSURE style.css has Dark Mode Variables ---
with open('frontend/css/style.css', 'r') as f: css = f.read()

if '[data-theme="dark"]' not in css:
    css += """
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
"""
    with open('frontend/css/style.css', 'w') as f: f.write(css)
    print("✅ Added Dark Mode CSS to style.css")
else:
    print("ℹ️ Dark Mode CSS already exists in style.css")

