import os

# 1. UPDATE index.html
with open('frontend/index.html', 'r') as f: html = f.read()

# Add Help Button (?) next to the bell
html = html.replace(
    '<button id="notif-btn"',
    '<button id="help-btn" class="icon-btn" style="margin-right:10px; background:transparent; border:none; cursor:pointer; font-size:16px; color:var(--muted);" title="Help">❔</button>\n<button id="notif-btn"'
)

# Add Help Modal HTML at the very end of the body
help_modal = """
<div id="help-modal" class="modal-overlay hidden" style="position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:999; display:flex; justify-content:center; align-items:center;">
    <div class="panel" style="width:400px; max-width:90%; background:var(--panel); color:var(--ink);">
        <div class="panel-head">
            <h3>How to use CampusSpace</h3>
            <button id="close-help" class="icon-btn">×</button>
        </div>
        <ul style="line-height:1.8; font-size:13px; padding-left:20px; margin-bottom:0;">
            <li><strong>Find a Room:</strong> Use the Classroom Finder. Green means recently verified.</li>
            <li><strong>Book a Room:</strong> Click "Book 1hr" to reserve a space.</li>
            <li><strong>Report Faults:</strong> Go to Fault Reports, pick a location, and submit a ticket.</li>
            <li><strong>Canteen:</strong> Use Scan & Done to check in and see crowd levels.</li>
        </ul>
    </div>
</div>
"""
html = html.replace('</body>', help_modal + '\n</body>')

# Add My Bookings container to Dashboard
html = html.replace(
    '<div class="panel"><div class="panel-head"><div><h3>Recent fault reports</h3>',
    '''<div class="panel" id="my-bookings-panel" style="display:none;">
        <div class="panel-head"><div><h3>My Upcoming Bookings</h3><p>Rooms you have reserved</p></div></div>
        <div id="my-bookings-list" class="table-wrap"></div>
    </div>
    <div class="panel"><div class="panel-head"><div><h3>Recent fault reports</h3>'''
)

with open('frontend/index.html', 'w') as f: f.write(html)


# 2. UPDATE app.js
with open('frontend/js/app.js', 'r') as f: js = f.read()

# Add Help Modal Logic
js = js.replace(
    "bootstrap();",
    """
// Help Modal Logic
const helpBtn = document.getElementById('help-btn');
const helpModal = document.getElementById('help-modal');
const closeHelp = document.getElementById('close-help');
if (helpBtn) {
    helpBtn.addEventListener('click', () => helpModal.classList.remove('hidden'));
    closeHelp.addEventListener('click', () => helpModal.classList.add('hidden'));
    helpModal.addEventListener('click', (e) => { if(e.target === helpModal) helpModal.classList.add('hidden'); });
}

// My Bookings Logic (Mocked from local storage for the demo)
function loadMyBookings() {
    const bookings = JSON.parse(localStorage.getItem('my_bookings') || '[]');
    const panel = document.getElementById('my-bookings-panel');
    const list = document.getElementById('my-bookings-list');
    if (bookings.length > 0 && panel && list) {
        panel.style.display = 'block';
        list.innerHTML = `<table><thead><tr><th>Room</th><th>Time</th><th>Purpose</th></tr></thead><tbody>
            ${bookings.map(b => `<tr><td><strong>${b.room}</strong></td><td>${b.time}</td><td>${b.purpose}</td></tr>`).join('')}
        </tbody></table>`;
    }
}
// Call it when dashboard loads
const originalRefreshDashboard = refreshDashboard;
refreshDashboard = async function() {
    await originalRefreshDashboard();
    loadMyBookings();
};

bootstrap();
"""
)

# Save booking to local storage when successful
js = js.replace(
    "toast('Room successfully booked for 1 hour!');",
    """toast('Room successfully booked for 1 hour!');
            const bookings = JSON.parse(localStorage.getItem('my_bookings') || '[]');
            bookings.push({ room: 'Room ID ' + id, time: 'Today, 1 Hour', purpose: 'Study session' });
            localStorage.setItem('my_bookings', JSON.stringify(bookings));"""
)

with open('frontend/js/app.js', 'w') as f: f.write(js)


# 3. UPDATE style.css
with open('frontend/css/style.css', 'r') as f: css = f.read()
css += """
/* Page Fade-in Animation */
.page.active {
  animation: fadeIn 0.3s ease-in-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Modal Overlay */
.modal-overlay {
  backdrop-filter: blur(4px);
}
"""
with open('frontend/css/style.css', 'w') as f: f.write(css)

print("✅ Added My Bookings Widget, Help Modal, and Smooth Animations!")
