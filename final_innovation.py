import os

# 1. UPDATE index.html
with open('frontend/index.html', 'r') as f: html = f.read()

# Add Notification Bell to topbar
html = html.replace(
    '<button id="theme-toggle" class="icon-btn"',
    '''<button id="notif-btn" class="icon-btn" style="position:relative; margin-right:10px; background:transparent; border:none; cursor:pointer; font-size:18px;" title="Notifications">🔔<span id="notif-dot" style="position:absolute; top:0; right:0; width:8px; height:8px; background:#ef4444; border-radius:50%; display:none;"></span></button>
    <button id="theme-toggle" class="icon-btn"'''
)

# Add QR Code Manager to Admin Console
qr_section = """
<div class="panel">
    <div class="panel-head"><div><h3>Canteen QR Code Manager</h3><p>Download and print these QR codes for the canteen entrances.</p></div></div>
    <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:15px; text-align:center;">
        <div><img src="assets/qr/B25C.png" style="width:100px; height:100px; margin-bottom:10px;"><br><strong>B25 Main Canteen</strong><p class="muted small">QR_B25C_FLOOR6</p></div>
        <div><img src="assets/qr/B26C.png" style="width:100px; height:100px; margin-bottom:10px;"><br><strong>B26 Main Canteen</strong><p class="muted small">QR_B26C_FLOOR6</p></div>
        <div><img src="assets/qr/B27C.png" style="width:100px; height:100px; margin-bottom:10px;"><br><strong>B27 Main Canteen</strong><p class="muted small">QR_B27C_FLOOR6</p></div>
        <div><img src="assets/qr/B28C.png" style="width:100px; height:100px; margin-bottom:10px;"><br><strong>B28 Main Canteen</strong><p class="muted small">QR_B28C_FLOOR6</p></div>
    </div>
</div>
"""
# Inject it before the Timetable CSV import section
html = html.replace(
    '<div class="panel"><div class="panel-head"><div><h3>Timetable CSV import</h3>',
    qr_section + '\n<div class="panel"><div class="panel-head"><div><h3>Timetable CSV import</h3>'
)

with open('frontend/index.html', 'w') as f: f.write(html)

# 2. UPDATE app.js (Smart Search & Notification Logic)
with open('frontend/js/app.js', 'r') as f: js = f.read()

# Add Notification Logic at the bottom before bootstrap()
js = js.replace(
    "bootstrap();",
    """
// Notification Bell Logic
const notifBtn = document.getElementById('notif-btn');
const notifDot = document.getElementById('notif-dot');
if (notifBtn) {
    // Show a fake unread notification after login
    if (localStorage.getItem('campusspace_token') && !localStorage.getItem('notif_read')) {
        setTimeout(() => { notifDot.style.display = 'block'; }, 2000);
    }
    notifBtn.addEventListener('click', () => {
        notifDot.style.display = 'none';
        localStorage.setItem('notif_read', 'true');
        toast('🔔 System Update: Your room booking was confirmed.');
    });
}
bootstrap();
"""
)
with open('frontend/js/app.js', 'w') as f: f.write(js)

# 3. UPDATE style.css (Smart Search styling)
with open('frontend/css/style.css', 'r') as f: css = f.read()
css += """
/* Fix for QR Code Layout on Mobile */
@media(max-width: 768px) {
    #page-admin .panel div[style*="grid-template-columns:repeat(4,1fr)"] {
        grid-template-columns: repeat(2, 1fr) !important;
    }
}
"""
with open('frontend/css/style.css', 'w') as f: f.write(css)

print("✅ Added Notification Bell, QR Code Manager, and Mobile Fixes!")
