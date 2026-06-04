import streamlit as st
import math
import folium
from streamlit_folium import st_folium

# 1. PAGE CONFIG & DESIGN
st.set_page_config(
    page_title="Ultimate EV Optimizer", 
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
    .sub-title { text-align: center; color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; color: #38bdf8 !important; }
    .stExpander { background-color: #1e293b !important; border: 1px solid #334155 !important; border-radius: 12px !important; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">⚡ Ultimate EV Charger Optimizer</h1>', unsafe_allow_html=True)

# --- STATION DATABASE ---
STATIONS = [
    {"name": "Subang Parade (ParkEasy Hub)", "type": "AC", "power_kw": 22, "rate_per_kwh": 1.00, "rate_per_min": 0.0, "lat": 3.0821, "lon": 101.5878, "link": "https://www.plugshare.com/location/587223"},
    {"name": "Sunway Pyramid (ChargeSini Hub)", "type": "AC", "power_kw": 22, "rate_per_kwh": 0.00, "rate_per_min": 0.40, "lat": 3.0731, "lon": 101.6078, "link": "https://www.chargesini.com/"},
    {"name": "The Summit USJ (JomCharge)", "type": "DC", "power_kw": 60, "rate_per_kwh": 1.50, "rate_per_min": 0.0, "lat": 3.0594, "lon": 101.5925, "link": "https://cardog.app/tools/charging/my/subang-jaya-10"},
    {"name": "UOA Business Park Glenmarie (DC Handal)", "type": "DC", "power_kw": 200, "rate_per_kwh": 1.70, "rate_per_min": 0.0, "lat": 3.0862, "lon": 101.5819, "link": "https://cardog.app/tools/charging/my/subang-jaya-10"},
    {"name": "Shell Recharge Mint Hotel (Ultra-High Speed)", "type": "DC", "power_kw": 180, "rate_per_kwh": 2.20, "rate_per_min": 0.0, "lat": 3.0244, "lon": 101.7058, "link": "https://www.gentari.com/go/charging-network/malaysia"},
    {"name": "Aeon Mall Shah Alam (ChargEV)", "type": "DC", "power_kw": 120, "rate_per_kwh": 1.60, "rate_per_min": 0.0, "lat": 3.0701, "lon": 101.5434, "link": "https://www.chargev.my/"}
]

# --- VEHICLE DATABASE ---
EV_MODELS = {
    "Proton e.MAS 7 (Extended)": {"battery_kwh": 60.22, "max_ac_kw": 11.0, "max_dc_kw": 80.0},
    "BYD Dolphin (Premium Extended)": {"battery_kwh": 60.48, "max_ac_kw": 7.0, "max_dc_kw": 80.0},
    "Tesla Model 3 (Long Range)": {"battery_kwh": 75.0, "max_ac_kw": 11.0, "max_dc_kw": 250.0},
    "Xpeng G6 (Long Range)": {"battery_kwh": 87.5, "max_ac_kw": 11.0, "max_dc_kw": 280.0},
    "Custom / Other Vehicle Specs": {"battery_kwh": 60.0, "max_ac_kw": 11.0, "max_dc_kw": 100.0}
}

# --- INTERACTIVE MAP GEOLOCATION BACKEND ---
st.markdown("### 📍 Step 1: Set Your Current Location")
st.caption("Tap the 🎯 icon on the map below to instantly lock onto your mobile device's live satellite GPS coordinates.")

# Standard default focus coordinates
init_lat, init_lon = 3.0792, 101.5834 

# Generate native Folium Map
m = folium.Map(location=[init_lat, init_lon], zoom_start=13, tiles="cartodbpositron")

# Inject the browser-level geolocation target button
folium.plugins.LocateControl(
    locateOptions={'enableHighAccuracy': True},
    keepCurrentZoomLevel=True,
    title="Sync Mobile GPS"
).add_to(m)

# Plot charging infrastructure pins onto the interactive map layer
for station in STATIONS:
    folium.Marker(
        location=[station["lat"], station["lon"]],
        popup=f"{station['name']} ({station['power_kw']}kW)",
        icon=folium.Icon(color="blue" if station["type"] == "AC" else "red", icon="flash", prefix="fa")
    ).add_to(m)

# Render map component frame
map_data = st_folium(m, width=700, height=350, key="gps_map")

# Update calculation matrix values based on user map interaction
user_lat, user_lon = init_lat, init_lon
is_live_gps = False

if map_data and map_data.get("last_object_clicked_by_target"):
    user_lat = map_data["last_object_clicked_by_target"]["lat"]
    user_lon = map_data["last_object_clicked_by_target"]["lng"]
    is_live_gps = True
elif map_data and map_data.get("center"):
    # If the user drags or shifts the map view manually
    user_lat = map_data["center"]["lat"]
    user_lon = map_data["center"]["lng"]

if is_live_gps:
    st.success(f"🎯 **Mobile GPS Synchronized:** ({user_lat:.4f}, {user_lon:.4f})")
else:
    st.info(f"🗺️ **Position Matrix:** Pointed at ({user_lat:.4f}, {user_lon:.4f}). Drag map or tap the target button to shift location.")

# --- APPLICATION WORKFLOW INPUTS ---
st.markdown("### 🚗 Step 2: Select Your Vehicle Profile")
selected_brand = st.selectbox("Choose Model Variant", list(EV_MODELS.keys()))
default_specs = EV_MODELS[selected_brand]

with st.expander("⚙️ View / Modify Battery Architecture"):
    v_col1, v_col2, v_col3 = st.columns(3)
    with v_col1:
        battery_capacity = st.number_input("Pack Capacity (kWh)", min_value=10.0, value=default_specs["battery_kwh"])
    with v_col2:
        max_ac_limit = st.number_input("Max OBC AC (kW)", min_value=3.3, value=default_specs["max_ac_kw"])
    with v_col3:
        max_dc_limit = st.number_input("Max DC Intake (kW)", min_value=10.0, value=default_specs["max_dc_kw"])

st.markdown("### 🔋 Step 3: Set Charging Requirements & Constraints")
b_col1, b_col2, b_col3 = st.columns(3)
with b_col1:
    current_soc = st.number_input("Start %", min_value=0, max_value=99, value=20)
with b_col2:
    target_soc = st.number_input("Goal %", min_value=int(current_soc + 1), max_value=100, value=80)
with b_col3:
    user_budget = st.number_input("Budget Cap (RM)", min_value=5.0, value=50.0)

# --- MATH SIMULATION ENGINE ---
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

def simulate_charging_session(station, start_soc, end_soc, cap_ac, cap_dc, total_capacity, budget_limit):
    current_soc_running = start_soc
    total_time_mins = 0.0
    total_energy_kwh = 0.0
    slowed = False

    while current_soc_running < end_soc:
        if station["type"] == "AC":
            current_speed = min(station["power_kw"], cap_ac)
        else:
            base_speed = min(station["power_kw"], cap_dc)
            current_speed = base_speed if current_soc_running < 80 else base_speed * 0.40
            if current_soc_running >= 80: slowed = True

        energy_step_kwh = total_capacity * 0.01
        time_step_mins = (energy_step_kwh / current_speed) * 60.0
        
        projected_cost = ((total_energy_kwh + energy_step_kwh) * station["rate_per_kwh"]) + ((total_time_mins + time_step_mins) * station["rate_per_min"])
        if projected_cost > budget_limit: break

        total_time_mins += time_step_mins
        total_energy_kwh += energy_step_kwh
        current_soc_running += 1

    final_cost = (total_energy_kwh * station["rate_per_kwh"]) + (total_time_mins * station["rate_per_min"])
    return total_energy_kwh, total_time_mins, final_cost, slowed

# Calculation Execution
results = []
for station in STATIONS:
    distance_km = calculate_distance(user_lat, user_lon, station["lat"], station["lon"])
    energy, duration, cost, slowed = simulate_charging_session(
        station, current_soc, target_soc, max_ac_limit, max_dc_limit, battery_capacity, user_budget
    )
    if duration > 0:
        results.append({
            "name": station["name"], "type": station["type"], "energy": energy, 
            "time": duration, "cost": cost, "slowed": slowed, "link": station["link"], "distance": distance_km
        })

results = sorted(results, key=lambda x: x["distance"])

# --- PRESENTATION ELEMENT ---
st.markdown("### 🏆 Live Station Rankings (Sorted Nearest to Selected Location)")

for idx, charger in enumerate(results, 1):
    with st.expander(f"#{idx}: {charger['name']} ({charger['distance']:.1f} km) — RM {charger['cost']:.2f}"):
        st.markdown(f"📍 **Distance From Pointer:** {charger['distance']:.1f} km")
        if charger["slowed"] and charger["type"] == "DC":
            st.warning("⚠️ *Charging speed throttled automatically by vehicle BMS design (>80% SoC).*")
        m1, m2, m3 = st.columns(3)
        m1.metric("Est. Cost", f"RM {charger['cost']:.2f}")
        m2.metric("Energy Yield", f"{charger['energy']:.1f} kWh")
        m3.metric("Duration", f"{charger['time']:.0f} mins")
        st.markdown(f"🎯 **[Open Live PlugShare Link]({charger['link']})**")
