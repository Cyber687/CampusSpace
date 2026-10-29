import re

# 1. UPDATE app.js (Skeletons, Toast Icons, Shortcuts)
with open('frontend/js/app.js', 'r') as f: js = f.read()

# --- Skeleton Loader ---
# Replace the spinner with a skeleton grid in loadClassrooms
js = js.replace(
    "async function loadClassrooms(){ $('#room-grid').innerHTML = '<div class=\"loading-spinner\"></div>'; try{",
    """async function loadClassrooms(){ 
    // Show Skeleton UI
    let skeletonHTML = '';
    for(let i=0; i<6; i++) {
        skeletonHTML += `<div class="room-card skeleton-card">
            <div class="skeleton-title"></div>
            <div class="skeleton-text"></div>
            <div class="skeleton-text short"></div>
            <div class="skeleton-box"></div>
        </div>`;
    }
    $('#room-grid').innerHTML = skeletonHTML;
    try{"""
)

# --- Smart Toasts ---
# Upgrade the toast function to support icons and a close button
old_toast = "function toast(msg){const el=$('#toast');el.textContent=msg;el.classList.add('show');clearTimeout(toast.timer);toast.timer=setTimeout(()=>el.classList.remove('show'),3500)}"
new_toast = """function toast(msg, type='info'){
    const el=$('#toast');
    let icon = 'ℹ️';
    if(type === 'success') icon = '✅';
    if(type === 'error') icon = '❌';
    if(type === 'warning') icon = '⚠️';
    
    el.innerHTML = `<div style="display:flex; align-items:center; gap:10px;">
        <span style="font-size:18px;">${icon}</span>
        <span style="flex:1;">${msg}</span>
        <button onclick="this.parentElement.parentElement.classList.remove('show')" style="background:none; border:none; color:white; cursor:pointer; font-size:16px;">×</button>
    </div>`;
    
    el.className = 'toast-' + type + ' show';
    clearTimeout(toast.timer);
    toast.timer = setTimeout(()=>el.classList.remove('show'), 4000);
}"""
js = js.replace(old_toast, new_toast)

# Update specific toasts to use the new types
js = js.replace("toast(r.message+' Please sign in.');", "toast(r.message+' Please sign in.', 'success');")
js = js.replace("toast('Room successfully booked for 1 hour!');", "toast('Room successfully booked for 1 hour!', 'success');")
js = js.replace("toast('Booking failed: ' + e.message);", "toast('Booking failed: ' + e.message, 'error');")
js = js.replace("toast('Welcome to CampusSpace');", "toast('Welcome to CampusSpace', 'success');")

# --- Keyboard Shortcuts ---
js = js.replace(
    "bootstrap();",
    """
// Keyboard Shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        // Close Help Modal
        const helpModal = document.getElementById('help-modal');
        if (helpModal) helpModal.classList.add('hidden');
        // Close Fault Form
        const faultPanel = document.getElementById('fault-form-panel');
        if (faultPanel) faultPanel.classList.add('hidden');
    }
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
        e.preventDefault(); // Prevent typing / in the page
        const searchInput = document.getElementById('room-search');
        if (searchInput) searchInput.focus();
    }
});

bootstrap();
"""
)

with open('frontend/js/app.js', 'w') as f: f.write(js)


# 2. UPDATE style.css (Skeleton Animations & Toast Colors)
with open('frontend/css/style.css', 'r') as f: css = f.read()

css += """
/* --- SKELETON LOADING --- */
.skeleton-card { pointer-events: none; border-color: #e2e8f0; }
.skeleton-title { width: 50%; height: 20px; background: #e2e8f0; border-radius: 4px; margin-bottom: 15px; animation: pulse-bg 1.5s infinite; }
.skeleton-text { width: 80%; height: 12px; background: #e2e8f0; border-radius: 4px; margin-bottom: 8px; animation: pulse-bg 1.5s infinite; }
.skeleton-text.short { width: 40%; }
.skeleton-box { width: 100%; height: 40px; background: #e2e8f0; border-radius: 6px; margin-top: 15px; animation: pulse-bg 1.5s infinite; }
[data-theme="dark"] .skeleton-title, [data-theme="dark"] .skeleton-text, [data-theme="dark"] .skeleton-box { background: #334155; }
@keyframes pulse-bg { 0% { opacity: 0.6; } 50% { opacity: 0.3; } 100% { opacity: 0.6; } }

/* --- SMART TOASTS --- */
#toast { border-left: 4px solid #fff; }
#toast.toast-success { background: #10b981; border-left-color: #047857; }
#toast.toast-error { background: #ef4444; border-left-color: #b91c1c; }
#toast.toast-warning { background: #f59e0b; border-left-color: #b45309; }
#toast.toast-info { background: #3b82f6; border-left-color: #1d4ed8; }
"""
with open('frontend/css/style.css', 'w') as f: f.write(css)

print("✅ Added Skeleton Loaders, Smart Toasts with Icons, and Keyboard Shortcuts!")
