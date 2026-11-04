
const $ = (s,root=document)=>root.querySelector(s), $$=(s,root=document)=>[...root.querySelectorAll(s)];
let me=null, blocksCache=[], roomsCache=[], canteensCache=[];
const esc = v => String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function toast(msg, type='info'){
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
}
function dateText(){return new Date().toLocaleDateString(undefined,{weekday:'long',month:'long',day:'numeric'})}
function statusClass(s){return String(s||'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')}
function badge(s){return `<span class="status-badge ${statusClass(s)}">${esc(s)}</span>`}
function isAdmin(){return me?.role==='admin'} function isStaff(){return ['admin','maintenance'].includes(me?.role)}
async function api(path,opts){return API.request(path,opts)}
function authMode(mode){$$('[data-auth]').forEach(b=>b.classList.toggle('active',b.dataset.auth===mode));$('#login-form').classList.toggle('hidden',mode!=='login');$('#register-form').classList.toggle('hidden',mode!=='register')}
$$('[data-auth]').forEach(b=>b.addEventListener('click',()=>authMode(b.dataset.auth)));

// --- AUTHENTICATION ---
$('#login-form').addEventListener('submit',async e=>{
    e.preventDefault();
    const data=Object.fromEntries(new FormData(e.currentTarget));
    try{
        const r=await api('/auth/login',{method:'POST',body:data});
        localStorage.setItem('campusspace_token',r.access_token);
        me=r.user;
        showApp();
        toast('Welcome to CampusSpace', 'success');
    }catch(err){toast(err.message)}
});
$('#register-form').addEventListener('submit',async e=>{
    e.preventDefault();
    const form=e.currentTarget;
    const data=Object.fromEntries(new FormData(form));
    try{
        const r=await api('/auth/register',{method:'POST',body:data});
        toast(r.message+' Please sign in.', 'success');
        form.reset();
        authMode('login');
        $('#login-form [name=email]').value=data.email;
        $('#login-form [name=password]').value='';
    }catch(err){toast(err.message)}
});
$('#logout-btn').addEventListener('click',()=>{
    localStorage.removeItem('campusspace_token');
    me=null;
    $('#app-view').classList.add('hidden');
    $('#auth-view').classList.remove('hidden')
});
async function bootstrap(){if(!localStorage.getItem('campusspace_token'))return;try{me=await api('/auth/me');showApp()}catch{localStorage.removeItem('campusspace_token')}}
function showApp(){
    $('#auth-view').classList.add('hidden');
    $('#app-view').classList.remove('hidden');
    $('#side-name').textContent=me.full_name;
    $('#side-role').textContent=me.role;
    $('#avatar').textContent=$('#top-avatar').textContent=(me.full_name||'U').trim()[0].toUpperCase();
    $('#welcome-title').textContent=`Good day, ${(me.full_name||'there').split(' ')[0]} 👋`;
    $$('.role-admin').forEach(x=>x.classList.toggle('hidden',!isAdmin()));
    $$('.role-staff').forEach(x=>x.classList.toggle('hidden',!isStaff()));
    $('#date-label').textContent=dateText().toUpperCase();
    navigate('dashboard');
    refreshDashboard();loadBlocks();loadClassrooms();loadCanteens();loadFaults();loadTimetable();checkConnection();
}
const pageNames={dashboard:'Overview',classrooms:'Classroom finder',navigation:'Blocks & floors',faults:'Fault reports',canteens:'Scan & Done',visits:'My canteen visits',timetable:'Timetable',maintenance:'Maintenance desk',admin:'Admin console'};
function navigate(name){
    if((name==='admin'&&!isAdmin())||(name==='maintenance'&&!isStaff())){toast('This area requires staff permissions');return}
    $$('.page').forEach(p=>p.classList.toggle('active',p.id===`page-${name}`));
    $$('.nav-item').forEach(b=>b.classList.toggle('active',b.dataset.page===name));
    $('#page-title').textContent=pageNames[name]||'CampusSpace';
    $('.sidebar').classList.remove('open');
    if(name==='visits')loadVisits();
    if(name==='maintenance')loadMaintenance();
    if(name==='admin')loadAdmin()
}
$$('[data-page]').forEach(b=>b.addEventListener('click',()=>navigate(b.dataset.page)));
$$('[data-go]').forEach(b=>b.addEventListener('click',()=>navigate(b.dataset.go)));

async function checkConnection(){try{await fetch('/health/live');$('#connection-label').textContent='Backend online';$('.status-dot').style.background='#19a15f'}catch{$('#connection-label').textContent='Backend offline';$('.status-dot').style.background='#d34e4e'}}
async function refreshDashboard(){try{const [rooms,faults,canteens]=await Promise.all([api('/classrooms'),api('/fault-reports'),api('/canteens')]);$('#stats-grid').innerHTML=[['Classrooms',rooms.length,'Across four blocks'],['Campus blocks',blocksCache.length||4,'8 floors per block'],['Canteens',canteens.length,'QR check-in enabled'],['Open fault reports',faults.filter(f=>f.status!=='Completed').length,'Live backend data']].map(x=>`<div class="stat-card"><span>${x[0]}</span><strong>${x[1]}</strong><small>${x[2]}</small></div>`).join('');renderRecentFaults(faults.slice(0,5))}catch(e){console.warn(e)}}
function renderRecentFaults(rows){$('#recent-faults').innerHTML=rows.length?`<table><thead><tr><th>Ticket</th><th>Location</th><th>Issue</th><th>Status</th></tr></thead><tbody>${rows.map(r=>`<tr><td><strong>${esc(r.ticket_id)}</strong></td><td>${esc(r.room_number||'Canteen / facility')}</td><td>${esc(r.category)}</td><td>${badge(r.status)}</td></tr>`).join('')}</tbody></table>`:'<div class="empty">No fault reports found.</div>'}
async function loadBlocks(){try{blocksCache=await api('/blocks');$('#filter-block').innerHTML='<option value="">All blocks</option>'+blocksCache.map(b=>`<option value="${b.id}">${esc(b.name)}</option>`).join('');$('#block-grid').innerHTML=blocksCache.map(b=>`<article class="block-card"><div class="block-code">${esc(b.code)}</div><h3>${esc(b.name)}</h3><p>${b.floor_count} floors · ${b.classroom_count} classrooms</p><div class="floor-pills">${Array.from({length:8},(_,i)=>`<span>Floor ${i+1}${i<5?' · alleyway':''}</span>`).join('')}</div></article>`).join('');}catch(e){console.warn(e)}}
async function loadClassrooms(){ 
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
    try{const params=new URLSearchParams();if($('#filter-block').value)params.set('block_id',$('#filter-block').value);if($('#filter-floor').value)params.set('floor_number',$('#filter-floor').value);if($('#room-search').value.trim())params.set('search',$('#room-search').value.trim());if($('#filter-quiet').checked)params.set('quiet','true');roomsCache=await api('/classrooms?'+params);renderRooms(roomsCache)}catch(e){$('#room-grid').innerHTML=`<div class="empty">${esc(e.message)}</div>`}}

// --- NEW: PAGINATED RENDERING & UI TAGS ---
function renderRooms(rows){
    if(!rows.length){
        $('#room-grid').innerHTML='<div class="empty" style="text-align:center; padding:40px;"><div style="font-size:40px; margin-bottom:15px;">🔍</div><h3>No rooms found</h3><p>Try adjusting your block or floor filters.</p></div>';
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
        <div class="room-top"><div><h3>${esc(r.room_number)}</h3><p class="sub">${esc(r.block_name)} · Floor ${r.floor_number}</p></div><span class="room-status ${avail?'available':blocked?'blocked':''}"><span class="pulse-dot ${avail?'green':blocked?'red':'blue'}"></span>${esc(st)}</span></div>
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
        <div style="display:flex; gap:5px; margin-top:10px;">
    <button class="btn primary" data-verify="${r.id}" style="flex:1;">Verify status</button>
    <button class="btn secondary" data-book="${r.id}" style="flex:1;">Book 1hr</button>
    </div>
        </article>`
    }).join('');
    $('#room-grid').innerHTML = html;
    $$('[data-room-detail]').forEach(b=>b.onclick=()=>roomDetail(b.dataset.roomDetail));
    $$('[data-verify]').forEach(b=>b.onclick=()=>verifyRoom(b.dataset.verify));
    $$('[data-book]').forEach(b=>b.onclick=()=>bookRoom(b.dataset.book));
}

$('#search-rooms').onclick=loadClassrooms;$('#refresh-rooms').onclick=loadClassrooms;$('#filter-block').onchange=loadClassrooms;$('#filter-floor').onchange=loadClassrooms;$('#filter-quiet').onchange=loadClassrooms;$('#room-search').addEventListener('keydown',e=>{if(e.key==='Enter')loadClassrooms()});
async function roomDetail(id){try{const r=await api(`/classrooms/${id}`);const schedule=(r.timetable||[]).slice(0,5).map(t=>`${t.day_of_week} ${t.start_time}-${t.end_time}: ${t.subject_name||'Class'}`).join('\n')||'No sample timetable entries';alert(`${r.room_number} · ${r.block_name}, Floor ${r.floor_number}\nStatus: ${r.availability.status}\nCapacity: ${r.capacity}\nSockets: ${r.student_sockets} student / ${r.faculty_sockets} faculty\n\nTimetable:\n${schedule}\n\nReminder: no scheduled class does not guarantee physical vacancy.`)}catch(e){toast(e.message)}}
async function bookRoom(id){
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
            toast('Room successfully booked for 1 hour!', 'success');
            const bookings = JSON.parse(localStorage.getItem('my_bookings') || '[]');
            bookings.push({ room: 'Room ID ' + id, time: 'Today, 1 Hour', purpose: 'Study session' });
            localStorage.setItem('my_bookings', JSON.stringify(bookings));
            loadClassrooms();
        } catch(e) {
            toast('Booking failed: ' + e.message, 'error');
        }
    }
    async function verifyRoom(id){const status=prompt('Enter status exactly: Reported Available, Reported Occupied, or Restricted','Reported Available');if(!status)return;try{await api(`/classrooms/${id}/verifications`,{method:'POST',body:{reported_status:status}});toast('Room status verification submitted');loadClassrooms()}catch(e){toast(e.message)}}
function loadFaultLocationOptions(){const type=$('#fault-location-type').value;const rows=type==='classroom'?roomsCache:canteensCache;$('#fault-location').innerHTML=rows.map(r=>`<option value="${r.id}">${esc(r.room_number||r.name)}${r.block_name?' · '+esc(r.block_name):''}</option>`).join('')}
$('#new-fault-btn').onclick=()=>{$('#fault-form-panel').classList.remove('hidden');loadFaultLocationOptions()};$('#close-fault-form').onclick=()=>$('#fault-form-panel').classList.add('hidden');$('#fault-location-type').onchange=loadFaultLocationOptions;
$('#fault-form').addEventListener('submit',async e=>{e.preventDefault();const f=new FormData(e.currentTarget);const type=f.get('location_type');const body={category:f.get('category'),description:f.get('description'),is_urgent:f.has('is_urgent'),classroom_id:type==='classroom'?Number(f.get('location_id')):null,canteen_id:type==='canteen'?Number(f.get('location_id')):null};try{const r=await api('/fault-reports',{method:'POST',body});toast(`${r.message} Ticket: ${r.ticket_id}`);e.currentTarget.reset();$('#fault-form-panel').classList.add('hidden');loadFaults();refreshDashboard()}catch(err){toast(err.message)}});
async function loadFaults(){try{const rows=await api('/fault-reports');const status=$('#fault-status-filter').value;const filtered=status?rows.filter(r=>r.status===status):rows;$('#fault-table').innerHTML=filtered.length?`<table><thead><tr><th>Ticket</th><th>Location</th><th>Category</th><th>Submitted</th><th>Status</th><th>Priority</th></tr></thead><tbody>${filtered.map(r=>`<tr><td><strong>${esc(r.ticket_id)}</strong></td><td>${esc(r.room_number||'Canteen / facility')} ${r.block_name?'· '+esc(r.block_name):''}</td><td>${esc(r.category)}</td><td>${esc(r.created_at)}</td><td>${badge(r.status)}</td><td>${r.is_urgent?'<span class="status-badge escalated-to-higher-authority">Urgent</span>':'Normal'}</td></tr>`).join('')}</tbody></table>`:'<div class="empty" style="text-align:center; padding:30px;"><div style="font-size:40px; margin-bottom:10px;">🛠️</div><h3>No fault reports found</h3><p>Submit a new report to get started.</p></div>';$('#fault-subtitle').textContent=isStaff()?'All campus reports':'Your reports and their latest status';}catch(e){$('#fault-table').innerHTML=`<div class="empty">${esc(e.message)}</div>`}}
$('#fault-status-filter').onchange=loadFaults;

async function loadCanteens(){try{canteensCache=await api('/canteens');$('#canteen-grid').innerHTML=canteensCache.map(c=>{const pct=Math.min(100,Math.round(c.active_registrations/Math.max(1,c.capacity)*100));const level=c.crowd_level.toLowerCase();return `<article class="canteen-card"><div class="canteen-icon">🥗</div><h3>${esc(c.name)}</h3><p>${esc(c.block_name)} · Floor ${c.floor_number} · Code ${esc(c.code)}</p><div class="crowd-num">${c.active_registrations}<span class="crowd-label"> / ${c.capacity}</span></div><div class="crowd-label">Active registrations · <strong>${esc(c.crowd_level)} crowd</strong></div><div class="crowd-meter"><span class="${level}" style="width:${pct}%"></span></div><p>Visit default: ${c.default_visit_duration_min} min</p><button class="btn primary" data-checkin="${esc(c.qr_code_identifier)}">Check in here</button></article>`}).join('');$$('[data-checkin]').forEach(b=>b.onclick=()=>checkin(b.dataset.checkin));loadFaultLocationOptions()}catch(e){$('#canteen-grid').innerHTML=`<div class="empty">${esc(e.message)}</div>`}}
$('#refresh-canteens').onclick=loadCanteens;
async function checkin(identifier){if(!confirm(`Confirm check-in using ${identifier}? Your active registration expires after the configured visit window.`))return;try{const r=await api('/canteens/check-in',{method:'POST',body:{qr_identifier:identifier}});toast(r.message||`Checked in at ${r.canteen}`);loadCanteens();loadVisits()}catch(e){toast(e.message)}}
$('#checkin-form').addEventListener('submit',e=>{e.preventDefault();checkin(new FormData(e.currentTarget).get('qr_identifier'))});
async function loadVisits(){try{const rows=await api('/canteen-visits/mine');$('#visits-table').innerHTML=rows.length?`<table><thead><tr><th>Canteen</th><th>Checked in</th><th>Expires</th><th>Status</th><th>Action</th></tr></thead><tbody>${rows.map(v=>`<tr><td>${esc(v.canteen_name)}</td><td>${esc(v.check_in_time)}</td><td>${esc(v.expires_at)}</td><td>${badge(v.status)}</td><td>${v.status==='Active'?`<button class="table-action" data-checkout="${v.id}">I'm leaving</button>`:'—'}</td></tr>`).join('')}</tbody></table>`:'<div class="empty" style="text-align:center; padding:30px;"><div style="font-size:40px; margin-bottom:10px;">🥗</div><h3>No active visits</h3><p>Scan a canteen QR code to check in.</p></div>';$$('[data-checkout]').forEach(b=>b.onclick=async()=>{try{await api(`/canteen-visits/${b.dataset.checkout}/checkout`,{method:'POST'});toast('Checked out successfully');loadVisits();loadCanteens()}catch(e){toast(e.message)}})}catch(e){$('#visits-table').innerHTML=`<div class="empty">${esc(e.message)}</div>`}}
$('#refresh-visits').onclick=loadVisits;
async function loadTimetable(){try{const day=$('#timetable-day').value;const rows=await api('/timetable?day_of_week='+encodeURIComponent(day));$('#timetable-table').innerHTML=rows.length?`<table><thead><tr><th>Room</th><th>Block</th><th>Floor</th><th>Subject / event</th><th>Start</th><th>End</th><th>Type</th></tr></thead><tbody>${rows.map(t=>`<tr><td>${esc(t.room_number)}</td><td>${esc(t.block_name)}</td><td>${t.floor_number}</td><td>${esc(t.subject_name||'—')}</td><td>${esc(t.start_time)}</td><td>${esc(t.end_time)}</td><td>${t.is_break_slot?'Break':'Class'}</td></tr>`).join('')}</tbody></table>`:`<div class="empty">No ${esc(day)} entries in the current sample dataset.</div>`}catch(e){$('#timetable-table').innerHTML=`<div class="empty">${esc(e.message)}</div>`}}
$('#timetable-day').onchange=loadTimetable;
async function loadMaintenance(){try{const [rows,summary]=await Promise.all([api('/fault-reports'),api('/maintenance/summary')]);$('#maintenance-stats').innerHTML=Object.entries(summary).map(([k,v])=>`<div class="stat-card"><span>${esc(k)}</span><strong>${v}</strong><small>Maintenance tickets</small></div>`).join('');$('#maintenance-table').innerHTML=rows.length?`<table><thead><tr><th>Ticket</th><th>Location</th><th>Issue</th><th>Priority</th><th>Status</th><th>Update</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${esc(r.ticket_id)}</td><td>${esc(r.room_number||'Canteen / facility')}</td><td>${esc(r.category)}<br><span class="muted">${esc(r.description)}</span></td><td>${r.is_urgent?'Urgent':'Normal'}</td><td>${badge(r.status)}</td><td><button class="table-action" data-update-fault="${r.id}">Update</button></td></tr>`).join('')}</tbody></table>`:'<div class="empty" style="text-align:center; padding:30px;"><div style="font-size:40px; margin-bottom:10px;">✅</div><h3>All caught up!</h3><p>No pending maintenance tickets.</p></div>';$$('[data-update-fault]').forEach(b=>b.onclick=()=>updateFault(b.dataset.updateFault))}catch(e){$('#maintenance-table').innerHTML=`<div class="empty">${esc(e.message)}</div>`}}
$('#refresh-maintenance').onclick=loadMaintenance;
async function updateFault(id){const status=prompt('New status: Submitted, In Progress, Completed, Escalated to Higher Authority','In Progress');if(!status)return;const note=prompt('Progress / resolution note (optional)','');try{await api(`/fault-reports/${id}`,{method:'PATCH',body:{status,note:note||''}});toast('Ticket updated');loadMaintenance();loadFaults();refreshDashboard()}catch(e){toast(e.message)}}
async function loadAdmin(){
    const table=$('#users-table');
    try{
        const [overview,users]=await Promise.all([api('/admin/overview'),api('/admin/users')]);
        $('#admin-stats').innerHTML=Object.entries(overview).map(([k,v])=>`<div class="stat-card"><span>${esc(k.replaceAll('_',' '))}</span><strong>${v}</strong><small>Live database count</small></div>`).join('');
        table.innerHTML=users.length?`<table><thead><tr><th>Name</th><th>Email</th><th>Department</th><th>Role</th><th>Account</th><th>Actions</th></tr></thead><tbody>${users.map(u=>`<tr><td>${esc(u.full_name)}</td><td>${esc(u.email)}</td><td>${esc(u.department)}</td><td><select class="admin-role" data-role-user="${u.id}">${['student','maintenance','admin'].map(r=>`<option value="${r}" ${u.role===r?'selected':''}>${r}</option>`).join('')}</select></td><td>${u.is_active?'Active':'Disabled'}</td><td><button class="table-action" data-toggle-user="${u.id}" data-active="${u.is_active?0:1}">${u.is_active?'Disable':'Enable'}</button> <button class="table-action" data-reset-password="${u.id}">Set password</button></td></tr>`).join('')}</tbody></table>`:'<div class="empty">No users.</div>';
        $$('[data-role-user]').forEach(sel=>sel.onchange=async()=>{try{await api(`/admin/users/${sel.dataset.roleUser}`,{method:'PATCH',body:{role:sel.value}});toast('Role updated');await loadAdmin()}catch(err){toast(err.message);await loadAdmin()}});
        $$('[data-toggle-user]').forEach(btn=>btn.onclick=async()=>{try{await api(`/admin/users/${btn.dataset.toggleUser}`,{method:'PATCH',body:{is_active:btn.dataset.active==='1'}});toast('Account updated');await loadAdmin()}catch(err){toast(err.message)}});
        $$('[data-reset-password]').forEach(btn=>btn.onclick=async()=>{const password=prompt('Set a new password (minimum 8 characters). Passwords are stored as hashes.');if(!password)return;try{await api(`/admin/users/${btn.dataset.resetPassword}`,{method:'PATCH',body:{password}});toast('Password changed');}catch(err){toast(err.message)}});
    }catch(err){table.innerHTML=`<div class="empty">Could not load users: ${esc(err.message)}. Try Refresh.</div>`}
}
$('#refresh-admin').onclick=loadAdmin;
$('#admin-create-user-form').addEventListener('submit',async e=>{
    e.preventDefault();
    const form=e.currentTarget;
    const submitButton=form.querySelector('button[type="submit"],button:not([type])');
    const data=Object.fromEntries(new FormData(form));
    if(submitButton){submitButton.disabled=true;submitButton.textContent='Creating…'}
    try{
        const r=await api('/admin/users',{method:'POST',body:data});
        form.reset();
        await loadAdmin();
        toast(`Created ${r.role} account: ${r.email}. User management refreshed.`);
    }catch(err){toast(`Could not create account: ${err.message}`)}
    finally{if(submitButton){submitButton.disabled=false;submitButton.textContent='Create account'}}
});
$('#timetable-import-form').addEventListener('submit',async e=>{e.preventDefault();const fd=new FormData(e.currentTarget);try{const r=await api('/admin/timetable/import',{method:'POST',body:fd});toast(`${r.message}: ${r.rows_inserted} rows`);loadTimetable()}catch(err){toast(err.message)}});

// --- NEW FEATURES INJECTED HERE ---
// Dark Mode
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

// Mobile Sidebar
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

// Simulate Scan
const simScan = document.getElementById('simulate-scan-btn');
if (simScan) {
    simScan.addEventListener('click', () => {
        const input = document.querySelector('#checkin-form [name="qr_identifier"]');
        input.value = 'QR_B25C_FLOOR6';
        if (typeof toast === 'function') toast('Simulated QR Scan: B25 Main Canteen');
        setTimeout(() => { document.getElementById('checkin-form').dispatchEvent(new Event('submit')); }, 800);
    });
}


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



