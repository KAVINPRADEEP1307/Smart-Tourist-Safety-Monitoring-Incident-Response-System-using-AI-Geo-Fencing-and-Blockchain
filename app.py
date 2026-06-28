import streamlit as st
import streamlit.components.v1 as components
import math, random, time
from datetime import datetime

st.set_page_config(page_title="SafeTrail", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# ── Session State ─────────────────────────────────────────────────────────────
DEFAULTS = {
    "page": "Login", "logged_in": False, "username": "", "email": "",
    "lat": None, "lon": None, "accuracy": None, "gps_error": None, "gps_granted": False,
    "users": {"admin": {"password": "1234", "email": "admin@safetrail.com", "phone": "9800000000"}},
    "login_mode": "login", "lang": "English",
    "notifications": [
        {"icon": "⚠️", "msg": "High risk area detected near Zone B", "time": "2 min ago", "read": False},
        {"icon": "🌧️", "msg": "Heavy rain alert for your region", "time": "10 min ago", "read": False},
        {"icon": "🔋", "msg": "Device battery below 20%", "time": "25 min ago", "read": True},
    ],
    "incidents": [],
    "sos_contacts": [{"name": "Emergency Contact 1", "phone": "9800000001"}],
    "otp": None, "otp_verified": False, "otp_email": "",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k] = v

# ── Translations ──────────────────────────────────────────────────────────────
T = {
    "English": {
        "dashboard": "Dashboard", "geo": "Geo-Fencing", "sos": "SOS Emergency",
        "risk": "AI Risk", "incident": "Incident Report", "admin": "Admin",
        "login": "Login", "logout": "Logout", "nearby": "Nearby Help",
        "weather": "Weather Alerts", "notify": "Notifications",
        "welcome": "Welcome back", "safe": "SAFE", "danger": "DANGER",
        "send_sos": "SEND SOS NOW", "submit": "Submit Report",
        "download": "Download PDF", "signin": "Sign In", "register": "Register",
        "low_risk": "LOW RISK", "med_risk": "MEDIUM RISK", "high_risk": "HIGH RISK",
    },
    "Tamil": {
        "dashboard": "கட்டுப்பாட்டு பலகை", "geo": "புவி-வேலி", "sos": "அவசர SOS",
        "risk": "AI ஆபத்து", "incident": "சம்பவ அறிக்கை", "admin": "நிர்வாகி",
        "login": "உள்நுழைவு", "logout": "வெளியேறு", "nearby": "அருகில் உதவி",
        "weather": "வானிலை எச்சரிக்கை", "notify": "அறிவிப்புகள்",
        "welcome": "மீண்டும் வரவேற்கிறோம்", "safe": "பாதுகாப்பு", "danger": "ஆபத்து",
        "send_sos": "SOS அனுப்பு", "submit": "அறிக்கை சமர்ப்பி",
        "download": "PDF பதிவிறக்கம்", "signin": "உள்நுழை", "register": "பதிவு செய்",
        "low_risk": "குறைந்த ஆபத்து", "med_risk": "நடுத்தர ஆபத்து", "high_risk": "அதிக ஆபத்து",
    },
    "Hindi": {
        "dashboard": "डैशबोर्ड", "geo": "जियो-फेंसिंग", "sos": "SOS आपातकाल",
        "risk": "AI जोखिम", "incident": "घटना रिपोर्ट", "admin": "व्यवस्थापक",
        "login": "लॉगिन", "logout": "लॉगआउट", "nearby": "नजदीकी सहायता",
        "weather": "मौसम चेतावनी", "notify": "सूचनाएं",
        "welcome": "वापसी पर स्वागत", "safe": "सुरक्षित", "danger": "खतरा",
        "send_sos": "SOS भेजें", "submit": "रिपोर्ट सबमिट करें",
        "download": "PDF डाउनलोड", "signin": "साइन इन", "register": "पंजीकरण",
        "low_risk": "कम जोखिम", "med_risk": "मध्यम जोखिम", "high_risk": "उच्च जोखिम",
    }
}
def t(key): return T[st.session_state.lang].get(key, key)


# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; background: #f0f4ff; color: #1e293b; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ═══ APP BG ═══ */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 60% 40% at 15% 0%, rgba(30,90,255,0.07) 0%, transparent 55%),
        radial-gradient(ellipse 50% 35% at 85% 90%, rgba(16,185,129,0.06) 0%, transparent 55%),
        #f0f4ff;
}

/* ═══ SIDEBAR ═══ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8faff 0%, #f0f4ff 100%) !important;
    border-right: 1px solid rgba(30,90,255,0.12) !important;
    min-width: 240px !important; max-width: 240px !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }

.sb-logo {
    display: flex; align-items: center; gap: 10px;
    padding: 1.4rem 1.2rem 1rem;
    border-bottom: 1px solid rgba(30,90,255,0.08);
}
.sb-logo-icon {
    width: 36px; height: 36px; border-radius: 10px; flex-shrink: 0;
    background: linear-gradient(135deg, #1e5aff, #10b981);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    box-shadow: 0 0 16px rgba(30,90,255,0.4);
}
.sb-logo-text { font-family: 'Syne', sans-serif; font-size: 17px; font-weight: 800; color: #0f172a; letter-spacing: -0.3px; }
.sb-logo-sub { font-size: 9.5px; color: #94a3b8; letter-spacing: 1.5px; text-transform: uppercase; }

/* GPS live pill */
.gps-pill {
    margin: .8rem 1rem;
    padding: .45rem .9rem;
    border-radius: 30px; font-size: 11px; font-weight: 600;
    display: flex; align-items: center; gap: 7px;
    border: 1px solid;
}
.gps-pill.live  { background: rgba(16,185,129,.1);  border-color: rgba(16,185,129,.25); color: #10b981; }
.gps-pill.wait  { background: rgba(251,191,36,.08); border-color: rgba(251,191,36,.2);  color: #fbbf24; }
.gps-pill.err   { background: rgba(239,68,68,.08);  border-color: rgba(239,68,68,.2);   color: #f87171; }
.gps-dot { width:7px; height:7px; border-radius:50%; flex-shrink:0; }
.gps-dot.live { background:#10b981; box-shadow:0 0 6px #10b981; animation:blink 1.4s infinite; }
.gps-dot.wait { background:#fbbf24; }
.gps-dot.err  { background:#f87171; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.25} }

/* nav section */
.nav-sec { font-size: 9px; color: #64748b; text-transform: uppercase; letter-spacing: 2px; padding: .6rem 1.2rem .3rem; }

/* nav buttons */
.stButton > button {
    background: transparent !important; color: #64748b !important;
    border: none !important; border-radius: 10px !important;
    padding: .55rem 1rem !important; font-size: 13px !important;
    font-weight: 500 !important; text-align: left !important;
    width: 100% !important; transition: all .18s ease !important;
}
.stButton > button:hover { background: rgba(30,90,255,0.07) !important; color: #1e5aff !important; transform: translateX(2px) !important; }
.nav-active > .stButton > button {
    background: linear-gradient(90deg, rgba(30,90,255,0.1), rgba(16,185,129,0.05)) !important;
    color: #1e5aff !important; border-left: 2px solid #1e5aff !important; font-weight: 700 !important;
}

/* lang select in sidebar */
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 8px !important; color: #475569 !important; font-size: 12px !important;
}

/* ═══ TOPBAR ═══ */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 2rem;
    background: rgba(255,255,255,0.92);
    border-bottom: 1px solid rgba(30,90,255,0.1);
    backdrop-filter: blur(12px);
    position: sticky; top: 0; z-index: 100;
}
.topbar-left { display: flex; align-items: center; gap: 10px; }
.topbar-logo {
    width: 32px; height: 32px; border-radius: 8px;
    background: linear-gradient(135deg, #1e5aff, #10b981);
    display: flex; align-items: center; justify-content: center; font-size: 16px;
    box-shadow: 0 0 12px rgba(30,90,255,0.35);
}
.topbar-title { font-family: 'Syne', sans-serif; font-size: 17px; font-weight: 800; color: #fff; }
.topbar-right { display: flex; align-items: center; gap: 12px; }
.notif-badge {
    position: relative; cursor: pointer;
    width: 34px; height: 34px; border-radius: 10px;
    background: rgba(255,255,255,0.05); border: 1px solid rgba(30,90,255,0.12);
    display: flex; align-items: center; justify-content: center; font-size: 15px;
}
.notif-count {
    position: absolute; top: -4px; right: -4px;
    background: #ef4444; color: #fff; font-size: 9px; font-weight: 700;
    width: 16px; height: 16px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
}
.profile-chip {
    display: flex; align-items: center; gap: 8px;
    background: rgba(30,90,255,0.1); border: 1px solid rgba(30,90,255,0.2);
    border-radius: 20px; padding: .3rem .8rem .3rem .4rem;
}
.profile-avatar {
    width: 26px; height: 26px; border-radius: 50%;
    background: linear-gradient(135deg, #1e5aff, #10b981);
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 700; color: #fff;
}
.profile-name { font-size: 12px; font-weight: 600; color: #7aa2ff; }

/* ═══ PAGE CONTENT ═══ */
.main-content { padding: 1.8rem 2rem; }

/* ═══ PAGE HEADER ═══ */
.ph { margin-bottom: 1.8rem; }
.ph-eye { font-size: 10.5px; text-transform: uppercase; letter-spacing: 3px; color: #1e5aff; font-weight: 700; margin-bottom: .4rem; }
.ph-title { font-family: 'Syne', sans-serif; font-size: 32px; font-weight: 800; color: #0f172a; letter-spacing: -1px; line-height: 1.1; }
.ph-title span { background: linear-gradient(90deg, #5b9aff, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.ph-sub { font-size: 13px; color: #64748b; margin-top: .4rem; }

/* ═══ GLASS CARDS ═══ */
.card {
    background: #ffffff;
    border: 1px solid rgba(30,90,255,0.1);
    border-radius: 18px; padding: 1.5rem;
    position: relative; overflow: hidden;
    margin-bottom: 1rem;
    box-shadow: 0 2px 16px rgba(30,90,255,0.06);
}
.card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #1e5aff, #10b981);
}
.card-title { font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: #94a3b8; font-weight: 700; margin-bottom: 1rem; }

/* ═══ STAT CARDS ═══ */
.stat {
    background: #ffffff;
    border: 1px solid rgba(30,90,255,0.1);
    border-radius: 16px; padding: 1.3rem 1.5rem;
    position: relative; overflow: hidden;
    box-shadow: 0 2px 12px rgba(30,90,255,0.06);
}
.stat-bar { height: 2px; border-radius: 2px; margin-bottom: 1rem; }
.stat-icon { position: absolute; right: 1rem; top: 1rem; font-size: 28px; opacity: .12; }
.stat-label { font-size: 10px; text-transform: uppercase; letter-spacing: 2px; color: #94a3b8; margin-bottom: .35rem; }
.stat-val { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; color: #0f172a; line-height: 1; }
.stat-sub { font-size: 11px; color: #94a3b8; margin-top: .35rem; }

/* ═══ INPUTS ═══ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: #f8faff !important;
    border: 1px solid rgba(30,90,255,0.15) !important;
    border-radius: 11px !important; color: #1e293b !important;
    font-size: 13.5px !important; padding: .7rem 1rem !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(30,90,255,0.6) !important;
    box-shadow: 0 0 0 3px rgba(30,90,255,0.12) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label, .stNumberInput label {
    color: #2d4a70 !important; font-size: 11px !important;
    font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 1px !important;
}
.stSelectbox > div > div {
    background: #f8faff !important;
    border: 1px solid rgba(30,90,255,0.15) !important;
    border-radius: 11px !important; color: #1e293b !important;
}

/* ═══ PRIMARY BUTTON ═══ */
.pbtn .stButton > button {
    background: linear-gradient(135deg, #1e5aff, #0d3dbf) !important;
    color: #fff !important; border: none !important; border-radius: 11px !important;
    padding: .72rem 1.8rem !important; font-weight: 700 !important; font-size: 13.5px !important;
    text-align: center !important; letter-spacing: .2px !important;
    box-shadow: 0 4px 20px rgba(30,90,255,0.35) !important; transition: all .2s !important;
}
.pbtn .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 28px rgba(30,90,255,0.5) !important; }

/* Green button */
.gbtn .stButton > button {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    color: #fff !important; border: none !important; border-radius: 11px !important;
    padding: .72rem 1.8rem !important; font-weight: 700 !important; font-size: 13.5px !important;
    text-align: center !important; box-shadow: 0 4px 20px rgba(16,185,129,0.35) !important;
}

/* SOS */
.sosbtn .stButton > button {
    background: linear-gradient(135deg, #dc2626, #991b1b) !important;
    color: #fff !important; border: none !important; border-radius: 999px !important;
    padding: 1.1rem 2.5rem !important; font-weight: 800 !important; font-size: 17px !important;
    letter-spacing: 1px !important; animation: sosglow 2s infinite !important;
}
@keyframes sosglow {
    0%,100% { box-shadow: 0 0 20px rgba(220,38,38,0.5), 0 0 0 0 rgba(220,38,38,0.4); }
    50%      { box-shadow: 0 0 40px rgba(220,38,38,0.7), 0 0 0 14px rgba(220,38,38,0); }
}

/* logout button */
.lbtn .stButton > button {
    background: rgba(239,68,68,0.1) !important; color: #f87171 !important;
    border: 1px solid rgba(239,68,68,0.2) !important; border-radius: 8px !important;
    padding: .4rem .9rem !important; font-size: 12px !important; font-weight: 600 !important;
}

/* ═══ COORD BOX ═══ */
.cbox { background: #f1f5f9; border: 1px solid rgba(30,90,255,0.15); border-radius: 12px; overflow: hidden; }
.crow { display: flex; justify-content: space-between; align-items: center; padding: .65rem 1rem; border-bottom: 1px solid #e2e8f0; }
.crow:last-child { border-bottom: none; }
.ck { font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: #64748b; }
.cv { font-family: 'Syne', sans-serif; font-size: 13.5px; font-weight: 700; color: #5b9aff; }

/* ═══ RISK BAR ═══ */
.rbar-bg { background: rgba(255,255,255,0.06); border-radius: 99px; height: 10px; margin: .8rem 0; overflow: hidden; }
.rbar-fill { height: 10px; border-radius: 99px; transition: width .5s ease; }

/* ═══ NOTIF PANEL ═══ */
.notif-item {
    display: flex; gap: 12px; padding: .9rem 1rem;
    border-bottom: 1px solid #e2e8f0;
    background: #f8faff; border-radius: 10px; margin-bottom: 6px;
}
.notif-item.unread { background: rgba(30,90,255,0.07); border: 1px solid rgba(30,90,255,0.12); }
.notif-icon { font-size: 20px; flex-shrink: 0; }
.notif-msg { font-size: 13px; color: #94a3b8; line-height: 1.4; }
.notif-time { font-size: 11px; color: #64748b; margin-top: 2px; }

/* ═══ INCIDENT HISTORY ═══ */
.inc-row {
    display: flex; align-items: center; gap: 12px;
    padding: .8rem 1rem; border-radius: 10px; margin-bottom: 5px;
    background: #f8faff; border: 1px solid rgba(30,90,255,0.08);
}
.inc-icon { font-size: 18px; }
.inc-title { font-size: 13px; color: #94a3b8; font-weight: 600; }
.inc-sub { font-size: 11px; color: #64748b; }

/* ═══ QUICK CALL CARD ═══ */
.qcall {
    display: flex; align-items: center; justify-content: space-between;
    padding: .9rem 1.1rem; border-radius: 12px; margin-bottom: .5rem;
    border: 1px solid rgba(30,90,255,0.1); background: #f8faff;
    transition: border-color .2s;
}
.qcall:hover { border-color: rgba(30,90,255,0.3); }
.qcall-left { display: flex; align-items: center; gap: 10px; }
.qcall-icon { font-size: 22px; }
.qcall-name { font-size: 13px; color: #94a3b8; font-weight: 600; }
.qcall-num  { font-size: 11px; color: #64748b; }
.qcall-btn {
    background: linear-gradient(135deg, #1e5aff, #10b981);
    color: #fff; border: none; border-radius: 8px; padding: .4rem .9rem;
    font-size: 12px; font-weight: 700; cursor: pointer; text-decoration: none;
}

/* ═══ WEATHER CARD ═══ */
.wx-card {
    border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: .5rem;
    border: 1px solid; display: flex; align-items: center; gap: 12px;
}
.wx-card.warn { background: rgba(251,191,36,.07); border-color: rgba(251,191,36,.2); }
.wx-card.danger{ background: rgba(239,68,68,.07); border-color: rgba(239,68,68,.2); }
.wx-card.ok   { background: rgba(16,185,129,.07); border-color: rgba(16,185,129,.2); }
.wx-icon { font-size: 28px; }
.wx-title { font-size: 13px; font-weight: 700; color: #0f172a; }
.wx-sub { font-size: 11.5px; color: #64748b; }

/* ═══ STATUS BADGES ═══ */
.badge { display:inline-block; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:700; letter-spacing:.5px; }
.badge.safe { background:rgba(16,185,129,.15); color:#10b981; border:1px solid rgba(16,185,129,.25); }
.badge.warn { background:rgba(251,191,36,.15); color:#fbbf24; border:1px solid rgba(251,191,36,.25); }
.badge.danger{ background:rgba(239,68,68,.15); color:#f87171; border:1px solid rgba(239,68,68,.25); }

/* ═══ LOGIN ═══ */
.login-bg {
    min-height: 92vh; display: flex; align-items: center; justify-content: center;
}
.login-card {
    background: #ffffff;
    border: 1px solid rgba(30,90,255,0.12);
    border-radius: 24px; padding: 2.5rem 2.2rem;
    width: 100%; max-width: 420px; position: relative; overflow: hidden;
}
.login-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(30,90,255,0.6), rgba(16,185,129,0.5), transparent);
}
.login-brand { text-align: center; margin-bottom: 2rem; }
.login-icon {
    width: 72px; height: 72px; border-radius: 20px; margin: 0 auto 1rem;
    background: linear-gradient(135deg, #1e5aff, #10b981);
    display: flex; align-items: center; justify-content: center; font-size: 32px;
    box-shadow: 0 0 40px rgba(30,90,255,0.45), 0 0 80px rgba(30,90,255,0.15);
}
.login-title { font-family:'Syne',sans-serif; font-size:28px; font-weight:800; color:#fff; letter-spacing:-1px; }
.login-sub { font-size:13px; color:#2d4a70; margin-top:.3rem; }
.tab-row { display:flex; gap:8px; margin-bottom:1.5rem; }
.tab-btn { flex:1; padding:.55rem; border-radius:9px; border:1px solid rgba(255,255,255,0.08); background:transparent; color:#4a6080; font-size:13px; font-weight:600; cursor:pointer; transition:all .18s; text-align:center; }
.tab-btn.active { background:rgba(30,90,255,0.2); border-color:rgba(30,90,255,0.4); color:#7aa2ff; }

/* ═══ GEO FENCE STATUS ═══ */
.gf-status { text-align:center; padding:2rem 1rem; border-radius:16px; }

/* table */
[data-testid="stTable"] th { background:rgba(30,90,255,0.1)!important; color:#5b9aff!important; font-size:11px!important; text-transform:uppercase!important; letter-spacing:1px!important; }
[data-testid="stTable"] td { background:rgba(255,255,255,0.02)!important; color:#94a3b8!important; font-size:13px!important; }

/* alerts */
.stAlert { border-radius: 12px !important; }

/* slider */
[data-testid="stSlider"] { padding: 0 !important; }

/* toggle - deep selectors for Streamlit internals */
.stToggle,
[data-testid="stToggle"],
div[data-testid="stToggle"],
.stCheckbox,
[data-testid="stCheckbox"] {
    background: #ffffff !important;
    border-radius: 10px !important;
    padding: .45rem .7rem !important;
    margin-bottom: 4px !important;
}
.stToggle label,
.stToggle label p,
.stToggle label span,
.stToggle > label,
.stToggle > div > label,
[data-testid="stToggle"] label,
[data-testid="stToggle"] label p,
[data-testid="stToggle"] label span,
[data-testid="stToggle"] p,
[data-testid="stToggle"] span,
div[data-testid="stToggle"] p,
div[data-testid="stToggle"] span,
div[data-testid="stToggle"] label {
    color: #000000 !important;
    font-size: 13.5px !important;
    font-weight: 700 !important;
}
/* catch all p tags inside toggles */
.stToggle p { color: #000000 !important; font-weight: 700 !important; font-size: 13.5px !important; }
div[class*="toggle"] p, div[class*="Toggle"] p { color: #000000 !important; font-weight: 700 !important; }

.divline { height:1px; background:linear-gradient(90deg,transparent,rgba(30,90,255,0.15),transparent); margin:.6rem 0; }
</style>
""", unsafe_allow_html=True)


# ── GPS JS ────────────────────────────────────────────────────────────────────
GPS_HTML = """
<div id="gs" style="font-size:10px;color:#1e3a5f;font-family:monospace;padding:1px 0;"></div>
<script>
(function(){
  var s=document.getElementById('gs');
  if(!navigator.geolocation){s.textContent='GPS not supported';return;}
  s.textContent='Requesting GPS...';
  navigator.geolocation.watchPosition(function(p){
    var la=p.coords.latitude,lo=p.coords.longitude,ac=p.coords.accuracy;
    s.textContent='GPS '+la.toFixed(5)+', '+lo.toFixed(5)+' ±'+Math.round(ac)+'m';
    var u=new URL(window.parent.location.href);
    u.searchParams.set('gps_lat',la.toFixed(7));
    u.searchParams.set('gps_lon',lo.toFixed(7));
    u.searchParams.set('gps_acc',Math.round(ac));
    window.parent.history.replaceState(null,'',u.toString());
  },function(e){
    var u=new URL(window.parent.location.href);
    u.searchParams.set('gps_error',e.message);
    window.parent.history.replaceState(null,'',u.toString());
  },{enableHighAccuracy:true,timeout:15000,maximumAge:0});
})();
</script>
"""

# ── GPS from query params ────────────────────────────────────────────────────
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

# ── Helpers ──────────────────────────────────────────────────────────────────
def haversine(la1,lo1,la2,lo2):
    R=6371000; f1,f2=math.radians(la1),math.radians(la2)
    dp=math.radians(la2-la1); dl=math.radians(lo2-lo1)
    a=math.sin(dp/2)**2+math.cos(f1)*math.cos(f2)*math.sin(dl/2)**2
    return R*2*math.atan2(math.sqrt(a),math.sqrt(1-a))

def map_embed(lat,lon,label=""):
    return f'<iframe width="100%" height="300" style="border:0;border-radius:14px;" loading="lazy" src="https://maps.google.com/maps?q={lat},{lon}&z=16&output=embed"></iframe><div style="font-size:11px;color:#64748b;text-align:center;margin-top:.3rem">📍 {label} {lat:.6f}, {lon:.6f}</div>'

def stat_card(col, bar_color, icon, label, value, sub):
    with col:
        st.markdown(f'<div class="stat"><div class="stat-bar" style="background:{bar_color}"></div><div class="stat-icon">{icon}</div><div class="stat-label">{label}</div><div class="stat-val">{value}</div><div class="stat-sub">{sub}</div></div>', unsafe_allow_html=True)

def generate_otp():
    return str(random.randint(100000, 999999))

# ── PDF Generator ─────────────────────────────────────────────────────────────
def make_pdf_report(username, lat, lon, incidents):
    lines = [
        "SafeTrail – Incident Report",
        "=" * 40,
        f"User: {username}",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"GPS: {lat:.6f}, {lon:.6f}" if lat else "GPS: Not available",
        "",
        "INCIDENTS:",
        "-" * 40,
    ]
    if incidents:
        for i, inc in enumerate(incidents, 1):
            lines += [f"{i}. [{inc['severity']}] {inc['desc']}", f"   Location: {inc.get('gps','N/A')}", f"   Time: {inc['time']}", ""]
    else:
        lines.append("No incidents recorded.")
    return "\n".join(lines)


# ── NAV ITEMS ─────────────────────────────────────────────────────────────────
nav_items = [
    ("📡", "Dashboard"),("📍", "Geo-Fencing"),("🆘", "SOS Emergency"),
    ("🤖", "AI Risk"),("📋", "Incident Report"),("🔔", "Notifications"),
    ("🏥", "Nearby Help"),("⚙️", "Admin"),
]

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('''<div class="sb-logo">
      <div class="sb-logo-icon">🛡️</div>
      <div><div class="sb-logo-text">SafeTrail</div><div class="sb-logo-sub">Safety System</div></div>
    </div>''', unsafe_allow_html=True)

    lat = st.session_state.lat
    if st.session_state.gps_error:
        st.markdown('<div class="gps-pill err"><div class="gps-dot err"></div>GPS Error</div>', unsafe_allow_html=True)
    elif lat:
        st.markdown(f'<div class="gps-pill live"><div class="gps-dot live"></div>GPS Live · ±{st.session_state.accuracy:.0f}m</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="gps-pill wait"><div class="gps-dot wait"></div>Waiting for GPS…</div>', unsafe_allow_html=True)

    # Language selector
    lang_choice = st.selectbox("", ["English","Tamil","Hindi"], index=["English","Tamil","Hindi"].index(st.session_state.lang), key="lang_sel", label_visibility="collapsed")
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice; st.rerun()

    st.markdown('<div class="divline"></div>', unsafe_allow_html=True)

    if st.session_state.logged_in:
        st.markdown('<div class="nav-sec">MAIN MENU</div>', unsafe_allow_html=True)
        unread = sum(1 for n in st.session_state.notifications if not n["read"])
        for icon, label in nav_items:
            badge = f" 🔴{unread}" if label == "Notifications" and unread else ""
            active = st.session_state.page == label
            if active: st.markdown('<div class="nav-active">', unsafe_allow_html=True)
            if st.button(f"{icon}  {label}{badge}", key=f"n_{label}", use_container_width=True):
                st.session_state.page = label; st.rerun()
            if active: st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="nav-sec">ACCOUNT</div>', unsafe_allow_html=True)
        if st.button("🔐  Login", key="n_Login", use_container_width=True):
            st.session_state.page = "Login"; st.rerun()

    st.markdown('<div class="divline"></div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;font-size:10px;color:#0f2040;padding:.3rem">© 2025 SafeTrail Inc.</div>', unsafe_allow_html=True)

# Inject GPS collector
components.html(GPS_HTML, height=16)

page = st.session_state.page

# ── TOP BAR (when logged in) ──────────────────────────────────────────────────
if st.session_state.logged_in:
    unread = sum(1 for n in st.session_state.notifications if not n["read"])
    uname  = st.session_state.username
    init   = uname[0].upper() if uname else "U"
    tb_c1, tb_c2, tb_c3, tb_c4 = st.columns([3, 1, 1, 1])
    with tb_c1:
        st.markdown(f'<div style="padding:.6rem 0"><span style="font-size:20px;font-family:Syne,sans-serif;font-weight:800;color:#0f172a;">🛡️ SafeTrail</span><span style="font-size:11px;color:#94a3b8;margin-left:10px;">/ {page}</span></div>', unsafe_allow_html=True)
    with tb_c2:
        # Language quick toggle shown in topbar too
        st.markdown(f'<div style="padding:.5rem 0;text-align:right;font-size:11px;color:#2d4a70">🌐 {st.session_state.lang}</div>', unsafe_allow_html=True)
    with tb_c3:
        notif_label = f"🔔 ({unread})" if unread else "🔔"
        if st.button(notif_label, key="topbar_notif"):
            st.session_state.page = "Notifications"; st.rerun()
    with tb_c4:
        st.markdown('<div class="lbtn">', unsafe_allow_html=True)
        if st.button("⬡ Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.username  = ""
            st.session_state.page      = "Login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="divline"></div>', unsafe_allow_html=True)

st.markdown('<div class="main-content">', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
if page == "Login":
    _, col, _ = st.columns([1, 1.05, 1])
    with col:
        st.markdown('<div class="login-bg"><div>', unsafe_allow_html=True)
        st.markdown('''<div class="login-card">
          <div class="login-brand">
            <div class="login-icon">🛡️</div>
            <div class="login-title">SafeTrail</div>
            <div class="login-sub">Intelligent Tourist Safety Platform</div>
          </div>''', unsafe_allow_html=True)

        # Tabs via HTML + session state
        mode = st.session_state.login_mode
        st.markdown(f'''<div class="tab-row">
          <button class="tab-btn {'active' if mode=='login' else ''}" onclick="void(0)"
            style="pointer-events:none">🔐 Login</button>
          <button class="tab-btn {'active' if mode=='register' else ''}" onclick="void(0)"
            style="pointer-events:none">📝 Register</button>
        </div>''', unsafe_allow_html=True)
        tl, tr = st.columns(2)
        with tl:
            if st.button("🔐 Login", use_container_width=True, key="sw_login"):
                st.session_state.login_mode = "login"; st.rerun()
        with tr:
            if st.button("📝 Register", use_container_width=True, key="sw_reg"):
                st.session_state.login_mode = "register"; st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if mode == "login":
            lu = st.text_input("Username", placeholder="Enter username", key="lu")
            lp = st.text_input("Password", type="password", placeholder="••••••••", key="lp")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="pbtn">', unsafe_allow_html=True)
            if st.button(f"  {t('signin')}  →", use_container_width=True, key="do_login"):
                if not lu or not lp:
                    st.error("Username மற்றும் Password போடுங்க!")
                elif lu in st.session_state.users and st.session_state.users[lu]["password"] == lp:
                    st.session_state.logged_in = True
                    st.session_state.username  = lu
                    st.session_state.email     = st.session_state.users[lu].get("email","")
                    st.session_state.page      = "Dashboard"
                    st.rerun()
                else:
                    st.error("❌ Wrong username or password!")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div style="text-align:center;margin-top:1rem;font-size:11.5px;color:#1e3a5f">Default: <code style="color:#5b9aff">admin</code> / <code style="color:#5b9aff">1234</code></div>', unsafe_allow_html=True)

        else:
            ru  = st.text_input("Username",        placeholder="Choose a username",  key="ru")
            re  = st.text_input("Email",            placeholder="your@email.com",     key="re")
            rph = st.text_input("Phone",            placeholder="+91 XXXXX XXXXX",    key="rph")
            rp  = st.text_input("Password",         type="password", placeholder="Min 4 chars", key="rp")
            rp2 = st.text_input("Confirm Password", type="password", placeholder="••••••••",    key="rp2")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="gbtn">', unsafe_allow_html=True)
            if st.button(f"  {t('register')}  →", use_container_width=True, key="do_reg"):
                if not ru or not rp:
                    st.error("❌ Username மற்றும் Password கட்டாயம்!")
                elif rp != rp2:
                    st.error("❌ Passwords match ஆகல!")
                elif len(rp) < 4:
                    st.error("❌ Password குறைஞ்சது 4 characters!")
                elif ru in st.session_state.users:
                    st.error("❌ Username already உள்ளது!")
                else:
                    st.session_state.users[ru] = {"password": rp, "email": re, "phone": rph}
                    st.session_state.logged_in = True
                    st.session_state.username  = ru
                    st.session_state.email     = re
                    st.session_state.page      = "Dashboard"
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        if not st.session_state.gps_granted:
            st.markdown('<div style="text-align:center;margin-top:.8rem;font-size:12px;color:#64748b;border:1px solid rgba(30,90,255,.15);border-radius:10px;padding:.7rem;background:rgba(30,90,255,.04)">📡 Allow location access for GPS tracking</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Dashboard":
    lat = st.session_state.lat; lon = st.session_state.lon; acc = st.session_state.accuracy
    uname = st.session_state.username
    st.markdown(f'<div class="ph"><div class="ph-eye">Live Monitoring</div><div class="ph-title">{t("welcome")}, <span>{uname}</span> 👋</div><div class="ph-sub">Real-time GPS safety dashboard • {datetime.now().strftime("%d %b %Y, %I:%M %p")}</div></div>', unsafe_allow_html=True)

    # ── Stat row ──
    c1,c2,c3,c4 = st.columns(4)
    stat_card(c1,"linear-gradient(90deg,#1e5aff,#5b9aff)","👥","Total Users",str(len(st.session_state.users)),"Registered")
    stat_card(c2,"linear-gradient(90deg,#ef4444,#f87171)","🆘","Active SOS","0","No active alerts")
    stat_card(c3,"linear-gradient(90deg,#fbbf24,#f97316)","⚠️","High Risk Areas","1","Zone B flagged")
    stat_card(c4,"linear-gradient(90deg,#10b981,#34d399)","📍","GPS Status","Live" if lat else "Waiting","navigator.geolocation")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.7, 1])
    with c1:
        # Map
        st.markdown('<div class="card"><div class="card-title">📍 Your Live Location</div>', unsafe_allow_html=True)
        if lat and lon:
            st.markdown(map_embed(lat,lon,f"{uname} —"), unsafe_allow_html=True)
        else:
            st.markdown('<div style="height:200px;display:flex;align-items:center;justify-content:center;color:#64748b;font-size:13px;flex-direction:column;gap:8px"><div style="font-size:36px">📡</div>Allow location access in your browser</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Recent incidents
        st.markdown('<div class="card"><div class="card-title">🕒 Recent Incident History</div>', unsafe_allow_html=True)
        if st.session_state.incidents:
            for inc in st.session_state.incidents[-4:][::-1]:
                sev = inc['severity']
                col_s = "#10b981" if "Minor" in sev else "#fbbf24" if "Moderate" in sev else "#f87171"
                st.markdown(f'<div class="inc-row"><div class="inc-icon">📋</div><div><div class="inc-title">{inc["desc"][:50]}…</div><div class="inc-sub">{inc["time"]} · <span style="color:{col_s}">{sev}</span> · {inc.get("gps","N/A")}</div></div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#64748b;font-size:13px;padding:.5rem">No incidents recorded yet.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        # Coordinates
        st.markdown('<div class="card"><div class="card-title">📐 Your Coordinates</div>', unsafe_allow_html=True)
        if lat:
            st.markdown(f'''<div class="cbox">
              <div class="crow"><span class="ck" style="color:#64748b">Latitude</span><span class="cv">{lat:.7f}°</span></div>
              <div class="crow"><span class="ck" style="color:#64748b">Longitude</span><span class="cv">{lon:.7f}°</span></div>
              <div class="crow"><span class="ck" style="color:#64748b">Accuracy</span><span class="cv">±{acc:.0f} m</span></div>
              <div class="crow"><span class="ck" style="color:#64748b">User</span><span class="cv">{uname}</span></div>
            </div>
            <a href="https://www.google.com/maps?q={lat},{lon}" target="_blank" style="display:block;margin-top:.8rem;text-align:center;font-size:12px;color:#5b9aff;padding:.5rem;background:rgba(30,90,255,.08);border-radius:9px;border:1px solid rgba(30,90,255,.15);text-decoration:none">🔗 Open in Google Maps ↗</a>''', unsafe_allow_html=True)
        else:
            st.info("📡 GPS will appear here once active.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Weather warnings
        st.markdown('<div class="card"><div class="card-title">🌦️ Weather Alerts</div>', unsafe_allow_html=True)
        st.markdown('''
        <div class="wx-card danger"><div class="wx-icon">🌀</div><div><div class="wx-title">Cyclone Warning</div><div class="wx-sub">Category 1 — 120 km away</div></div></div>
        <div class="wx-card warn"><div class="wx-icon">🌧️</div><div><div class="wx-title">Heavy Rain Alert</div><div class="wx-sub">Expected 4 PM – 10 PM today</div></div></div>
        <div class="wx-card ok"><div class="wx-icon">🌤️</div><div><div class="wx-title">Morning Clear</div><div class="wx-sub">Safe conditions until noon</div></div></div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Device status
        st.markdown('<div class="card"><div class="card-title">📱 Device Status</div>', unsafe_allow_html=True)
        st.markdown('''<div class="cbox">
          <div class="crow"><span class="ck" style="color:#64748b">🔋 Battery</span><span class="cv" style="color:#f87171">18% ⚠️</span></div>
          <div class="crow"><span class="ck" style="color:#64748b">📶 Network</span><span class="cv" style="color:#10b981">4G Strong</span></div>
          <div class="crow"><span class="ck" style="color:#64748b">📡 GPS</span><span class="cv" style="color:#10b981">Active</span></div>
        </div>''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# GEO-FENCING
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Geo-Fencing":
    lat = st.session_state.lat; lon = st.session_state.lon
    st.markdown(f'<div class="ph"><div class="ph-eye">Boundary Detection</div><div class="ph-title">{t("geo")}</div><div class="ph-sub">Your live GPS is checked against the safe zone in real-time</div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1.6])
    with c1:
        st.markdown('<div class="card"><div class="card-title">⚙️ Zone Settings</div>', unsafe_allow_html=True)
        zla = st.number_input("Zone Centre Latitude",  value=lat if lat else 13.0827, format="%.6f", step=0.0001)
        zlo = st.number_input("Zone Centre Longitude", value=lon if lon else 80.2707, format="%.6f", step=0.0001)
        rad = st.slider("Safe Radius (metres)", 50, 5000, 500, step=50)
        st.markdown('</div>', unsafe_allow_html=True)

        if lat and lon:
            dist = haversine(lat,lon,zla,zlo)
            st.markdown(f'''<div class="card"><div class="cbox">
              <div class="crow"><span class="ck" style="color:#64748b">Your Position</span><span class="cv" style="font-size:12px">{lat:.5f}, {lon:.5f}</span></div>
              <div class="crow"><span class="ck" style="color:#64748b">Zone Centre</span><span class="cv" style="font-size:12px">{zla:.5f}, {zlo:.5f}</span></div>
              <div class="crow"><span class="ck" style="color:#64748b">Distance</span><span class="cv">{dist:.1f} m</span></div>
              <div class="crow"><span class="ck" style="color:#64748b">Radius Limit</span><span class="cv">{rad} m</span></div>
            </div></div>''', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if lat and lon:
            dist = haversine(lat,lon,zla,zlo)
            inside = dist <= rad
            if inside:
                st.markdown(f'<div class="gf-status" style="border:1px solid rgba(16,185,129,.2);background:rgba(16,185,129,.05)"><div style="font-size:54px">✅</div><div style="font-family:Syne,sans-serif;font-size:22px;font-weight:800;color:#10b981;margin:.5rem 0">{st.session_state.username} — {t("safe")}</div><div style="color:#64748b;font-size:13px">Distance: <strong style="color:#10b981">{dist:.1f} m</strong> within {rad} m limit</div></div>', unsafe_allow_html=True)
                st.success("✅ Boundary check passed.")
            else:
                st.markdown(f'<div class="gf-status" style="border:1px solid rgba(239,68,68,.2);background:rgba(239,68,68,.05)"><div style="font-size:54px">🚨</div><div style="font-family:Syne,sans-serif;font-size:22px;font-weight:800;color:#f87171;margin:.5rem 0">{st.session_state.username} — {t("danger")}</div><div style="color:#64748b;font-size:13px">Exceeded by <strong style="color:#f87171">{dist-rad:.1f} m</strong> — response unit alerted!</div></div>', unsafe_allow_html=True)
                st.error("⚠️ Geo-fence breach! Emergency protocol activated.")
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(map_embed(lat, lon, st.session_state.username), unsafe_allow_html=True)
        else:
            st.markdown('<div style="height:280px;display:flex;align-items:center;justify-content:center;color:#64748b;flex-direction:column;gap:8px"><div style="font-size:36px">📡</div>Waiting for live GPS signal…</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SOS EMERGENCY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "SOS Emergency":
    lat = st.session_state.lat; lon = st.session_state.lon
    st.markdown(f'<div class="ph"><div class="ph-eye">Emergency Response</div><div class="ph-title">{t("sos")}</div><div class="ph-sub">Live GPS auto-dispatched with every alert</div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><div class="card-title">📋 Emergency Details</div>', unsafe_allow_html=True)
        name  = st.text_input("Full Name", value=st.session_state.username)
        phone = st.text_input("Contact Number", placeholder="+91 XXXXX XXXXX")
        etype = st.selectbox("Emergency Type", ["🏥 Medical","🔪 Theft / Robbery","🧭 Lost","💥 Accident","🌊 Natural Disaster","⚡ Other"])
        note  = st.text_area("Situation Details", placeholder="Describe briefly…", height=70)

        if lat:
            st.markdown(f'<div class="cbox" style="margin-top:.7rem"><div class="crow"><span class="ck" style="color:#64748b">📍 GPS Auto-Attached</span><span class="cv" style="font-size:12px">{lat:.6f}, {lon:.6f}</span></div><div class="crow"><span class="ck" style="color:#64748b">Accuracy</span><span class="cv">±{st.session_state.accuracy:.0f} m</span></div></div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Enable GPS for precise location tracking")

        # Quick call buttons
        st.markdown('<div style="margin-top:1rem"><div class="card-title">📞 Quick Call</div>', unsafe_allow_html=True)
        calls = [("🚔","Police","100"),("🚑","Ambulance","108"),("🚒","Fire","101"),("🆘","Tourist Helpline","1800-111-363")]
        for icon, name_c, num in calls:
            st.markdown(f'''<div class="qcall">
              <div class="qcall-left"><div class="qcall-icon">{icon}</div><div><div class="qcall-name">{name_c}</div><div class="qcall-num">{num}</div></div></div>
              <a href="tel:{num}" class="qcall-btn">📞 Call</a>
            </div>''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card" style="text-align:center;padding:2.5rem 1.5rem">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:72px;line-height:1;margin-bottom:.8rem;filter:drop-shadow(0 0 24px rgba(220,38,38,.7))">🆘</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-family:Syne,sans-serif;font-size:20px;font-weight:800;color:#f87171;letter-spacing:1px;margin-bottom:.3rem">PRESS IN AN EMERGENCY</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:12px;color:#2d4a70;margin-bottom:2rem;line-height:1.6">Your live GPS coordinates are instantly<br>dispatched to all nearby responders</div>', unsafe_allow_html=True)
        st.markdown('<div class="sosbtn">', unsafe_allow_html=True)
        if st.button(f"🆘  {t('send_sos')}", use_container_width=True, key="sos_btn"):
            loc = f"{lat:.6f}, {lon:.6f}" if lat else "GPS unavailable"
            mlink = f"https://maps.google.com/?q={lat},{lon}" if lat else "N/A"
            st.error(f"🚨 **ALERT DISPATCHED**\n\n👤 **{name}** | 📞 {phone or 'N/A'}\n🚨 **{etype}**\n📍 **GPS:** {loc}\n🔗 {mlink}")
            st.snow()
        st.markdown('</div>', unsafe_allow_html=True)
        if lat:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(map_embed(lat, lon, "SOS Location"), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# AI RISK
# ══════════════════════════════════════════════════════════════════════════════
elif page == "AI Risk":
    lat = st.session_state.lat
    st.markdown(f'<div class="ph"><div class="ph-eye">Machine Learning</div><div class="ph-title">{t("risk")}</div><div class="ph-sub">GPS-aware intelligent safety scoring for your live position</div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown('<div class="card"><div class="card-title">📊 Risk Assessment</div>', unsafe_allow_html=True)
        score = st.slider("Adjust Risk Score", 0, 100, 25)
        if score < 30:
            fc,lbl,icon,tip = "#10b981",t("low_risk"),"🟢","Safe conditions — normal operations."
            bar = "linear-gradient(90deg,#10b981,#059669)"
        elif score < 70:
            fc,lbl,icon,tip = "#fbbf24",t("med_risk"),"🟡","Caution advised — increase patrol."
            bar = "linear-gradient(90deg,#fbbf24,#d97706)"
        else:
            fc,lbl,icon,tip = "#f87171",t("high_risk"),"🔴","Immediate action — consider evacuation."
            bar = "linear-gradient(90deg,#f87171,#dc2626)"
        st.markdown(f'''<div style="text-align:center;padding:1.5rem 0">
          <div style="font-size:52px;filter:drop-shadow(0 0 12px {fc})">{icon}</div>
          <div style="font-family:Syne,sans-serif;font-size:26px;font-weight:800;color:{fc};margin:.5rem 0">{lbl}</div>
          <div class="rbar-bg"><div class="rbar-fill" style="width:{score}%;background:{bar}"></div></div>
          <div style="font-size:13px;color:#4a6080">{tip}</div>
          {f'<div style="font-size:11px;color:#2d4a70;margin-top:.5rem">📍 {lat:.5f}, {st.session_state.lon:.5f}</div>' if lat else ""}
        </div>''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">🌦️ Weather + Risk Factors</div>', unsafe_allow_html=True)
        st.markdown('''
        <div class="wx-card danger"><div class="wx-icon">🌀</div><div><div class="wx-title">Cyclone +15 Risk Points</div><div class="wx-sub">Severe weather elevates danger score</div></div></div>
        <div class="wx-card warn"><div class="wx-icon">🌧️</div><div><div class="wx-title">Heavy Rain +8 Risk Points</div><div class="wx-sub">Reduced visibility, slippery terrain</div></div></div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><div class="card-title">🗺️ Risk Map</div>', unsafe_allow_html=True)
        if lat:
            st.markdown(map_embed(lat, st.session_state.lon, "Risk point"), unsafe_allow_html=True)
        else:
            st.info("GPS needed to show risk map")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">📊 Zone Risk Summary</div>', unsafe_allow_html=True)
        st.table({"Zone":["Zone A","Zone B","Zone C","Zone D"],"Score":[12,72,28,45],"Level":["🟢 Low","🔴 High","🟢 Low","🟡 Med"]})
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# INCIDENT REPORT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Incident Report":
    lat = st.session_state.lat; lon = st.session_state.lon
    uname = st.session_state.username
    st.markdown(f'<div class="ph"><div class="ph-eye">Blockchain Ledger</div><div class="ph-title">{t("incident")}</div><div class="ph-sub">GPS geo-tagged, blockchain-recorded, PDF-downloadable</div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card"><div class="card-title">📋 New Report</div>', unsafe_allow_html=True)
        reporter = st.text_input("Your Name", value=uname)
        severity = st.selectbox("Severity", ["🟢 Minor","🟡 Moderate","🔴 Critical"])
        incident_desc = st.text_area("Incident Description", placeholder="What happened?", height=100)
        if lat:
            st.markdown(f'<div class="cbox" style="margin:.6rem 0"><div class="crow"><span class="ck" style="color:#64748b">📍 GPS Tag</span><span class="cv" style="font-size:12px">{lat:.6f}, {lon:.6f}</span></div></div>', unsafe_allow_html=True)

        col_sub, col_dl = st.columns(2)
        with col_sub:
            st.markdown('<div class="pbtn">', unsafe_allow_html=True)
            if st.button(t("submit"), use_container_width=True, key="inc_sub"):
                if incident_desc.strip():
                    loc_str = f"{lat:.6f},{lon:.6f}" if lat else "N/A"
                    entry = {
                        "desc": incident_desc, "severity": severity,
                        "gps": loc_str, "user": reporter,
                        "time": datetime.now().strftime("%d %b %Y %I:%M %p"),
                        "tx": f"0x{hash(incident_desc)%10**16:016x}"
                    }
                    st.session_state.incidents.append(entry)
                    st.success("✅ Report geo-tagged & recorded on blockchain!")
                    st.code(f"TX: {entry['tx']}\nGPS: {loc_str}", language="text")
                else:
                    st.warning("Please describe the incident.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_dl:
            st.markdown('<div class="gbtn">', unsafe_allow_html=True)
            pdf_text = make_pdf_report(uname, lat, lon, st.session_state.incidents)
            st.download_button(
                label=f"⬇️ {t('download')}",
                data=pdf_text.encode("utf-8"),
                file_name=f"safetrail_report_{uname}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="dl_pdf"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><div class="card-title">📍 Incident Location</div>', unsafe_allow_html=True)
        if lat:
            st.markdown(map_embed(lat, lon, f"Incident by {uname}"), unsafe_allow_html=True)
        else:
            st.info("GPS auto-embedded once active")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">🕒 All Reports</div>', unsafe_allow_html=True)
        if st.session_state.incidents:
            for inc in st.session_state.incidents[::-1][:5]:
                sev_col = "#10b981" if "Minor" in inc['severity'] else "#fbbf24" if "Moderate" in inc['severity'] else "#f87171"
                st.markdown(f'<div class="inc-row"><div class="inc-icon">📋</div><div><div class="inc-title">{inc["desc"][:45]}…</div><div class="inc-sub">{inc["time"]} · <span style="color:{sev_col}">{inc["severity"]}</span></div></div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#64748b;font-size:13px">No reports yet.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# NOTIFICATIONS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Notifications":
    st.markdown(f'<div class="ph"><div class="ph-eye">Alerts & Updates</div><div class="ph-title">{t("notify")}</div><div class="ph-sub">All safety notifications in one place</div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.markdown('<div class="card"><div class="card-title">🔔 All Notifications</div>', unsafe_allow_html=True)
        st.markdown('<div class="pbtn">', unsafe_allow_html=True)
        if st.button("✓ Mark All Read", key="mark_all"):
            for n in st.session_state.notifications: n["read"] = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        for i, n in enumerate(st.session_state.notifications):
            cls = "notif-item unread" if not n["read"] else "notif-item"
            st.markdown(f'<div class="{cls}"><div class="notif-icon">{n["icon"]}</div><div><div class="notif-msg">{n["msg"]}</div><div class="notif-time">{n["time"]}</div></div></div>', unsafe_allow_html=True)
            if not n["read"]:
                if st.button(f"Mark read", key=f"nr_{i}"):
                    st.session_state.notifications[i]["read"] = True
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><div class="card-title">📱 Emergency Contacts</div>', unsafe_allow_html=True)
        for i, ec in enumerate(st.session_state.sos_contacts):
            st.markdown(f'<div class="qcall"><div class="qcall-left"><div class="qcall-icon">👤</div><div><div class="qcall-name">{ec["name"]}</div><div class="qcall-num">{ec["phone"]}</div></div></div><a href="tel:{ec["phone"]}" class="qcall-btn">📞</a></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title" style="margin-top:1rem">➕ Add Contact</div>', unsafe_allow_html=True)
        nc_name  = st.text_input("Name",  placeholder="Contact name",  key="nc_n")
        nc_phone = st.text_input("Phone", placeholder="+91 XXXXX XXXXX", key="nc_p")
        st.markdown('<div class="gbtn">', unsafe_allow_html=True)
        if st.button("Add Contact", use_container_width=True, key="add_ec"):
            if nc_name and nc_phone:
                st.session_state.sos_contacts.append({"name": nc_name, "phone": nc_phone})
                st.success("✅ Contact added!")
                st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# NEARBY HELP
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Nearby Help":
    lat = st.session_state.lat; lon = st.session_state.lon
    st.markdown(f'<div class="ph"><div class="ph-eye">Emergency Services</div><div class="ph-title">{t("nearby")}</div><div class="ph-sub">Hospitals, Police Stations, and Emergency Services near you</div></div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1.5])
    with c1:
        st.markdown('<div class="card"><div class="card-title">📞 Emergency Numbers</div>', unsafe_allow_html=True)
        services = [
            ("🚔","Police Control Room","100","24x7"),
            ("🚑","Ambulance / EMRI","108","24x7"),
            ("🚒","Fire & Rescue","101","24x7"),
            ("👮","Tourist Helpline","1800-111-363","24x7"),
            ("🏥","Medical Helpline","104","24x7"),
            ("⚡","Disaster Mgmt","1077","24x7"),
        ]
        for icon, name_s, num, hrs in services:
            st.markdown(f'''<div class="qcall">
              <div class="qcall-left"><div class="qcall-icon">{icon}</div>
              <div><div class="qcall-name">{name_s}</div><div class="qcall-num">{num} · {hrs}</div></div></div>
              <a href="tel:{num}" class="qcall-btn">📞 Call</a>
            </div>''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><div class="card-title">🗺️ Nearby on Map</div>', unsafe_allow_html=True)
        if lat and lon:
            search_type = st.selectbox("Search for", ["hospital","police","pharmacy","fire_station"])
            map_src = f"https://maps.google.com/maps?q={search_type}+near+{lat},{lon}&z=14&output=embed"
            st.markdown(f'<iframe width="100%" height="340" style="border:0;border-radius:14px;" loading="lazy" src="{map_src}"></iframe>', unsafe_allow_html=True)
            st.markdown(f'<a href="https://www.google.com/maps/search/{search_type}+near+me/@{lat},{lon},14z" target="_blank" style="display:block;margin-top:.5rem;text-align:center;font-size:12px;color:#5b9aff;padding:.5rem;background:rgba(30,90,255,.08);border-radius:9px;border:1px solid rgba(30,90,255,.15);text-decoration:none">🔗 Open full map ↗</a>', unsafe_allow_html=True)
        else:
            st.info("📡 GPS needed to show nearby services")
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ADMIN
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Admin":
    lat = st.session_state.lat
    st.markdown(f'<div class="ph"><div class="ph-eye">System Control</div><div class="ph-title">{t("admin")}</div><div class="ph-sub">System-wide monitoring and live GPS control panel</div></div>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    stat_card(c1,"linear-gradient(90deg,#1e5aff,#5b9aff)","👥","Registered Users",str(len(st.session_state.users)),"Total accounts")
    stat_card(c2,"linear-gradient(90deg,#ef4444,#f87171)","🆘","Active Alerts","0","All clear")
    stat_card(c3,"linear-gradient(90deg,#fbbf24,#f97316)","📋","Incidents",str(len(st.session_state.incidents)),"This session")
    stat_card(c4,"linear-gradient(90deg,#10b981,#34d399)","💚","System Health","99%","All services up")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.6, 1])
    with c1:
        st.markdown('<div class="card"><div class="card-title">🗺️ Live Tracking</div>', unsafe_allow_html=True)
        if lat:
            st.markdown(map_embed(lat, st.session_state.lon, st.session_state.username), unsafe_allow_html=True)
        else:
            st.info("Waiting for GPS signal…")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-title">👥 User Registry</div>', unsafe_allow_html=True)
        user_data = {"Username": list(st.session_state.users.keys()), "Email": [v.get("email","—") for v in st.session_state.users.values()]}
        st.table(user_data)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><div class="card-title">⚙️ System Controls</div>', unsafe_allow_html=True)
        # Custom HTML toggles - always visible black text on white
        for label, default_on in [
            ("🛡️ Geo-fence Alerts", True),
            ("🤖 AI Risk Monitoring", True),
            ("🔗 Blockchain Logging", True),
            ("📱 SMS Notifications", False),
            ("🌦️ Weather Alerts", True),
        ]:
            checked = "checked" if default_on else ""
            color = "#1e5aff" if default_on else "#94a3b8"
            status = "ON" if default_on else "OFF"
            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;
                        background:#ffffff;border:1px solid rgba(30,90,255,0.12);
                        border-radius:10px;padding:.6rem 1rem;margin-bottom:6px;">
                <span style="color:#000000;font-size:13px;font-weight:700;">{label}</span>
                <span style="background:{color};color:#fff;font-size:10px;font-weight:800;
                             padding:3px 10px;border-radius:20px;letter-spacing:.5px">{status}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="pbtn">', unsafe_allow_html=True)
        if st.button("🔄  Refresh Data", use_container_width=True, key="ref_btn"): st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        if lat:
            st.markdown(f'''<div class="cbox" style="margin-top:1rem">
              <div class="crow"><span class="ck" style="color:#64748b">User</span><span class="cv" style="font-size:12px">{st.session_state.username}</span></div>
              <div class="crow"><span class="ck" style="color:#64748b">Lat</span><span class="cv" style="font-size:12px">{lat:.6f}°</span></div>
              <div class="crow"><span class="ck" style="color:#64748b">Lon</span><span class="cv" style="font-size:12px">{st.session_state.lon:.6f}°</span></div>
              <div class="crow"><span class="ck" style="color:#64748b">Accuracy</span><span class="cv" style="font-size:12px">±{st.session_state.accuracy:.0f} m</span></div>
            </div>''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close main-content
