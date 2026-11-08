import os

# 1. FIX BACKEND OFFLINE DOT
with open('frontend/js/app.js', 'r') as f: js = f.read()
# Replace the hardcoded local URL in checkConnection
js = js.replace("fetch('http://127.0.0.1:8000/health/live')", "fetch('/health/live')")
with open('frontend/js/app.js', 'w') as f: f.write(js)
print("✅ Fixed Backend Offline red dot.")

# 2. MASSIVE MOBILE UI POLISH
with open('frontend/css/style.css', 'r') as f: css = f.read()

css += """
/* =========================================
   DEDICATED MOBILE POLISH (Screens < 850px)
   ========================================= */
@media (max-width: 850px) {
    /* Topbar adjustments */
    .topbar { padding: 0 15px; height: 70px; }
    .top-right #connection-label { display: none; } /* Hide text, keep dot */
    
    /* Layout stacking */
    .grid-two { grid-template-columns: 1fr; gap: 15px; }
    .stats-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
    .stat-card { padding: 15px; }
    .stat-card strong { font-size: 24px; }
    
    /* Welcome Banner */
    .welcome { flex-direction: column; text-align: center; padding: 20px; }
    .welcome-art { font-size: 50px; margin-top: 20px; }
    
    /* Forms and Inputs */
    .form-grid { grid-template-columns: 1fr; gap: 12px; }
    .span-two { grid-column: span 1; }
    .filters { flex-direction: column; align-items: stretch; gap: 10px; }
    .filters label { width: 100%; }
    
    /* Full width buttons for easier tapping */
    .btn { width: 100%; padding: 14px; font-size: 14px; margin-bottom: 5px; }
    .inline-form { flex-direction: column; align-items: stretch; width: 100%; }
    
    /* Room Cards */
    .room-grid { grid-template-columns: 1fr; }
    .room-card { padding: 15px; }
    .room-card .btn { margin-top: 10px; }
    
    /* Tables - Horizontal Scroll */
    .table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 0 -15px; padding: 0 15px; }
    table { min-width: 600px; } /* Force scroll instead of squishing */
    th, td { white-space: nowrap; }
    
    /* Modals */
    .modal-overlay > div { width: 95% !important; padding: 15px !important; }
    
    /* Sidebar overlay */
    .sidebar { transform: translateX(-100%); box-shadow: none; }
    .sidebar.open { transform: translateX(0); box-shadow: 2px 0 20px rgba(0,0,0,0.5); }
    .sidebar.open::after { content: ''; position: fixed; top: 0; left: 245px; right: 0; bottom: 0; background: rgba(0,0,0,0.5); backdrop-filter: blur(2px); z-index: -1; }
}
"""
with open('frontend/css/style.css', 'w') as f: f.write(css)
print("✅ Added massive Mobile UI optimizations.")
