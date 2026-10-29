# 1. UPDATE index.html (Add loading container)
with open('frontend/index.html', 'r') as f: html = f.read()
# Add a spinner to the room grid initially
html = html.replace('<div id="room-grid" class="room-grid"></div>', 
    '<div id="room-grid" class="room-grid"><div class="loading-spinner"></div></div>')
with open('frontend/index.html', 'w') as f: f.write(html)

# 2. UPDATE app.js (Add Booking Logic, Spinner, Empty State)
with open('frontend/js/app.js', 'r') as f: js = f.read()

# Add loading spinner logic to loadClassrooms
js = js.replace(
    "async function loadClassrooms(){try{",
    "async function loadClassrooms(){ $('#room-grid').innerHTML = '<div class=\"loading-spinner\"></div>'; try{"
)

# Update renderRooms to include the Booking button and better empty state
old_render = """function renderRooms(rows){
    if(!rows.length){
        $('#room-grid').innerHTML='<div class="empty">No classrooms match these filters.</div>';
        return;
    }"""
new_render = """function renderRooms(rows){
    if(!rows.length){
        $('#room-grid').innerHTML='<div class="empty" style="text-align:center; padding:40px;"><div style="font-size:40px; margin-bottom:15px;">🔍</div><h3>No rooms found</h3><p>Try adjusting your block or floor filters.</p></div>';
        return;
    }"""
js = js.replace(old_render, new_render)

# Add the Book Room button to the HTML template
js = js.replace(
    '<button class="btn primary" data-verify="${r.id}">Verify status</button>',
    '''<div style="display:flex; gap:5px; margin-top:10px;">
    <button class="btn primary" data-verify="${r.id}" style="flex:1;">Verify status</button>
    <button class="btn secondary" data-book="${r.id}" style="flex:1;">Book 1hr</button>
    </div>'''
)

# Add the Booking Event Listener at the bottom of renderRooms
js = js.replace(
    "$$('[data-verify]').forEach(b=>b.onclick=()=>verifyRoom(b.dataset.verify));",
    """$$('[data-verify]').forEach(b=>b.onclick=()=>verifyRoom(b.dataset.verify));
    $$('[data-book]').forEach(b=>b.onclick=()=>bookRoom(b.dataset.book));"""
)

# Add the bookRoom function right after verifyRoom
js = js.replace(
    "async function verifyRoom(id){",
    """async function bookRoom(id){
        const now = new Date();
        const end = new Date(now.getTime() + 60 * 60000); // +1 hour
        try {
            await api('/classrooms/' + id + '/bookings', {
                method: 'POST',
                body: {
                    starts_at: now.toISOString(),
                    ends_at: end.toISOString(),
                    purpose: 'Study session'
                }
            });
            toast('Room successfully booked for 1 hour!');
            loadClassrooms();
        } catch(e) {
            toast('Booking failed: ' + e.message);
        }
    }
    async function verifyRoom(id){"""
)

with open('frontend/js/app.js', 'w') as f: f.write(js)

# 3. UPDATE style.css (Add Spinner CSS)
with open('frontend/css/style.css', 'r') as f: css = f.read()
css += """
/* Loading Spinner */
.loading-spinner {
  width: 40px; height: 40px; border: 4px solid var(--line);
  border-top: 4px solid var(--blue); border-radius: 50%;
  animation: spin 1s linear infinite; margin: 40px auto; grid-column: 1/-1;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
"""
with open('frontend/css/style.css', 'w') as f: f.write(css)

print("✅ Added Book Room functionality, Loading Spinners, and Beautiful Empty States!")
