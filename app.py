import streamlit as st
import math

# 1. PAGE CONFIG & DESIGN
st.set_page_config(page_title="Malaysia Master EV Navigator", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .main-title { font-size: 2.3rem !important; font-weight: 800 !important; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0.2rem; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; color: #38bdf8 !important; }
    .stExpander { background-color: #1e293b !important; border: 1px solid #334155 !important; border-radius: 12px !important; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 🎯 NATIONWIDE DATA GRID (INTEGRATED URBAN & HIGHWAY) ---
@st.cache_data
def get_master_database():
    return [
        # --- HIGHWAY CORRIDORS (PLUS / LPT / LEKAS / KESAS) ---
        {"state": "Johor", "town": "Highway (PLUS)", "building": "Pagoh RSA Northbound", "operator": "TNB Electron", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.1},
        {"state": "Johor", "town": "Highway (PLUS)", "building": "Yong Peng RSA Southbound", "operator": "Gentari", "type": "DC", "kw": 120, "rate": 1.60, "dist": 0.2},
        {"state": "Melaka", "town": "Highway (PLUS)", "building": "Ayer Keroh RSA Overhead", "operator": "TNB Electron", "type": "DC", "kw": 200, "rate": 2.20, "dist": 0.5},
        {"state": "Negeri Sembilan", "town": "Highway (PLUS)", "building": "Seremban RSA Southbound", "operator": "Terra", "type": "DC", "kw": 200, "rate": 1.50, "dist": 0.1},
        {"state": "Selangor", "town": "Highway (PLUS)", "building": "Dengkil RSA Southbound", "operator": "TNB Electron", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.2},
        {"state": "Perak", "town": "Highway (PLUS)", "building": "Tapah RSA Northbound", "operator": "TNB Electron", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.2},
        {"state": "Perak", "town": "Highway (PLUS)", "building": "Sungai Perak RSA Southbound", "operator": "TNB Electron", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.3},
        {"state": "Kedah", "town": "Highway (PLUS)", "building": "Gurun RSA Northbound", "operator": "Gentari", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.1},
        {"state": "Pahang", "town": "Highway (LPT)", "building": "Temerloh RSA Eastbound", "operator": "TNB Electron", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.2},
        {"state": "Terengganu", "town": "Highway (LPT)", "building": "Paka RSA Northbound", "operator": "TNB Electron", "type": "DC", "kw": 90, "rate": 1.50, "dist": 0.2},
        
        # --- URBAN CENTERS (EXPANDED NATIONWIDE) ---
        {"state": "Johor", "town": "Johor Bahru", "building": "Mid Valley Southkey", "operator": "Shell Recharge", "type": "DC", "kw": 180, "rate": 2.20, "dist": 1.2},
        {"state": "Penang", "town": "Batu Kawan", "building": "Design Village Outlet", "operator": "ChargEV", "type": "DC", "kw": 50, "rate": 1.40, "dist": 0.9},
        {"state": "Kedah", "town": "Sungai Petani", "building": "Central Square Mall", "operator": "ChargeSini", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.3},
        {"state": "Sabah", "town": "Kota Kinabalu", "building": "Imago Mall", "operator": "Gentari", "type": "DC", "kw": 60, "rate": 1.60, "dist": 0.7},
        {"state": "Sarawak", "town": "Kuching", "building": "The Spring Mall", "operator": "Gentari", "type": "DC", "kw": 120, "rate": 1.70, "dist": 1.9},
        {"state": "FT Kuala Lumpur", "town": "KLCC", "building": "Suria KLCC", "operator": "Gentari", "type": "DC", "kw": 60, "rate": 1.60, "dist": 0.2},
        {"state": "Selangor", "town": "Subang Jaya", "building": "Subang Parade", "operator": "ParkEasy", "type": "AC", "kw": 22, "rate": 0.18, "dist": 0.6}
    ]

# --- 🚗 VEHICLE MODEL DIRECTORY (ALL AVAILABLE MODELS) ---
@st.cache_data
def get_vehicle_models():
    return {
        "MG": {"MG4 Standard": 51.0, "MG4 Luxury": 64.0, "MG S5 EV Standard": 47.1, "MG S5 EV LUX Long Range": 62.1},
        "Proton": {"e.MAS 5 Prime": 42.0, "e.MAS 5 Premium": 51.5, "e.MAS 7 Prime": 49.52, "e.MAS 7 Premium": 60.22},
        "BYD": {"Atto 3 Ext": 60.48, "Seal Premium": 82.56, "Seal Performance": 82.56, "M6 Ext": 71.8},
        "Tesla": {"Model 3 RWD": 57.5, "Model 3 Long Range": 75.0, "Model Y RWD": 57.5, "Model Y Long Range": 75.0},
        "Volvo": {"EX30 Ultra": 64.0, "XC40 Recharge": 67.0},
        "Chery": {"Omoda E5": 61.0},
        "BMW": {"iX xDrive40": 71.0, "iX xDrive50": 105.2, "i4 eDrive40": 80.7},
        "Hyundai": {"Ioniq 5 Max": 72.6, "Ioniq 6 Long Range": 77.4},
        "Kia": {"EV6 GT-Line": 77.4, "EV9 AWD": 99.8},
        "Mercedes-Benz": {"EQE 350+": 90.6, "EQS 450+": 107.8},
        "Porsche": {"Taycan Base": 71.0, "Macan 4": 95.0},
        "smart": {"smart #1 Premium": 66.0, "smart #3 BRABUS": 66.0}
    }

# --- APPLICATION LOGIC ---
db, car_db = get_master_database(), get_vehicle_models()
st.markdown("### 📍 Select Location")
states = sorted(list(set(row["state"] for row in db)))
selected_state = st.selectbox("State", states)
towns = sorted(list(set(row["town"] for row in db if row["state"] == selected_state)))
selected_town = st.selectbox("Town or Highway Corridor", towns)

st.markdown(f'<h1 class="main-title">⚡ Charging Grid: {selected_town}</h1>', unsafe_allow_html=True)
LIVE_STATIONS = [row for row in db if row["state"] == selected_state and row["town"] == selected_town]

# Vehicle Selection & Logic (Truncated for brevity, rest of your original logic applies here)
st.markdown("### 🚗 Configure Vehicle")
selected_brand = st.selectbox("Brand", sorted(car_db.keys()))
selected_model = st.selectbox("Model", sorted(car_db[selected_brand].keys()))
# ... [Insert your existing calculation logic here] ...
