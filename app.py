import streamlit as st

# Page Setup
st.set_page_config(page_title="Ultimate EV Optimizer", page_icon="⚡", layout="centered")
st.title("⚡ Ultimate EV Charger Optimizer")
st.subheader("Subang Jaya Station Matcher & Simulator")
st.write("Configure your vehicle specs, current battery levels, and limits below.")

# Comprehensive Local EV Database
EV_MODELS = {
    "BYD Atto 3 (Extended Range)": {"battery_kwh": 60.5, "max_ac_kw": 7.0, "max_dc_kw": 88.0},
    "BYD Dolphin (Standard Range)": {"battery_kwh": 44.9, "max_ac_kw": 7.0, "max_dc_kw": 60.0},
    "BYD Seal (Premium)": {"battery_kwh": 82.5, "max_ac_kw": 7.0, "max_dc_kw": 150.0},
    "Tesla Model 3 (Standard RWD)": {"battery_kwh": 60.0, "max_ac_kw": 11.0, "max_dc_kw": 170.0},
    "Tesla Model Y (Rear-Wheel Drive)": {"battery_kwh": 57.5, "max_ac_kw": 11.0, "max_dc_kw": 170.0},
    "GWM Ora Good Cat (500 Ultra)": {"battery_kwh": 63.1, "max_ac_kw": 6.6, "max_dc_kw": 60.0},
    "Smart #1 (Pro)": {"battery_kwh": 49.0, "max_ac_kw": 7.2, "max_dc_kw": 150.0},
    "Custom / Other Vehicle": {"battery_kwh": 60.0, "max_ac_kw": 11.0, "max_dc_kw": 100.0}
}

# Regional Charging Network Database
STATIONS = [
    {"name": "Subang Parade (ParkEasy Hub)", "type": "AC", "power_kw": 22, "rate_per_kwh": 1.00, "rate_per_min": 0.0, "link": "https://www.plugshare.com/location/587223"},
    {"name": "Sunway Pyramid (ChargeSini Hub)", "type": "AC", "power_kw": 22, "rate_per_kwh": 0.00, "rate_per_min": 0.40, "link": "https://www.chargesini.com/"},
    {"name": "The Summit USJ (JomCharge)", "type": "DC", "power_kw": 60, "rate_per_kwh": 1.50, "rate_per_min": 0.0, "link": "https://cardog.app/tools/charging/my/subang-jaya-10"},
    {"name": "UOA Business Park Glenmarie (DC Handal)", "type": "DC", "power_kw": 200, "rate_per_kwh": 1.70, "rate_per_min": 0.0, "link": "https://cardog.app/tools/charging/my/subang-jaya-10"},
    {"name": "Shell Recharge Mint Hotel (High Speed)", "type": "DC", "power_kw": 180, "rate_per_kwh": 2.20, "rate_per_min": 0.0, "link": "https://www.gentari.com/go/charging-network/malaysia"}
]

# --- SECTION 1: DETAILED VEHICLE INPUTS ---
st.sidebar.header("🚗 1. Vehicle Setup Profile")
selected_brand = st.sidebar.selectbox("Select Car Brand / Variant", list(EV_MODELS.keys()))
default_specs = EV_MODELS[selected_brand]

# Input fields auto-populate based on selection, but stay completely editable
battery_capacity = st.sidebar.number_input("Battery Size (Total kWh Capacity)", min_value=15.0, max_value=150.0, value=default_specs["battery_kwh"], step=0.5)
max_ac_limit = st.sidebar.number_input("Max Vehicle AC Power Intake Limit (kW)", min_value=3.3, max_value=22.0, value=default_specs["max_ac_kw"], step=0.1)
max_dc_limit = st.sidebar.number_input("Max Vehicle DC Fast-Charge Limit (kW)", min_value=20.0, max_value=350.0, value=default_specs["max_dc_kw"], step=5.0)

# --- SECTION 2: PERCENTAGE INPUT BOXES ---
st.sidebar.header("🔋 2. Charge Target Matrix")
current_soc = st.sidebar.number_input("Current Battery Level (Starting %)", min_value=0, max_value=99, value=20, step=1)

# Dynamically force the target percent input box to protect against impossible values
target_soc = st.sidebar.number_input("Target Battery Level (Goal %)", min_value=int(current_soc + 1), max_value=100, value=80, step=1)

# --- SECTION 3: TRIP CONSTRAINTS ---
st.write("---")
st.markdown("### ⏱️ Session Parameters")
col1, col2 = st.columns(2)

with col1:
    user_time_limit = st.number_input("Max Waiting Time Allowed (Minutes)", min_value=10, max_value=480, value=45, step=5)
with col2:
    user_budget = st.number_input("Wallet Budget Threshold Limit (RM)", min_value=5.0, max_value=300.0, value=40.0, step=5.0)

# --- MULTI-STAGE SIMULATION ENGINE ---
def simulate_charging_session(station, start_soc, end_soc, cap_ac, cap_dc, total_capacity, time_limit, budget_limit):
    current_soc_running = start_soc
    total_time_mins = 0.0
    total_energy_kwh = 0.0
    hit_slowdown = False

    while current_soc_running < end_soc:
        # Determine actual charge intake speed factoring charger vs vehicle capabilities
        if station["type"] == "AC":
            current_speed = min(station["power_kw"], cap_ac)
        else: # Applies realistic battery thermal curves for DC Fast Chargers
            base_speed = min(station["power_kw"], cap_dc)
            if current_soc_running < 80:
                current_speed = base_speed
            elif 80 <= current_soc_running < 90:
                current_speed = base_speed * 0.50  # Power drops by 50%
                hit_slowdown = True
            else:
                current_speed = min(base_speed * 0.15, 11.0)  # Power drops to a slow trickle
                hit_slowdown = True

        # Math logic to scale up 1% State of Charge (SoC)
        energy_step_kwh = total_capacity * 0.01
        time_step_mins = (energy_step_kwh / current_speed) * 60.0

        # Boundary checks against user parameters
        if (total_time_mins + time_step_mins) > time_limit:
            break
            
        projected_cost = ((total_energy_kwh + energy_step_kwh) * station["rate_per_kwh"]) + ((total_time_mins + time_step_mins) * station["rate_per_min"])
        if projected_cost > budget_limit:
            break

        # Process step confirmation
        total_time_mins += time_step_mins
        total_energy_kwh += energy_step_kwh
        current_soc_running += 1

    final_cost = (total_energy_kwh * station["rate_per_kwh"]) + (total_time_mins * station["rate_per_min"])
    attained_goal = "Yes" if current_soc_running >= end_soc else f"Partial ({current_soc_running}%)"

    return total_energy_kwh, total_time_mins, final_cost, attained_goal, hit_slowdown

# Execute Calculations
soc_delta = target_soc - current_soc
energy_needed_theoretical = battery_capacity * (soc_delta / 100)

st.info(f"📊 **Target Metric:** Charge up **{soc_delta}%** of the battery. Requires an estimated **{energy_needed_theoretical:.2f} kWh**.")

results = []
for station in STATIONS:
    energy, duration, cost, outcome, slowed = simulate_charging_session(
        station, current_soc, target_soc, max_ac_limit, max_dc_limit, battery_capacity, user_time_limit, user_budget
    )
    
    if duration > 0:
        results.append({
            "name": station["name"],
            "type": station["type"],
            "power": f"{station['power_kw']} kW",
            "energy": energy,
            "time": duration,
            "cost": cost,
            "outcome": outcome,
            "slowed": slowed,
            "link": station["link"]
        })

# Sort selections by lowest cost
results = sorted(results, key=lambda x: x["cost"])

# --- DISPLAY RENDER LAYOUT ---
st.write("---")
st.markdown("### 🏆 Filtered Options Ranked by Total Cost")

if not results:
    st.error("❌ No options match your constraints. Try raising your budget/time allowance or narrowing your charge target percent window.")
else:
    for idx, charger in enumerate(results, 1):
        status_text = "🟢 Full Target Achieved" if charger["outcome"] == "Yes" else f"🟡 Partial Completion ({charger['outcome']})"
        
        with st.expander(f"#{idx}: {charger['name']} ({charger['type']} {charger['power']}) — RM {charger['cost']:.2f}"):
            st.markdown(f"**Status:** {status_text}")
            
            if charger["slowed"] and charger["type"] == "DC":
                st.warning("⚠️ *The profile exceeded 80% SoC. The computation automatically calculated charging curve speed restrictions.*")
                
            c1, c2, c3 = st.columns(3)
            c1.metric("Est. Bill", f"RM {charger['cost']:.2f}")
            c2.metric("Energy Pumped", f"{charger['energy']:.2f} kWh")
            c3.metric("Time Duration", f"{charger['time']:.1f} mins")
            st.markdown(f"[📍 Open Map & View Station Info]({charger['link']})")

st.caption("ℹ️ Calculations assume a uniform average grid output voltage and prioritize cost efficiency rankings.")
