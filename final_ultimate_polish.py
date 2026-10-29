import re

# 1. UPDATE index.html (Add Favicon)
with open('frontend/index.html', 'r') as f: html = f.read()

# Inject an SVG Favicon (No external image needed!)
favicon = '''<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='25' fill='%232864e8'/%3E%3Ctext x='50' y='70' font-size='60' text-anchor='middle' fill='white' font-family='sans-serif' font-weight='bold'%3EC%3C/text%3E%3C/svg%3E">'''
html = html.replace('<link rel="stylesheet" href="css/style.css">', favicon + '\n<link rel="stylesheet" href="css/style.css">')
with open('frontend/index.html', 'w') as f: f.write(html)


# 2. UPDATE app.js (Pulsing Dots & Empty States)
with open('frontend/js/app.js', 'r') as f: js = f.read()

# Add Pulsing Dot to Room Status Badges
js = js.replace(
    '<span class="room-status ${avail?\'available\':blocked?\'blocked\':\'\'}">${esc(st)}</span>',
    '<span class="room-status ${avail?\'available\':blocked?\'blocked\':\'\'}"><span class="pulse-dot ${avail?\'green\':blocked?\'red\':\'blue\'}"></span>${esc(st)}</span>'
)

# Enhance Empty States for Faults, Visits, and Maintenance
js = js.replace(
    "'<div class=\"empty\">No reports to show.</div>'",
    "'<div class=\"empty\" style=\"text-align:center; padding:30px;\"><div style=\"font-size:40px; margin-bottom:10px;\">🛠️</div><h3>No fault reports found</h3><p>Submit a new report to get started.</p></div>'"
)
js = js.replace(
    "'<div class=\"empty\">You have no canteen visits yet.</div>'",
    "'<div class=\"empty\" style=\"text-align:center; padding:30px;\"><div style=\"font-size:40px; margin-bottom:10px;\">🥗</div><h3>No active visits</h3><p>Scan a canteen QR code to check in.</p></div>'"
)
js = js.replace(
    "'<div class=\"empty\">No reports.</div>'",
    "'<div class=\"empty\" style=\"text-align:center; padding:30px;\"><div style=\"font-size:40px; margin-bottom:10px;\">✅</div><h3>All caught up!</h3><p>No pending maintenance tickets.</p></div>'"
)

with open('frontend/js/app.js', 'w') as f: f.write(js)


# 3. UPDATE style.css (Animations for Pulsing Dots)
with open('frontend/css/style.css', 'r') as f: css = f.read()

css += """
/* --- PREMIUM PULSING DOTS --- */
.pulse-dot {
  display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px;
}
.pulse-dot.green { background-color: #10b981; box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); animation: pulse-green 2s infinite; }
.pulse-dot.red { background-color: #ef4444; box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); animation: pulse-red 2s infinite; }
.pulse-dot.blue { background-color: #3b82f6; box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); animation: pulse-blue 2s infinite; }

@keyframes pulse-green {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}
@keyframes pulse-red {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}
@keyframes pulse-blue {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(59, 130, 246, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
}
"""
with open('frontend/css/style.css', 'w') as f: f.write(css)

print("✅ Added Favicon, Pulsing Status Dots, and Beautiful Empty States!")
