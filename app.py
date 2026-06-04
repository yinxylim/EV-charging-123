import streamlit as st
import streamlit.components.v1 as components
import json
import math

# 1. PAGE CONFIG & MODERN STYLE INJECTION
st.set_page_config(
    page_title="Ultimate EV Optimizer", 
    page_icon="⚡", 
    layout="centered"
)

# Cleaned CSS
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .main-title {
        font-size: 2.3rem !important; font-weight: 800 !important;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 0.2rem;
    }
    .sub-title { text-align: center; color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; color: #38bdf8 !important; }
    .stExpander { background-color: #1e293b !important; border: 1px solid #334155 !important; border-radius: 12px !important; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State variables so the page doesn't reset on inputs
if "user_lat" not in st.session_state:
    st.session_state.user_lat = 3.0792  # Fallback default (Subang Jaya Centerpoint)
    st.session_state.user_lon = 101.5834
    st.session_state.geo_synced = False

# --- CLEAN JAVASCRIPT GEOLOCATION COUPLER ---
# Using Streamlit query params safely without destructive page flashing
query_params = st.query_params
if "lat" in query_params and "lon" in query_params:
    st.session_state.user_lat = float(query_params["lat"])
    st.session_state.user_lon = float(query_params["lon"])
    st.session_state.geo_synced = True

# Hidden location fetcher that executes safely via standard Web API
location_html = """
<script>
    navigator.geolocation.getCurrentPosition(function(position) {
        const lat = position.coords.latitude.toFixed(4);
        const lon = position.coords.longitude.toFixed(4);
        const urlParams = new URLSearchParams(window.parent.location.search);
        
        if (urlParams.get('lat') !== lat || urlParams.get('lon') !== lon) {
            urlParams.set('lat', lat);
            urlParams.set('lon', lon);
            window.parent.history.replaceState({}, '', window.parent.location.pathname + '?' + urlParams.toString());
            // Small delayed action to signal app framework smoothly
            setTimeout(() => { window.parent.location.reload(); }, 300);
        }
    });
</script>
"""

# Only trigger geolocation components if we haven't locked coordinates yet
if not st.session_state.geo_synced:
    components.html(location_html, height=0, width=0)
    st.caption("🌐 Location Engine Active: Awaiting browser coordinate match...")
else:
    st.success(f"📍 GPS Sync Active: Showing closest stations to your position ({st.session_state.user_lat:.4f}, {st.session_state.user_lon:.4f})")

# Render Dynamic Headers
st.markdown('<h1 class="main-title">⚡ Ultimate EV Charger Optimizer</h1>', unsafe_allow_html=True)
location_title = "Live GPS Matcher & Smart Curve Simulator" if st.session_state.geo_synced else "Subang Jaya Station Matcher & Smart Curve Simulator"
st.markdown(f'<p class="sub-title">{location_title}</p>', unsafe_allow_html=True)

# Comprehensive Malaysian EV Market Database
EV_MODELS = {
    "Xpeng G6 (Standard Range)": {"battery_kwh": 66.0, "max_ac_kw": 11.0, "max_dc_kw": 215.0},
    "Xpeng G6 (Long Range)": {"battery_kwh": 87.5, "max_ac_kw": 11.0, "max_dc_kw": 280.0},
    "Zeekr 7X (Standard LFP)": {"battery_kwh": 75.0, "max_ac_kw": 22.0, "max_dc_kw": 450.0},
    "Zeekr 7X (Long Range NCM)": {"battery_kwh": 100.0, "max_ac_kw": 22.0, "max_dc_kw": 420.0},
    "MG S5 EV (Lux Long Range)": {"battery_kwh": 62.0, "max_ac_kw": 7.0, "max_dc_kw": 150.0},
    "MG ZS EV (COM/LUX)": {"battery_kwh": 51.1, "max_ac_kw": 7.0, "max_dc_kw": 50.0},
    "Proton e.MAS 7 (Prime)": {"battery_kwh": 49.5, "max_ac_kw": 11.0, "max_dc_kw": 80.0},
    "Proton e.MAS 7 (Extended)": {"battery_kwh": 60.2, "max_ac_kw": 11.0, "max_dc_kw": 80.0},
    "Chery Omoda E5": {"battery_kwh": 61.0, "max_ac_kw": 9.9, "max_dc_kw": 80.0},
    "BYD Atto 3 (Extended Range)": {"battery_kwh": 60.5, "max_ac_kw": 7.0, "max_dc_kw": 88.0},
    "BYD Dolphin (Standard Range)": {"battery_kwh": 44.9, "max_ac_kw": 7.0, "max_dc_kw": 60.0},
    "BYD Seal (Premium)": {"battery_kwh": 82.5, "max_ac_kw": 7.0, "max_dc_kw": 150.0},
    "Tesla Model 3 (Standard RWD)": {"battery_kwh": 60.0, "max_ac_kw": 11.0, "max_dc_kw": 170.0},
    "Tesla Model Y (Rear-Wheel Drive)": {"battery_kwh": 57.5, "max_ac_kw": 11.0, "max_dc_kw": 170.0},
    "Custom / Other Vehicle": {"battery_kwh": 60.0, "max_ac_kw": 11.0, "max_dc_kw": 100.0}
}

# Regional Charging Database
STATIONS = [
    {"name": "Subang Parade (ParkEasy Hub)", "type": "AC", "power_kw": 22, "rate_per_kwh": 1.00, "rate_per_min": 0.0, "lat": 3.0821, "lon": 101.5878, "link": "https://www.plugshare.com/location/587223"},
    {"name": "Sunway Pyramid (ChargeSini Hub)", "type": "AC", "power_kw": 22, "rate_per_kwh": 0.00, "rate_per_min": 0.40, "lat": 3.0731, "lon": 101.6078, "link": "https://www.chargesini.com/"},
    {"name": "The Summit USJ (JomCharge)", "type": "DC", "power_kw": 60, "rate_per_kwh": 1.50, "rate_per_min": 0.0, "lat": 3.0594, "lon": 101.5925, "link": "https://cardog.app/tools/charging/my/subang-jaya-10"},
    {"name": "UOA Business Park Glenmarie (DC Handal)", "type": "DC", "power_kw": 200, "rate_per_kwh": 1.70, "rate_per_min": 0.0, "lat": 3.0862, "lon": 101.5819, "link": "https://cardog.app/tools/charging/my/subang-jaya-10"},
    {"name": "Shell Recharge Mint Hotel (High Speed)", "type": "DC", "power_kw": 180, "rate_per_kwh": 2.20, "rate_per_min": 0.0, "lat": 3.0244, "lon": 101.7058, "link": "https://www.gentari.com/go/charging-network/malaysia"},
    {"name": "Aeon Mall Shah Alam (ChargEV)", "type": "DC", "power_kw": 120, "rate_per_kwh": 1.60, "rate_per_min": 0.0, "lat": 3.0701, "lon": 101.5434, "link": "https://www.chargev.my/"},
    {"name": "Bangsar Shopping Centre (JomCharge)", "type": "AC", "power_kw": 11, "rate_per_kwh": 0.80, "rate_per_min": 0.0, "lat": 3.1429, "lon": 101.6667, "link": "https://www.jomcharge.com/"}
]

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# --- MAIN SCREEN INPUTS ---
st.markdown("### 🚗 Step 1: Select Your Vehicle Profile")
selected_brand = st.selectbox("Choose Model Variant", list(EV_MODELS.keys()))
default_specs = EV_MODELS[selected_brand]

with st.expander("⚙️ View / Tweak Advanced Mechanical Specs"):
    v_col1, v_col2, v_col3 = st.columns(3)
    with v_col1:
        battery_capacity = st.number_input("Battery Capacity (kWh)", min_value=15.0, value=default_specs["battery_kwh"], step=0.5)
    with v_col2:
        max_ac_limit = st.number_input("Max Vehicle AC Input (kW)", min_value=3.3, value=default_specs["max_ac_kw"], step=0.1)
    with v_col3:
        max_dc_limit = st.number_input("Max Vehicle DC Input (kW)", min_value=20.0, value=default_specs["max_dc_kw"], step=5.0)

st.markdown("### 🔋 Step 2: Set Charging Requirements")
b_col1, b_col2 = st.columns(2)
with b_col1:
    current_soc = st.number_input("Current Battery Level (Starting %)", min_value=0, max_value=99, value=20, step=1)
with b_col2:
    target_soc = st.number_input("Target Battery Level (Goal %)", min_value=int(current_soc + 1), max_value=100, value=80, step=1)

st.markdown("### ⏱️ Step 3: Set Your Personal Limits")
c_col1, c_col2 = st.columns(2)
with c_col1:
    user_time_limit = st.number_input("Max Wait Allowance (Minutes)", min_value=10, max_value=480, value=45, step=5)
with c_col2:
    user_budget = st.number_input("Wallet Budget Max (RM)", min_value=5.0, max_value=300.0, value=40.0, step=5.0)

# --- MATH SIMULATION ENGINE ---
def simulate_charging_session(station, start_soc, end_soc, cap_ac, cap_dc, total_capacity, time_limit, budget_limit):
    current_soc_running = start_soc
    total_time_mins = 0.0
    total_energy_kwh = 0.0
    hit_slowdown = False

    while current_soc_running < end_soc:
        if station["type"] == "AC":
            current_speed = min(station["power_kw"], cap_ac)
        else:
            base_speed = min(station["power_kw"], cap_dc)
            if current_soc_running < 80:
                current_speed = base_speed
            elif 80 <= current_soc_running < 90:
                current_speed = base_speed * 0.50
                hit_slowdown = True
            else:
                current_speed = min(base_speed * 0.15, 11.0)
                hit_slowdown = True

        energy_step_kwh = total_capacity * 0.01
        time_step_mins = (energy_step_kwh / current_speed) * 60.0

        if (total_time_mins + time_step_mins) > time_limit:
            break
            
        projected_cost = ((total_energy_kwh + energy_step_kwh) * station["rate_per_kwh"]) + ((total_time_mins + time_step_mins) * station["rate_per_min"])
        if projected_cost > budget_limit:
            break

        total_time_mins += time_step_mins
        total_energy_kwh += energy_step_kwh
        current_soc_running += 1

    final_cost = (total_energy_kwh * station["rate_per_kwh"]) + (total_time_mins * station["rate_per_min"])
    attained_goal = "Yes" if current_soc_running >= end_soc else f"Partial ({current_soc_running}%)"

    return total_energy_kwh, total_time_mins, final_cost, attained_goal, hit_slowdown

# Calculation Execution
soc_delta = target_soc - current_soc
energy_needed_theoretical = battery_capacity * (soc_delta / 100)

st.write("---")
st.info(f"📊 **Target Assessment:** Adding **{soc_delta}%** charge requires ~**{energy_needed_theoretical:.2f} kWh** of raw energy.")

results = []
for station in STATIONS:
    distance_km = calculate_distance(st.session_state.user_lat, st.session_state.user_lon, station["lat"], station["lon"])
    
    energy, duration, cost, outcome, slowed = simulate_charging_session(
        station, current_soc, target_soc, max_ac_limit, max_dc_limit, battery_capacity, user_time_limit, user_budget
    )
    if duration > 0:
        results.append({
            "name": station["name"], "type": station["type"], "power": f"{station['power_kw']} kW",
            "energy": energy, "time": duration, "cost": cost, "outcome": outcome, "slowed": slowed, 
            "link": station["link"], "distance": distance_km
        })

# Sort selections by closest physical distance
results = sorted(results, key=lambda x: x["distance"])

# --- DISPLAY OUTPUT RESULTS PANEL ---
st.markdown("### 🏆 Live Station Rankings (Nearest to You)")

if not results:
    st.error("❌ No options match your boundaries. Try expanding your parameters.")
else:
    for idx, charger in enumerate(results, 1):
        badge = "🟢 **Full Goal Reached**" if charger["outcome"] == "Yes" else f"🟡 **{charger['outcome']}**"
            
        with st.expander(f"#{idx}: {charger['name']} ({charger['distance']:.1f} km away) — RM {charger['cost']:.2f}"):
            st.markdown(f"⚡ **Status Indicator:** {badge} | 📍 **Distance:** {charger['distance']:.1f} km")
            
            if charger["slowed"] and charger["type"] == "DC":
                st.warning("⚠️ *Battery crossed 80%. Multi-stage speed throttling was applied automatically.*")
                
            m1, m2, m3 = st.columns(3)
            m1.metric("Est. Total Bill", f"RM {charger['cost']:.2f}")
            m2.metric("Energy Transferred", f"{charger['energy']:.2f} kWh")
            m3.metric("Required Stop Time", f"{charger['time']:.1f} mins")
            
            st.markdown(f"🎯 **[Tap to Open Navigation Map & Station Rules]({charger['link']})**")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>⚡ Built by an independent local developer. Tracks your location safely across Malaysia! ☕</p>", unsafe_allow_html=True)
