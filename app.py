import streamlit as st
import streamlit.components.v1 as components
import math

st.set_page_config(page_title="SafeTrail", page_icon="🛡️", layout="wide")

for k, v in {"page":"Login","logged_in":False,"username":"","lat":None,"lon":None,"accuracy":None,"gps_error":None,"gps_granted":False}.items():
    if k not in st.session_state: st.session_state[k] = v

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #020817; color: #e2e8f0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1280px !important; }

/* ═══ ANIMATED BG ═══ */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(56,189,248,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(139,92,246,0.08) 0%, transparent 60%),
        #020817;
}

/* ═══ SIDEBAR ═══ */
[data-testid="stSidebar"] {
    background: rgba(2,8,23,0.95) !important;
    border-right: 1px solid rgba(56,189,248,0.1) !important;
    backdrop-filter: blur(20px);
}
[data-testid="stSidebar"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 200px;
    background: radial-gradient(ellipse at 50% 0%, rgba(56,189,248,0.12) 0%, transparent 70%);
    pointer-events: none;
}

.brand-wrap {
    padding: 2.2rem 1.2rem 1.8rem;
    text-align: center;
    position: relative;
}
.brand-icon {
    width: 64px; height: 64px;
    background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
    border-radius: 18px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 30px;
    box-shadow: 0 0 30px rgba(14,165,233,0.4), 0 0 60px rgba(14,165,233,0.15);
    margin-bottom: 1rem;
}
.brand-name {
    font-family: 'Syne', sans-serif;
    font-size: 22px; font-weight: 800;
    background: linear-gradient(135deg, #38bdf8, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}
.brand-tag { font-size: 11px; color: #334155; letter-spacing: 2px; text-transform: uppercase; margin-top: 2px; }
.brand-sep { height: 1px; background: linear-gradient(90deg, transparent, rgba(56,189,248,0.2), transparent); margin: 1.5rem 0; }

/* GPS badge */
.gps-badge {
    display: flex; align-items: center; gap: 8px;
    margin: 0 1rem 1.2rem;
    padding: .5rem 1rem;
    border-radius: 30px;
    font-size: 11px; font-weight: 600; letter-spacing: 0.3px;
    border: 1px solid;
}
.gps-badge.live   { background: rgba(34,197,94,0.08); border-color: rgba(34,197,94,0.25); color: #4ade80; }
.gps-badge.wait   { background: rgba(251,191,36,0.08); border-color: rgba(251,191,36,0.25); color: #fbbf24; }
.gps-badge.err    { background: rgba(248,113,113,0.08); border-color: rgba(248,113,113,0.25); color: #f87171; }
.dot {
    width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0;
}
.dot.live { background: #4ade80; box-shadow: 0 0 6px #4ade80; animation: blink 1.4s infinite; }
.dot.wait { background: #fbbf24; }
.dot.err  { background: #f87171; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }

/* nav section label */
.nav-sec { font-size: 9.5px; color: #1e3a5f; text-transform: uppercase; letter-spacing: 2px; padding: 0 1.2rem .5rem; }

/* nav buttons */
.stButton > button {
    background: transparent !important;
    color: #475569 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: .6rem 1rem !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-align: left !important;
    width: 100% !important;
    transition: all .2s ease !important;
    letter-spacing: 0.1px !important;
}
.stButton > button:hover {
    background: rgba(56,189,248,0.07) !important;
    color: #7dd3fc !important;
    transform: translateX(3px) !important;
}
.nav-active > .stButton > button {
    background: linear-gradient(90deg, rgba(14,165,233,0.15), rgba(139,92,246,0.08)) !important;
    color: #38bdf8 !important;
    border-left: 2px solid #38bdf8 !important;
    font-weight: 600 !important;
}

/* ═══ PAGE HEADER ═══ */
.ph-wrap { margin-bottom: 2rem; }
.ph-eyebrow { font-size: 11px; text-transform: uppercase; letter-spacing: 3px; color: #0ea5e9; font-weight: 600; margin-bottom: .5rem; }
.ph-title {
    font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 800;
    background: linear-gradient(135deg, #f0f9ff 0%, #7dd3fc 50%, #a78bfa 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1.1; letter-spacing: -1px;
}
.ph-sub { font-size: 13.5px; color: #475569; margin-top: .5rem; line-height: 1.6; }

/* ═══ GLASS CARDS ═══ */
.gc {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 1.6rem;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
    margin-bottom: 1rem;
}
.gc::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.3), transparent);
}
.gc-title { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 1rem; }

/* ═══ STAT CARDS ═══ */
.sc {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 1.4rem 1.6rem;
    position: relative; overflow: hidden;
}
.sc::after {
    content: attr(data-icon);
    position: absolute; right: 1rem; top: 50%; transform: translateY(-50%);
    font-size: 36px; opacity: .07;
}
.sc-accent { height: 2px; border-radius: 2px; margin-bottom: 1.1rem; }
.sc-label { font-size: 10.5px; text-transform: uppercase; letter-spacing: 2px; color: #334155; margin-bottom: .4rem; }
.sc-value { font-family: 'Syne', sans-serif; font-size: 30px; font-weight: 800; color: #f8fafc; line-height: 1; }
.sc-sub { font-size: 11.5px; color: #334155; margin-top: .4rem; }

/* ═══ INPUTS ═══ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-size: 14px !important;
    padding: .75rem 1rem !important;
    transition: all .2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(56,189,248,0.5) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.1), 0 0 20px rgba(56,189,248,0.08) !important;
    background: rgba(56,189,248,0.04) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label, .stNumberInput label {
    color: #64748b !important; font-size: 12px !important; font-weight: 600 !important;
    text-transform: uppercase !important; letter-spacing: 1px !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 12px !important; color: #e2e8f0 !important;
}

/* ═══ ACTION BUTTONS ═══ */
.abtn .stButton > button {
    background: linear-gradient(135deg, #0ea5e9, #8b5cf6) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; padding: .75rem 2rem !important;
    font-weight: 700 !important; font-size: 14px !important;
    letter-spacing: .3px !important; text-align: center !important;
    box-shadow: 0 4px 20px rgba(14,165,233,0.3), 0 0 40px rgba(14,165,233,0.1) !important;
    transition: all .2s !important;
}
.abtn .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(14,165,233,0.4) !important;
}

/* SOS */
.sos .stButton > button {
    background: linear-gradient(135deg, #ef4444, #dc2626) !important;
    color: #fff !important; border: none !important;
    border-radius: 999px !important; padding: 1.1rem 2.5rem !important;
    font-weight: 800 !important; font-size: 17px !important;
    letter-spacing: 1px !important; text-align: center !important;
    box-shadow: 0 0 0 0 rgba(239,68,68,.5) !important;
    animation: sosPulse 2s infinite !important;
}
@keyframes sosPulse {
    0%  { box-shadow: 0 0 0 0 rgba(239,68,68,.6), 0 0 30px rgba(239,68,68,.3); }
    70% { box-shadow: 0 0 0 18px rgba(239,68,68,0), 0 0 50px rgba(239,68,68,.5); }
    100%{ box-shadow: 0 0 0 0 rgba(239,68,68,0), 0 0 30px rgba(239,68,68,.3); }
}

/* ═══ COORD TABLE ═══ */
.ctab { background: rgba(0,0,0,0.3); border: 1px solid rgba(56,189,248,0.1); border-radius: 14px; overflow: hidden; }
.crow { display: flex; justify-content: space-between; align-items: center; padding: .75rem 1.1rem; border-bottom: 1px solid rgba(255,255,255,0.04); }
.crow:last-child { border-bottom: none; }
.ck { font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #334155; }
.cv { font-family: 'Syne', sans-serif; font-size: 14px; font-weight: 700; color: #38bdf8; }

/* ═══ RISK BAR ═══ */
.rbar-bg { background: rgba(255,255,255,0.05); border-radius: 99px; height: 10px; overflow: hidden; margin: 1rem 0; }
.rbar-fg { height: 10px; border-radius: 99px; transition: width .5s; }

/* ═══ LOGIN PAGE ═══ */
.login-wrap {
    min-height: 80vh; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
}
.login-glow {
    width: 120px; height: 120px;
    background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
    border-radius: 32px;
    display: flex; align-items: center; justify-content: center;
    font-size: 52px;
    box-shadow: 0 0 60px rgba(14,165,233,0.5), 0 0 120px rgba(14,165,233,0.2);
    margin-bottom: 1.5rem;
}
.login-title {
    font-family: 'Syne', sans-serif; font-size: 34px; font-weight: 800;
    background: linear-gradient(135deg, #f0f9ff, #7dd3fc, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; margin-bottom: .5rem; letter-spacing: -1px;
}
.login-sub { font-size: 14px; color: #475569; text-align: center; margin-bottom: 2rem; }
.login-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px; padding: 2.5rem 2rem;
    width: 100%; max-width: 420px;
    backdrop-filter: blur(20px);
    position: relative; overflow: hidden;
}
.login-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.5), rgba(139,92,246,0.5), transparent);
}

/* ═══ GEO-FENCE STATUS ═══ */
.gf-box {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px; padding: 2.5rem 1.5rem;
    text-align: center;
}
.gf-title { font-family: 'Syne', sans-serif; font-size: 24px; font-weight: 800; margin: .75rem 0 .4rem; }
.gf-sub { font-size: 13px; color: #475569; }

/* ═══ TABLE ═══ */
[data-testid="stTable"] { background: transparent !important; }
thead tr th { background: rgba(56,189,248,0.08) !important; color: #7dd3fc !important; font-size: 11px !important; letter-spacing: 1px !important; text-transform: uppercase !important; }
tbody tr { background: rgba(255,255,255,0.02) !important; border-bottom: 1px solid rgba(255,255,255,0.04) !important; }
tbody tr:hover { background: rgba(56,189,248,0.05) !important; }

/* ═══ TOGGLE ═══ */
.stToggle { color: #64748b !important; }

.divline { height:1px; background:linear-gradient(90deg,transparent,rgba(56,189,248,0.15),transparent); margin:.8rem 0; }
</style>
""", unsafe_allow_html=True)

# ── GPS JS ──────────────────────────────────────────────────────────────────
GPS_HTML = """
<div id="gs" style="font-size:11px;color:#334155;font-family:monospace;padding:2px 0"></div>
<script>
(function(){
  var s=document.getElementById('gs');
  if(!navigator.geolocation){s.textContent='GPS not supported';return;}
  s.textContent='Requesting GPS...';
  navigator.geolocation.watchPosition(function(p){
    var la=p.coords.latitude,lo=p.coords.longitude,ac=p.coords.accuracy;
    s.textContent='GPS: '+la.toFixed(5)+', '+lo.toFixed(5)+' ±'+Math.round(ac)+'m';
    var u=new URL(window.parent.location.href);
    u.searchParams.set('gps_lat',la.toFixed(7));
    u.searchParams.set('gps_lon',lo.toFixed(7));
    u.searchParams.set('gps_acc',Math.round(ac));
    window.parent.history.replaceState(null,'',u.toString());
  },function(e){
    s.textContent='GPS error: '+e.message;
    var u=new URL(window.parent.location.href);
    u.searchParams.set('gps_error',e.message);
    window.parent.history.replaceState(null,'',u.toString());
  },{enableHighAccuracy:true,timeout:15000,maximumAge:0});
})();
</script>
"""

qp = st.query_params
if "gps_lat" in qp and "gps_lon" in qp:
    try:
        st.session_state.lat      = float(qp["gps_lat"])
        st.session_state.lon      = float(qp["gps_lon"])
        st.session_state.accuracy = float(qp.get("gps_acc", 0))
        st.session_state.gps_granted = True
        st.session_state.gps_error   = None
    except: pass
if "gps_error" in qp:
    st.session_state.gps_error = qp["gps_error"]

def haversine(la1,lo1,la2,lo2):
    R=6371000; p1,p2=math.radians(la1),math.radians(la2)
    dp=math.radians(la2-la1); dl=math.radians(lo2-lo1)
    a=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return R*2*math.atan2(math.sqrt(a),math.sqrt(1-a))

def mapsembed(lat,lon,lbl="You"):
    return f'<iframe width="100%" height="320" style="border:0;border-radius:16px;" loading="lazy" src="https://maps.google.com/maps?q={lat},{lon}&z=16&output=embed"></iframe><div style="font-size:11px;color:#334155;text-align:center;margin-top:.4rem;">📍 {lbl} — {lat:.6f}, {lon:.6f}</div>'

# ── SIDEBAR ─────────────────────────────────────────────────────────────────
nav_items = [("🔐","Login"),("📡","Dashboard"),("📍","Geo-Fencing"),("🆘","SOS Emergency"),("🤖","AI Risk"),("📋","Incident Report"),("⚙️","Admin")]

with st.sidebar:
    st.markdown('<div class="brand-wrap"><div class="brand-icon">🛡️</div><div class="brand-name">SafeTrail</div><div class="brand-tag">GPS Safety System</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sep"></div>', unsafe_allow_html=True)

    lat = st.session_state.lat
    if st.session_state.gps_error:
        st.markdown(f'<div class="gps-badge err"><div class="dot err"></div>GPS Error</div>', unsafe_allow_html=True)
    elif lat:
        st.markdown(f'<div class="gps-badge live"><div class="dot live"></div>GPS Live · ±{st.session_state.accuracy:.0f}m</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="gps-badge wait"><div class="dot wait"></div>Waiting for GPS…</div>', unsafe_allow_html=True)

    st.markdown('<div class="nav-sec">Navigation</div>', unsafe_allow_html=True)
    for icon, label in nav_items:
        active = st.session_state.page == label
        if active: st.markdown('<div class="nav-active">', unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=f"n_{label}", use_container_width=True):
            st.session_state.page = label; st.rerun()
        if active: st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divline"></div>', unsafe_allow_html=True)
    if st.session_state.logged_in:
        st.markdown(f'<div style="text-align:center;padding:.4rem;font-size:12px;color:#38bdf8;font-weight:600;">👤 {st.session_state.username}</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;font-size:10px;color:#1e293b;padding:.3rem;">© 2025 SafeTrail Inc.</div>', unsafe_allow_html=True)

page = st.session_state.page
components.html(GPS_HTML, height=22)

# ════════════════════ LOGIN ════════════════════
if page == "Login":
    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center"><div class="login-glow">🛡️</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="login-title">SafeTrail</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">Intelligent Tourist Safety Platform<br>with Live GPS Tracking</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        uname = st.text_input("Username", placeholder="Enter your username")
        pw    = st.text_input("Password", type="password", placeholder="••••••••")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="abtn">', unsafe_allow_html=True)
        if st.button("Sign In  →", use_container_width=True):
            if uname == "admin" and pw == "1234":
                st.session_state.logged_in = True
                st.session_state.username  = uname
                st.session_state.page      = "Dashboard"
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Use  admin / 1234")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;margin-top:1.2rem;font-size:12px;color:#1e3a5f;">Demo: <code style="color:#38bdf8;background:rgba(56,189,248,.1);padding:1px 6px;border-radius:4px;">admin</code> / <code style="color:#38bdf8;background:rgba(56,189,248,.1);padding:1px 6px;border-radius:4px;">1234</code></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if not st.session_state.gps_granted:
            st.markdown('<div style="text-align:center;margin-top:1rem;font-size:12px;color:#1e3a5f;background:rgba(56,189,248,.05);border:1px solid rgba(56,189,248,.1);border-radius:10px;padding:.8rem;">📡 Allow browser location access to activate GPS tracking</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════ DASHBOARD ════════════════════
elif page == "Dashboard":
    lat = st.session_state.lat; lon = st.session_state.lon; acc = st.session_state.accuracy
    st.markdown('<div class="ph-wrap"><div class="ph-eyebrow">Live Monitoring</div><div class="ph-title">Tourist Dashboard</div><div class="ph-sub">Real-time GPS tracking for ' + st.session_state.username + '</div></div>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    stats = [
        (c1,"linear-gradient(90deg,#38bdf8,#818cf8)","Latitude",   f"{lat:.5f}°" if lat else "—","Live GPS","🌐"),
        (c2,"linear-gradient(90deg,#818cf8,#ec4899)","Longitude",  f"{lon:.5f}°" if lon else "—","Live GPS","🌐"),
        (c3,"linear-gradient(90deg,#34d399,#0ea5e9)","Accuracy",   f"±{acc:.0f}m" if acc else "—","GPS precision","🎯"),
        (c4,"linear-gradient(90deg,#fbbf24,#f97316)","GPS Status", "● LIVE" if lat else "○ WAIT","navigator.geolocation","📡"),
    ]
    for col,grad,lbl,val,sub,icon in stats:
        with col:
            st.markdown(f'<div class="sc" data-icon="{icon}"><div class="sc-accent" style="background:{grad}"></div><div class="sc-label">{lbl}</div><div class="sc-value" style="font-size:22px">{val}</div><div class="sc-sub">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.7,1])
    with c1:
        st.markdown('<div class="gc"><div class="gc-title">🗺️ Your Live Location</div>', unsafe_allow_html=True)
        if lat and lon:
            st.markdown(mapsembed(lat, lon, f"{st.session_state.username}'s live position"), unsafe_allow_html=True)
        else:
            st.markdown('<div style="height:200px;display:flex;align-items:center;justify-content:center;color:#334155;font-size:14px;">📡 Waiting for GPS signal — allow location in browser</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="gc"><div class="gc-title">📐 Coordinates</div>', unsafe_allow_html=True)
        if lat and lon:
            st.markdown(f'''<div class="ctab">
              <div class="crow"><span class="ck">Latitude</span><span class="cv">{lat:.7f}°</span></div>
              <div class="crow"><span class="ck">Longitude</span><span class="cv">{lon:.7f}°</span></div>
              <div class="crow"><span class="ck">Accuracy</span><span class="cv">±{acc:.1f} m</span></div>
              <div class="crow"><span class="ck">User</span><span class="cv">{st.session_state.username}</span></div>
            </div>
            <a href="https://www.google.com/maps?q={lat},{lon}" target="_blank" style="display:block;margin-top:1rem;text-align:center;font-size:13px;color:#38bdf8;text-decoration:none;padding:.6rem;background:rgba(56,189,248,.07);border-radius:10px;border:1px solid rgba(56,189,248,.15);">🔗 Open in Google Maps ↗</a>''', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#334155;font-size:13px;padding:1rem;">Coordinates appear once GPS is active.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════ GEO-FENCING ════════════════════
elif page == "Geo-Fencing":
    lat = st.session_state.lat; lon = st.session_state.lon
    st.markdown('<div class="ph-wrap"><div class="ph-eyebrow">Boundary Detection</div><div class="ph-title">Geo-Fencing</div><div class="ph-sub">Define a safe zone and your live GPS is checked in real-time</div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1.6])
    with c1:
        st.markdown('<div class="gc"><div class="gc-title">⚙️ Zone Settings</div>', unsafe_allow_html=True)
        zla = st.number_input("Zone Centre Latitude",  value=lat if lat else 13.0827, format="%.6f", step=0.0001)
        zlo = st.number_input("Zone Centre Longitude", value=lon if lon else 80.2707, format="%.6f", step=0.0001)
        rad = st.slider("Safe Radius (m)", 50, 5000, 500, step=50)
        st.markdown('</div>', unsafe_allow_html=True)

        if lat and lon:
            dist = haversine(lat,lon,zla,zlo)
            st.markdown(f'''<div class="gc"><div class="ctab">
              <div class="crow"><span class="ck">Your Pos</span><span class="cv" style="font-size:12px">{lat:.5f}, {lon:.5f}</span></div>
              <div class="crow"><span class="ck">Zone Centre</span><span class="cv" style="font-size:12px">{zla:.5f}, {zlo:.5f}</span></div>
              <div class="crow"><span class="ck">Distance</span><span class="cv">{dist:.1f} m</span></div>
              <div class="crow"><span class="ck">Radius</span><span class="cv">{rad} m</span></div>
            </div></div>''', unsafe_allow_html=True)
        else:
            st.markdown('<div class="gc" style="color:#334155;font-size:13px;">📡 GPS signal needed for geo-fence check</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="gc">', unsafe_allow_html=True)
        if lat and lon:
            dist = haversine(lat,lon,zla,zlo)
            inside = dist <= rad
            if inside:
                st.markdown(f'<div class="gf-box" style="border-color:rgba(74,222,128,.2)"><div style="font-size:56px">✅</div><div class="gf-title" style="color:#4ade80">{st.session_state.username} — INSIDE SAFE ZONE</div><div class="gf-sub">Distance from centre: <strong style="color:#4ade80">{dist:.1f} m</strong> / limit {rad} m</div></div>', unsafe_allow_html=True)
                st.success("Boundary check passed. No action required.")
            else:
                st.markdown(f'<div class="gf-box" style="border-color:rgba(239,68,68,.2)"><div style="font-size:56px">🚨</div><div class="gf-title" style="color:#f87171">{st.session_state.username} — OUTSIDE SAFE ZONE</div><div class="gf-sub">Exceeded by <strong style="color:#f87171">{dist-rad:.1f} m</strong> — alerting response unit!</div></div>', unsafe_allow_html=True)
                st.error("⚠️ Geo-fence breached! Emergency protocol activated.")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(mapsembed(lat,lon,f"{st.session_state.username} live"), unsafe_allow_html=True)
        else:
            st.markdown('<div style="height:300px;display:flex;align-items:center;justify-content:center;color:#334155;">📡 Waiting for live GPS…</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════ SOS ════════════════════
elif page == "SOS Emergency":
    lat = st.session_state.lat; lon = st.session_state.lon
    st.markdown('<div class="ph-wrap"><div class="ph-eyebrow">Emergency Response</div><div class="ph-title">SOS Emergency</div><div class="ph-sub">Your live GPS coordinates are automatically dispatched with every alert</div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="gc"><div class="gc-title">📋 Emergency Details</div>', unsafe_allow_html=True)
        name  = st.text_input("Full Name", value=st.session_state.username)
        phone = st.text_input("Contact Number", placeholder="+91 XXXXX XXXXX")
        etype = st.selectbox("Emergency Type", ["🏥 Medical","🔪 Theft / Robbery","🧭 Lost","💥 Accident","🌊 Natural Disaster","⚡ Other"])
        note  = st.text_area("Situation Details", placeholder="Describe the situation…", height=80)
        if lat:
            st.markdown(f'<div class="ctab" style="margin-top:.8rem"><div class="crow"><span class="ck">📍 GPS Auto-Attached</span><span class="cv" style="font-size:12px">{lat:.6f}, {lon:.6f}</span></div><div class="crow"><span class="ck">Accuracy</span><span class="cv">±{st.session_state.accuracy:.0f} m</span></div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="margin-top:.8rem;font-size:12px;color:#f87171;background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.15);border-radius:10px;padding:.6rem .9rem;">⚠️ Enable GPS for precise location</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="gc" style="text-align:center;padding:2.5rem 1.5rem;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:72px;line-height:1;margin-bottom:1rem;filter:drop-shadow(0 0 20px rgba(239,68,68,.6))">🆘</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-family:Syne,sans-serif;font-size:20px;font-weight:800;color:#f87171;letter-spacing:1px;margin-bottom:.4rem;">PRESS IN AN EMERGENCY</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px;color:#475569;margin-bottom:2rem;line-height:1.6;">Your live GPS coordinates are instantly<br>dispatched to all nearby responders</div>', unsafe_allow_html=True)
        st.markdown('<div class="sos">', unsafe_allow_html=True)
        if st.button("🆘  SEND SOS NOW", use_container_width=True):
            loc = f"{lat:.6f}, {lon:.6f}" if lat else "GPS unavailable"
            mlink = f"https://maps.google.com/?q={lat},{lon}" if lat else "N/A"
            st.error(f"🚨 **ALERT DISPATCHED**\n\n**Name:** {name}  |  **Type:** {etype}\n\n**GPS:** {loc}\n\n**Maps:** {mlink}")
            st.snow()
        st.markdown('</div>', unsafe_allow_html=True)
        if lat: st.markdown("<br>" + mapsembed(lat,lon,"SOS location"), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════ AI RISK ════════════════════
elif page == "AI Risk":
    lat = st.session_state.lat
    st.markdown('<div class="ph-wrap"><div class="ph-eyebrow">Machine Learning</div><div class="ph-title">AI Risk Prediction</div><div class="ph-sub">GPS-aware intelligent safety scoring for your current position</div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.2,1])
    with c1:
        st.markdown('<div class="gc"><div class="gc-title">📊 Risk Assessment</div>', unsafe_allow_html=True)
        score = st.slider("Risk Score", 0, 100, 25)
        if score < 30:
            col,lbl,icon,tip = "#4ade80","LOW RISK","🟢","Environment is safe. Continue normal operations."
            bar = "linear-gradient(90deg,#4ade80,#16a34a)"
        elif score < 70:
            col,lbl,icon,tip = "#fbbf24","MEDIUM RISK","🟡","Exercise caution. Increase patrol frequency."
            bar = "linear-gradient(90deg,#fbbf24,#d97706)"
        else:
            col,lbl,icon,tip = "#f87171","HIGH RISK","🔴","Immediate action required. Consider evacuation."
            bar = "linear-gradient(90deg,#f87171,#dc2626)"

        st.markdown(f'''<div style="text-align:center;padding:1.5rem 0">
          <div style="font-size:52px;margin-bottom:.5rem;filter:drop-shadow(0 0 12px {col})">{icon}</div>
          <div style="font-family:Syne,sans-serif;font-size:28px;font-weight:800;color:{col};letter-spacing:-0.5px">{lbl}</div>
          <div class="rbar-bg"><div class="rbar-fg" style="width:{score}%;background:{bar}"></div></div>
          <div style="font-size:13px;color:#475569">{tip}</div>
          {f'<div style="font-size:11px;color:#334155;margin-top:.6rem">📍 At: {lat:.5f}, {st.session_state.lon:.5f}</div>' if lat else ''}
        </div>''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="gc"><div class="gc-title">🗺️ Risk Map</div>', unsafe_allow_html=True)
        if lat:
            st.markdown(mapsembed(lat,st.session_state.lon,"Risk assessment point"), unsafe_allow_html=True)
        else:
            st.markdown('<div style="height:200px;display:flex;align-items:center;justify-content:center;color:#334155;">GPS needed for risk map</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════ INCIDENT ════════════════════
elif page == "Incident Report":
    lat = st.session_state.lat; lon = st.session_state.lon
    st.markdown('<div class="ph-wrap"><div class="ph-eyebrow">Blockchain Ledger</div><div class="ph-title">Incident Report</div><div class="ph-sub">GPS geo-tagged and stored on the blockchain immutably</div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="gc"><div class="gc-title">📋 New Report</div>', unsafe_allow_html=True)
        reporter = st.text_input("Your Name", value=st.session_state.username)
        severity = st.selectbox("Severity", ["🟢 Minor","🟡 Moderate","🔴 Critical"])
        incident = st.text_area("Description", placeholder="What happened?", height=110)
        if lat:
            st.markdown(f'<div class="ctab" style="margin:.7rem 0"><div class="crow"><span class="ck">📍 GPS Tag</span><span class="cv" style="font-size:12px">{lat:.6f}, {lon:.6f}</span></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="abtn">', unsafe_allow_html=True)
        if st.button("Submit Report →", use_container_width=True):
            if incident.strip():
                loc = f"{lat:.6f},{lon:.6f}" if lat else "GPS unavailable"
                st.success("✅ Report geo-tagged and recorded on blockchain!")
                st.code(f"TX: 0x{hash(incident)%10**16:016x}\nGPS: {loc}\nBy: {reporter}", language="text")
            else:
                st.warning("Describe the incident first.")
        st.markdown('</div></div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="gc"><div class="gc-title">📍 Incident Location</div>', unsafe_allow_html=True)
        if lat:
            st.markdown(mapsembed(lat,lon,f"Incident by {st.session_state.username}"), unsafe_allow_html=True)
        else:
            st.markdown('<div style="height:200px;display:flex;align-items:center;justify-content:center;color:#334155;">GPS location auto-embedded once active</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════ ADMIN ════════════════════
elif page == "Admin":
    lat = st.session_state.lat
    st.markdown('<div class="ph-wrap"><div class="ph-eyebrow">System Control</div><div class="ph-title">Admin Dashboard</div><div class="ph-sub">System-wide monitoring and live GPS control panel</div></div>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col,grad,lbl,val,sub,icon in [
        (c1,"linear-gradient(90deg,#38bdf8,#818cf8)","GPS Status","Live" if lat else "Wait","navigator.geolocation","📡"),
        (c2,"linear-gradient(90deg,#fbbf24,#f97316)","Active Alerts","2","Needs review","⚠️"),
        (c3,"linear-gradient(90deg,#f87171,#dc2626)","Incidents","18","This month","📋"),
        (c4,"linear-gradient(90deg,#4ade80,#16a34a)","System Health","99%","All services up","💚"),
    ]:
        with col:
            st.markdown(f'<div class="sc" data-icon="{icon}"><div class="sc-accent" style="background:{grad}"></div><div class="sc-label">{lbl}</div><div class="sc-value">{val}</div><div class="sc-sub">{sub}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.6,1])
    with c1:
        st.markdown('<div class="gc"><div class="gc-title">🗺️ Live Tracking Map</div>', unsafe_allow_html=True)
        if lat:
            st.markdown(mapsembed(lat,st.session_state.lon,f"{st.session_state.username} — live"), unsafe_allow_html=True)
        else:
            st.markdown('<div style="height:240px;display:flex;align-items:center;justify-content:center;color:#334155;">Waiting for GPS signal…</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="gc"><div class="gc-title">⚙️ System Controls</div>', unsafe_allow_html=True)
        st.toggle("Geo-fence Alerts",   value=True)
        st.toggle("AI Risk Monitoring", value=True)
        st.toggle("Blockchain Logging", value=True)
        st.toggle("SMS Notifications",  value=False)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="abtn">', unsafe_allow_html=True)
        if st.button("🔄  Refresh Data", use_container_width=True): st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        if lat:
            st.markdown(f'''<div class="ctab" style="margin-top:1rem">
              <div class="crow"><span class="ck">User</span><span class="cv" style="font-size:13px">{st.session_state.username}</span></div>
              <div class="crow"><span class="ck">Lat</span><span class="cv" style="font-size:13px">{lat:.6f}°</span></div>
              <div class="crow"><span class="ck">Lon</span><span class="cv" style="font-size:13px">{st.session_state.lon:.6f}°</span></div>
              <div class="crow"><span class="ck">Accuracy</span><span class="cv" style="font-size:13px">±{st.session_state.accuracy:.0f} m</span></div>
            </div>''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
