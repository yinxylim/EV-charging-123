import streamlit as st
import math
import requests

# 1. PAGE CONFIG & DESIGN
st.set_page_config(
    page_title="Live EV Optimizer", 
    page_icon="⚡", 
    layout="centered"
)

# 🛑 REPLACE WITH YOUR FREE OPEN CHARGE MAP API KEY
OCM_API_KEY = "YOUR_OPEN_CHARGE_MAP_API_KEY"

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

st.markdown('<h1 class="main-title">⚡ Live EV Charger Optimizer</h1>', unsafe_allow_html=True)

# --- PRESET LOCATION DICTIONARY ---
PRESET_OPTIONS = {
    "Subang Jaya / USJ (Centerpoint)": (3.0792, 101.5834),
    "Sunway / Bandar Sunway": (3.0731, 101.6078),
    "Shah Alam (Aeon Area)": (3.0701, 101.5434),
    "Kuala Lumpur / Sungai Besi": (3.0244, 101.7058),
}

st.markdown("### 📍 Step 1: Set Your Location Zone")
selected_zone = st.selectbox("Where are you currently?", list(PRESET_OPTIONS.keys()))
user_lat, user_lon = PRESET_OPTIONS[selected_zone]

# --- 🛰️ DYNAMIC LIVE API FETCH ---
@st.cache_data(ttl=60)  # Caches live data for 1 minute to keep performance snappy
def fetch_live_stations(lat, lon, api_key):
    if api_key == "YOUR_OPEN_CHARGE_MAP_API_KEY" or not api_key:
        # Fallback to local test list if no API key is provided yet
        return [
            {"name": "Subang Parade Hub", "type": "AC", "power_kw": 22, "rate_per_kwh": 1.00, "lat": 3.0821, "lon": 101.5878, "link": "https://www.plugshare.com"},
            {"name": "Shell Recharge Mint Hotel", "type": "DC", "power_kw": 180, "rate_per_kwh": 2.20, "lat": 3.0244, "lon": 101.7058, "link": "https://www.plugshare.com"}
        ]
    
    url = f"https://api.openchargemap.io/v3/poi/?key={api_key}&output=json&latitude={lat}&longitude={lon}&distance=25&distanceunit=KM&maxresults=10"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            raw_data = response.json()
            live_list = []
            for item in raw_data:
                addr = item.get("AddressInfo", {})
                conns = item.get("Connections", [{}])
                
                # Check if it's DC Fast Charging or AC
                is_dc = any(c.get("CurrentTypeID") == 30 or (c.get("PowerKW") or 0) > 22 for c in conns)
                max_power = max([c.get("PowerKW") or 0 for c in conns], default=22)
                
                live_list.append({
                    "name": addr.get("Title", "Unknown Charger"),
                    "type": "DC" if is_dc else "AC",
                    "power_kw": max_power if max_power > 0 else 22,
                    "rate_per_kwh": 1.20 if is_dc else 0.80, # Estimate pricing if API field is blank
                    "lat": addr.get("Latitude"),
                    "lon": addr.get("Longitude"),
                    "link": addr.get("RelatedURL") or f"https://www.google.com/maps/search/?api=1&query={addr.get('Latitude')},{addr.get('Longitude')}"
                })
            return live_list
    except Exception as e:
        st.error(f"Error reaching live network: {e}")
    return []

# Fetch completely new stations relative to dropdown
STATIONS = fetch_live_stations(user_lat, user_lon, OCM_API_KEY)

# --- UI WORKFLOW INPUTS ---
st.markdown("### 🚗 Step 2: Set Requirements")
v_col1, v_col2 = st.columns(2)
with v_col1:
    battery_capacity = st.number_input("Pack Capacity (Net kWh)", min_value=10.0, value=60.0)
with v_col2:
    user_budget = st.number_input("Budget Cap (RM)", min_value=5.0, value=50.0)

b_col1, b_col2 = st.columns(2)
with b_col1:
    current_soc = st.number_input("Start %", min_value=0, max_value=99, value=20)
with b_col2:
    target_soc = st.number_input("Goal %", min_value=int(current_soc + 1), max_value=100, value=80)

# --- COMPUTATION ENGINES ---
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

results = []
for station in STATIONS:
    distance_km = calculate_distance(user_lat, user_lon, station["lat"], station["lon"])
    
    # Fast simulation calculations
    speed = station["power_kw"]
    needed_kwh = battery_capacity * ((target_soc - current_soc) / 100)
    duration_mins = (needed_kwh / speed) * 60
    cost = needed_kwh * station["rate_per_kwh"]
    
    if cost <= user_budget:
        results.append({
            "name": station["name"], "type": station["type"], "power": station["power_kw"],
            "time": duration_mins, "cost": cost, "link": station["link"], "distance": distance_km
        })

results = sorted(results, key=lambda x: x["distance"])

# --- DISPLAY PANEL ---
st.markdown("### 🏆 Real Live Station Rankings")
if OCM_API_KEY == "YOUR_OPEN_CHARGE_MAP_API_KEY":
    st.warning("⚠️ Running on local demo placeholders. Insert your Open Charge Map API key to pull real-time nearby stations.")

for idx, charger in enumerate(results, 1):
    with st.expander(f"#{idx}: {charger['name']} ({charger['distance']:.1f} km)"):
        m1, m2, m3 = st.columns(3)
        m1.metric("Est. Cost", f"RM {charger['cost']:.2f}")
        m2.metric("Speed", f"{charger['power']} kW ({charger['type']})")
        m3.metric("Duration", f"{charger['time']:.0f} mins")
        st.markdown(f"🔗 **[Navigate / Open Station Details]({charger['link']})**")
