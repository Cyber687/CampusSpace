import re

# --- 1. PATCH app.js (Fix Lag & Sidebar Click-outside) ---
with open('frontend/js/app.js', 'r') as f: js = f.read()

# Fix Lag: Only render the first 40 rooms to prevent browser freezing
js = js.replace(
    "function renderRooms(rows){if(!rows.length)",
    """function renderRooms(rows){
    if(rows.length > 40) {
        $('#room-grid').innerHTML += `<div class="empty" style="grid-column:1/-1; padding:15px; margin-bottom:15px; background:#fef3c7; color:#b45309;">Showing first 40 results. Please use the filters (Block/Floor) to narrow your search.</div>`;
        rows = rows.slice(0, 40);
    }
    if(!rows.length)"""
)

# Fix Sidebar: Close sidebar when clicking outside on mobile
js = js.replace(
    "$('#mobile-menu').addEventListener('click',()=>$('.sidebar').classList.toggle('open'));",
    """$('#mobile-menu').addEventListener('click',()=>$('.sidebar').classList.toggle('open'));
$('.main').addEventListener('click', (e) => {
    if (window.innerWidth <= 850 && $('.sidebar').classList.contains('open') && !e.target.closest('.sidebar')) {
        $('.sidebar').classList.remove('open');
    }
});"""
)

with open('frontend/js/app.js', 'w') as f: f.write(js)
print("✅ Optimized app.js (Fixed lag, added sidebar click-outside)")


# --- 2. PATCH style.css (Fix Text Overflow & Smooth Transitions) ---
with open('frontend/css/style.css', 'r') as f: css = f.read()

# Append improved CSS for sidebar and snappy UI
css += """
/* --- UI POLISH & LAG FIXES --- */
* { transition: background-color 0.2s ease, border-color 0.2s ease; }

/* Fix Sidebar Text Overflow */
.sidebar { z-index: 50; box-shadow: 2px 0 10px rgba(0,0,0,0.05); transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.nav-item { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-mini strong, .user-mini small { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 140px; }
.brand small { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 150px; }

/* Better Mobile Sidebar Overlay */
@media (max-width: 850px) {
    .sidebar.open::after {
        content: ''; position: fixed; top: 0; left: 245px; right: 0; bottom: 0;
        background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(2px); z-index: -1;
    }
    .sidebar { z-index: 100; }
    .main { transition: transform 0.3s ease; }
}

/* Make buttons snappier and more tactile */
.btn { transition: all 0.2s ease; }
.btn:active { transform: scale(0.97); }

/* Fix table horizontal scrolling on mobile without breaking layout */
.table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; border-radius: 8px; }

/* Nicer scrollbars */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
[data-theme="dark"] ::-webkit-scrollbar-thumb { background: #475569; }
"""

with open('frontend/css/style.css', 'w') as f: f.write(css)
print("✅ Polished style.css (Fixed sidebar text, added smooth transitions)")

