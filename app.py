import streamlit as st
import math

# 1. PAGE CONFIG & DESIGN
st.set_page_config(
    page_title="Malaysia Master EV Navigator", 
    page_icon="⚡", 
    layout="centered"
)

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .main-title {
        font-size: 2.3rem !important; font-weight: 800 !important;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 0.2rem;
    }
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; color: #38bdf8 !important; }
    .stExpander { background-color: #1e293b !important; border: 1px solid #334155 !important; border-radius: 12px !important; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 🎯 NATIONWIDE DATA GRID (HIGHWAY STATIONS & TNB ELECTRON HUB NETWORKS) ---
@st.cache_data
def get_master_database():
    return [
        # ==================== HIGHWAY CORRIDORS (PLUS / LPT / LEKAS) ====================
        {"state": "Johor", "town": "PLUS Highway (South)", "building": "Pagoh RSA Northbound", "operator": "TNB Electron Hub", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.1},
        {"state": "Johor", "town": "PLUS Highway (South)", "building": "Yong Peng Southbound RSA", "operator": "Gentari Highway Fast", "type": "DC", "kw": 120, "rate": 1.60, "dist": 0.2},
        {"state": "Johor", "town": "PLUS Highway (South)", "building": "Machap Northbound RSA", "operator": "Shell Recharge (ParkEasy)", "type": "DC", "kw": 180, "rate": 2.40, "dist": 0.1},
        {"state": "Johor", "town": "PLUS Highway (South)", "building": "Skudai Toll Plaza Lay-by", "operator": "JomCharge", "type": "DC", "kw": 60, "rate": 1.50, "dist": 0.4},
        
        {"state": "Melaka", "town": "PLUS Highway (South)", "building": "Ayer Keroh Overhead Bridge Restaurant RSA", "operator": "TNB Electron Hub", "type": "DC", "kw": 200, "rate": 2.20, "dist": 0.5},
        
        {"state": "Negeri Sembilan", "town": "PLUS Highway (South)", "building": "Seremban RSA Southbound (EV Hub)", "operator": "Terra ChargEV Hub", "type": "DC", "kw": 200, "rate": 1.50, "dist": 0.1},
        {"state": "Negeri Sembilan", "town": "PLUS Highway (South)", "building": "Senawang Lay-by Northbound", "operator": "Gentari BESS Modular", "type": "DC", "kw": 200, "rate": 1.60, "dist": 0.1},
        {"state": "Negeri Sembilan", "town": "PLUS Highway (South)", "building": "Senawang Lay-by Southbound", "operator": "Gentari BESS Modular", "type": "DC", "kw": 200, "rate": 1.60, "dist": 0.1},

        {"state": "Selangor", "town": "PLUS Highway (Central)", "building": "Ulu Bernam Southbound RSA", "operator": "Gentari Power", "type": "DC", "kw": 180, "rate": 1.60, "dist": 0.1},
        {"state": "Selangor", "town": "PLUS Highway (Central)", "building": "Dengkil Southbound RSA (Elite)", "operator": "TNB Electron Hub", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.2},
        {"state": "Selangor", "town": "PLUS Highway (Central)", "building": "Rawang Northbound RSA", "operator": "Gentari Fast Hub", "type": "DC", "kw": 120, "rate": 1.50, "dist": 0.1},

        {"state": "Perak", "town": "PLUS Highway (North)", "building": "Tapah RSA Northbound", "operator": "TNB Electron Hub", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.2},
        {"state": "Perak", "town": "PLUS Highway (North)", "building": "Tapah RSA Southbound", "operator": "Shell Recharge", "type": "DC", "kw": 180, "rate": 2.40, "dist": 0.1},
        {"state": "Perak", "town": "PLUS Highway (North)", "building": "Behrang Lay-by Northbound", "operator": "Gentari BESS Modular", "type": "DC", "kw": 200, "rate": 1.60, "dist": 0.1},
        {"state": "Perak", "town": "PLUS Highway (North)", "building": "Behrang Lay-by Southbound", "operator": "Gentari BESS Modular", "type": "DC", "kw": 200, "rate": 1.60, "dist": 0.1},
        {"state": "Perak", "town": "PLUS Highway (North)", "building": "Sungai Perak Southbound RSA", "operator": "TNB Electron Hub", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.3},

        {"state": "Kedah", "town": "PLUS Highway (North)", "building": "Gurun RSA Northbound", "operator": "Gentari Fast Hub", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.1},
        {"state": "Kedah", "town": "PLUS Highway (North)", "building": "Gurun RSA Southbound", "operator": "TNB Electron Hub", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.1},

        {"state": "Pahang", "town": "LPT East Coast Highway", "building": "Temerloh RSA Eastbound", "operator": "TNB Electron Hub", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.2},
        {"state": "Pahang", "town": "LPT East Coast Highway", "building": "Gambang Westbound RSA", "operator": "Shell Recharge", "type": "DC", "kw": 120, "rate": 2.20, "dist": 0.1},
        {"state": "Terengganu", "town": "LPT East Coast Highway", "building": "Paka RSA Northbound", "operator": "TNB Electron Hub", "type": "DC", "kw": 90, "rate": 1.50, "dist": 0.2},

        # ==================== URBAN CENTERS & TNB ELECTRON OUTLETS ====================
        {"state": "FT Kuala Lumpur", "town": "KLCC / Bukit Bintang", "building": "TNB Dua Sentral Hub", "operator": "TNB Electron Hub", "type": "DC", "kw": 200, "rate": 1.50, "dist": 1.5},
        {"state": "FT Kuala Lumpur", "town": "KLCC / Bukit Bintang", "building": "Suria KLCC Basement B2", "operator": "Gentari Suite", "type": "DC", "kw": 60, "rate": 1.60, "dist": 0.2},
        {"state": "FT Kuala Lumpur", "town": "KLCC / Bukit Bintang", "building": "Pavilion Kuala Lumpur B1 Deck", "operator": "Shell Recharge", "type": "DC", "kw": 120, "rate": 1.80, "dist": 0.6},

        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "The Atmosphere Seri Kembangan", "operator": "TNB Electron Plant", "type": "DC", "kw": 240, "rate": 1.50, "dist": 5.4},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "Sime Darby Auto Selection Glenmarie", "operator": "TNBX Network", "type": "DC", "kw": 60, "rate": 1.40, "dist": 1.1},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "Auto Bavaria Ara Damansara", "operator": "TNBX Network", "type": "DC", "kw": 90, "rate": 1.50, "dist": 2.3},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "Subang Parade", "operator": "ParkEasy Hub", "type": "AC", "kw": 22, "rate": 0.18, "dist": 0.6},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "UOA Business Park Glenmarie", "operator": "DC Handal", "type": "DC", "kw": 200, "rate": 0.81, "dist": 0.8},

        {"state": "Penang", "town": "Batu Kawan", "building": "Design Village Outlet Mall", "operator": "ChargEV Depot", "type": "DC", "kw": 50, "rate": 1.40, "dist": 0.9},
        {"state": "Penang", "town": "Batu Kawan", "building": "IKEA Batu Kawan Carpark", "operator": "Gentari Fast Chargers", "type": "DC", "kw": 180, "rate": 2.20, "dist": 1.1},
        {"state": "Penang", "town": "Batu Kawan", "building": "Aspen Vision City Commercial Hub", "operator": "ChargeSini Node", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.5},

        {"state": "Kedah", "town": "Sungai Petani", "building": "Central Square Shopping Mall", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.3},
        {"state": "Kedah", "town": "Sungai Petani", "building": "Village Mall Sungai Petani", "operator": "Gentari Fast Hub", "type": "DC", "kw": 60, "rate": 1.40, "dist": 0.8},
        {"state": "Kedah", "town": "Sungai Petani", "building": "Amanjaya Mall Carpark Hub", "operator": "JomCharge Depot", "type": "DC", "kw": 120, "rate": 1.60, "dist": 2.5}
    ]

# --- 🚗 MALAYSIAN MARKET EXHAUSTIVE EV MODEL DIRECTORY ---
@st.cache_data
def get_vehicle_models():
    return {
        "Audi": {"Q4 e-tron 45": 77.0, "Q8 e-tron 50": 89.0, "Q8 e-tron 55": 106.0, "e-tron GT Quattro": 83.7, "RS e-tron GT": 83.7},
        "BMW": {"iX1 xDrive30": 64.7, "iX2 xDrive30": 64.7, "iX3 M Sport": 74.0, "iX xDrive40": 71.0, "iX xDrive50": 105.2, "iX M60": 105.2, "i4 eDrive40": 80.7, "i5 eDrive40": 81.2, "i7 xDrive60": 101.7},
        "BYD": {"Dolphin Standard Range": 44.9, "Dolphin Premium Extended": 60.48, "Atto 2 Standard": 32.0, "Atto 3 Standard Range": 49.92, "Atto 3 Extended Range": 60.48, "Seal Dynamic RWD": 61.4, "Seal Premium RWD": 82.56, "Seal Performance AWD": 82.56, "Seal 6 Standard": 48.0, "M6 Electric MPV Standard": 55.4, "M6 Electric MPV Extended": 71.8},
        "Chery": {"Omoda E5": 61.0, "EQ1 Micro": 28.8},
        "Deepal": {"Deepal S05 Crossover": 56.1, "Deepal S07 Mid-SUV": 79.97},
        "Denza": {"D9 Advanced FWD": 103.3, "D9 Premium AWD": 103.6},
        "Dongfeng": {"Box Hatchback": 42.3, "Vigo Crossover": 50.5, "007 Fastback": 70.0},
        "GAC Aion": {"Aion Y Plus Premium": 63.2, "Aion Hyptec HT": 82.5},
        "GWM": {"Ora Good Cat 400 Pro": 47.8, "Ora Good Cat 500 Ultra": 63.1, "Ora 07 Long Range": 83.5, "Ora 07 Performance": 83.5},
        "Hongqi": {"E-HS9 Luxury Flagship": 99.0},
        "Hyundai": {"Kona Electric e-Max": 64.8, "Ioniq 5 Lite/Plus": 58.0, "Ioniq 5 Max AWD": 72.6, "Ioniq 6 Standard Range": 53.0, "Ioniq 6 Long Range RWD": 77.4, "Ioniq 6 Max AWD": 77.4},
        "Kia": {"Niro EV Crossover": 64.8, "EV6 GT-Line": 77.4, "EV6 GT Performance": 77.4, "EV9 AWD GT-Line": 99.8},
        "Lotus": {"Eletre Base": 112.0, "Eletre S / R": 112.0, "Emeya GT Hyper-Sedan": 102.0},
        "Maxus": {"MIFA 9 Luxury MPV": 90.0, "MIFA 9 Elevate Flagship": 90.0},
        "Mercedes-Benz": {"EQA 250": 66.5, "EQB 350 4MATIC": 66.5, "EQC 400 4MATIC": 80.0, "EQE 350+ Sedan": 90.6, "EQE 350+ SUV": 89.0, "EQE AMG 43": 90.6, "EQS 450+ Sedan": 107.8, "EQS 580 SUV": 108.4},
        "MG (Morris Garages)": {"MG4 Standard Range": 51.0, "MG4 Luxury": 64.0, "MG4 Extended Range": 77.0, "MG4 XPOWER AWD": 64.0, "MG ZS EV": 51.1, "MG S5 EV Standard": 47.1, "MG S5 EV LUX Long Range": 62.1},
        "Neta": {"Neta V Baseline": 38.5, "Neta V-II Upgrade": 36.1, "Neta X 400 Comfort": 52.4, "Neta X 500 Luxury": 62.0},
        "Nissan": {"Leaf Standard": 40.0},
        "Perodua": {"EM-O / QV-E Concept Platform": 37.0},
        "Porsche": {"Taycan Base Gen2": 71.0, "Taycan 4S / Cross Turismo": 83.7, "Macan 4 Electric": 95.0, "Macan Turbo Electric": 95.0},
        "Proton": {"e.MAS 5 Prime": 42.0, "e.MAS 5 Premium": 51.5, "e.MAS 7 Prime": 49.52, "e.MAS 7 Premium": 60.22},
        "smart": {"smart #1 Pro": 49.0, "smart #1 Premium": 66.0, "smart #1 BRABUS": 66.0, "smart #3 Pro+ / Premium": 66.0, "smart #3 BRABUS": 66.0},
        "Tesla": {"Model 3 Rear-Wheel Drive": 57.5, "Model 3 Long Range": 75.0, "Model 3 Performance": 75.0, "Model Y Rear-Wheel Drive": 57.5, "Model Y Long Range": 75.0, "Model Y Performance": 75.0},
        "Volvo": {"EX30 Plus / Ultra": 64.0, "XC40 Recharge Pure Electric": 67.0, "C40 Recharge Pure Electric": 67.0, "EX90 Flagship 7-Seater": 107.0},
        "Xpeng / Zeekr": {"Xpeng X9 Luxury MPV": 84.5, "Zeekr 009 Premium VIP": 116.0}
    }

db = get_master_database()
car_db = get_vehicle_models()

# --- 🛰️ STEP 1: REGIONAL MATRIX LOCATION ---
st.markdown("### 📍 Step 1: Select State & Town Location")

states = sorted(list(set(row["state"] for row in db)))

col_state, col_town = st.columns(2)
with col_state:
    default_state_idx = states.index("Selangor") if "Selangor" in states else 0
    selected_state = st.selectbox("Select State / Federal Territory", states, index=default_state_idx)

filtered_towns = sorted(list(set(row["town"] for row in db if row["state"] == selected_state)))

with col_town:
    selected_town = st.selectbox("Select Target Town or Highway Corridor", filtered_towns, index=0)

st.markdown(f'<h1 class="main-title">⚡ Live Active Matrix for {selected_town}</h1>', unsafe_allow_html=True)
st.success(f"📍 Intercity Grid Hub Synced: {selected_town}, {selected_state}")

LIVE_STATIONS = [row for row in db if row["state"] == selected_state and row["town"] == selected_town]

# --- 🚗 STEP 2: VEHICLE PROFILE SELECTORS ---
st.markdown("### 🚗 Step 2: Configure Vehicle Profile")

sorted_brands = sorted(list(car_db.keys()))
col_brand, col_model = st.columns(2)

with col_brand:
    # Defaults nicely to MG to easily show off your new vehicle options
    default_brand_idx = sorted_brands.index("MG (Morris Garages)") if "MG (Morris Garages)" in sorted_brands else 0
    selected_brand = st.selectbox("Select Car Brand", sorted_brands, index=default_brand_idx)

sorted_models = sorted(list(car_db[selected_brand].keys()))

with col_model:
    selected_model = st.selectbox("Select Car Model", sorted_models, index=0)

# Pulls dynamic net capacity from model dictionary entry
default_capacity = car_db[selected_brand][selected_model]
battery_capacity = st.number_input("Pack Useable Capacity (Net kWh)", min_value=10.0, value=default_capacity, step=0.1)

b_col1, b_col2 = st.columns(2)
with b_col1:
    current_soc = st.number_input("Start %", min_value=0, max_value=99, value=20)
with b_col2:
    target_soc = st.number_input("Goal %", min_value=int(current_soc + 1), max_value=100, value=80)

# --- 🎯 STEP 3: CHARGING CONSTRAINTS ---
st.markdown("### 🎯 Step 3: Set Charging Constraints")
c_col1, c_col2 = st.columns(2)

with c_col1:
    user_budget = st.number_input("Budget Cap (RM)", min_value=5.0, value=195.0, step=5.0)

with c_col2:
    max_wait_time = st.number_input("Max Time Allowance (Minutes)", min_value=10, max_value=480, value=340, step=10)

# --- MATH CALCULATION ENGINE ---
energy_needed = battery_capacity * ((target_soc - current_soc) / 100)

results = []
for station in LIVE_STATIONS:
    duration_mins = (energy_needed / station["kw"]) * 60
    cost = energy_needed * station["rate"]
    
    if cost <= user_budget and duration_mins <= max_wait_time:
        results.append({
            "building": station["building"],
            "operator": station["operator"],
            "type": station["type"],
            "power": station["kw"],
            "time": duration_mins,
            "cost": cost,
            "distance": station["dist"]
        })

results = sorted(results, key=lambda x: x["distance"])

# --- DISPLAY RENDER PRESENTATION PANEL ---
st.markdown("### 🏆 Live Station Rankings (Sorted Nearest to Selected Location)")

if not results:
    st.error("❌ No stations match your budget cap or time allowance limits along this route.")
else:
    for idx, charger in enumerate(results, 1):
        with st.expander(f"#{idx}: {charger['building']} ({charger['operator']}) — RM {charger['cost']:.2f}"):
            st.markdown(f"🏢 **Location Node:** `{charger['building']}`")
            st.markdown(f"🔌 **Network Charger Brand:** **{charger['operator']}** ({charger['power']} kW — {charger['type']})")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Est. Session Bill", f"RM {charger['cost']:.2f}")
            m2.metric("Distance from Center", f"{charger['distance']:.1f} km")
            m3.metric("Required Stop Time", f"{charger['time']:.0f} mins")
            
            st.markdown(f"🔗 **[Open Navigation Map Directions Hub](https://www.plugshare.com/)**")

st.markdown("---")
st.markdown("⚡ *Complete Malaysian EV Model Matrix updated with latest local and international launches.*")
