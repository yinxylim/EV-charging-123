import streamlit as st

# Page Setup
st.set_page_config(page_title="Advanced EV Optimizer", page_icon="⚡", layout="centered")
st.title("⚡ Advanced EV Charger Optimizer")
st.subheader("Subang Jaya Local Station Matcher with Real-World Fast Charge Curves")
st.write("Input your vehicle setup. The engine now calculates dynamic speed drops after hitting 80% SoC.")

# Preconfigured Malaysian EV Database
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

# Charging Point Operators Database
STATIONS = [
    {"name": "Subang Parade (ParkEasy Hub)", "type": "AC", "power_kw": 22, "rate_per_kwh": 1.00, "rate_per_min": 0.0, "link": "https://www.plugshare.com/location/587223"},
    {"name": "Sunway Pyramid (ChargeSini Hub)", "type": "AC", "power_kw": 22, "rate_per_kwh": 0.00, "rate_per_min": 0.40, "link": "https://www.chargesini.com/"},
    {"name": "The Summit USJ (JomCharge)", "type": "DC", "power_kw": 60, "rate_per_kwh": 1.50, "rate_per_min": 0.0, "link": "https://cardog.app/tools/charging/my/subang-jaya-10"},
    {"name": "UOA Business Park Glenmarie (DC Handal)", "type": "DC", "power_kw": 200, "rate_per_kwh": 1.70, "rate_per_min": 0.0, "link": "https://cardog.app/tools/charging/my/subang-jaya-10"},
    {"name": "Shell Recharge Mint Hotel (High Speed)", "type": "DC", "power_kw": 180, "rate_per_kwh": 2.20, "rate_per_min": 0.0, "link": "https://www.gentari.com/go/charging-network/malaysia"}
]

# Sidebar Inputs: Vehicle Specs
st.sidebar.header("🚗 1. Your Vehicle Details")
selected_brand = st.sidebar.selectbox("Select Car Brand / Variant", list(EV_MODELS.keys()))

default_specs = EV_MODELS[selected_brand]

if selected_brand == "Custom / Other Vehicle":
    battery_capacity = st.sidebar.number_input("Battery Size (Target kWh)", min_value=15.0, max_value=150.0, value=default_specs["battery_kwh"])
    max_ac_limit = st.sidebar.number_input("Max Car AC Limit (kW)", min_value=3.3, max_value=22.0, value=default_specs["max_ac_kw"])
    max_dc_limit = st.sidebar.number_input("Max Car DC Limit (kW)", min_value=20.0, max_value=350.0, value=default_specs["max_dc_kw"])
else:
    battery_capacity = default_specs["battery_kwh"]
    max_ac_limit = default_specs["max_ac_kw"]
    max_dc_limit = default_specs["max_dc_kw"]
    st.sidebar.info(f"📋 **Specs for {selected_brand}:**\n* Battery: {battery_capacity} kWh\n* Max AC: {max_ac_limit} kW\n* Max DC: {max_dc_limit} kW")

# Battery State Details
st.sidebar.header("🔋 2. Charge Target Profiles")
current_soc = st.sidebar.slider("Current Battery Level (%)", min_value=0, max_value=99, value=20)
target_soc = st.sidebar.slider("Target Battery Level (%)", min_value=current_soc + 1, max_value=100, value=90)

# Main Screen Constraints
st.write("---")
st.markdown("### ⏱️ Enter Current Session Constraints")
col1, col2 = st.columns(2)

with col1:
    user_time_limit = st.number_input("Max Waiting Time (Minutes)", min_value=10, max_value=480, value=45, step=5)
with col2:
    user_budget = st.number_input("Max Budget Limit (RM)", min_value=5.0, max_value=300.0, value=50.0, step=5.0)

# Helper function to calculate multi-stage charge time and true cost
def calculate_dynamic_charge(station, start_soc, end_soc, cap_ac, cap_dc, total_capacity, time_limit, budget_limit):
    current_soc_running = start_soc
    total_time_mins = 0.0
    total_energy_kwh = 0.0
    is_split_noted = False

    # Standardize time steps to small 1% battery increments for precise simulation
    while current_soc_running < end_soc:
        # Determine current charging speed cap based on battery percent threshold
        if station["type"] == "AC":
            current_speed = min(station["power_kw"], cap_ac)
        else: # DC Charging multi-stage charging curve implementation
            base_speed = min(station["power_kw"], cap_dc)
            if current_soc_running < 80:
                current_speed = base_speed
            elif 80 <= current_soc_running < 90:
                current_speed = base_speed * 0.50 # Step 1: Slow down by 50%
                is_split_noted = True
            else:
                current_speed = min(base_speed * 0.15, 11.0) # Step 2: Drop to a slow trickle cap

        # Energy required to move up exactly 1% SoC
        energy_step_kwh = total_capacity * 0.01
        time_step_mins = (energy_step_kwh / current_speed) * 60.0

        # Run boundary checks before committing the step
        projected_time = total_time_mins + time_step_mins
        projected_energy = total_energy_kwh + energy_step_kwh
        projected_cost = (projected_energy * station["rate_per_kwh"]) + (projected_time * station["rate_per_min"])

        if projected_time > time_limit or projected_cost > budget_limit:
            break # Halt simulation if limits are broken

        # Commit step metrics
        total_time_mins += time_step_mins
        total_energy_kwh += energy_step_kwh
        current_soc_running += 1

    final_cost = (total_energy_kwh * station["rate_per_kwh"]) + (total_time_mins * station["rate_per_min"])
    achieved_full = "Yes" if current_soc_running >= end_soc else f"Partial ({current_soc_running}%)"

    return total_energy_kwh, total_time_mins, final_cost, achieved_full, is_split_noted

# Run Logic
soc_to_add = target_soc - current_soc
theoretical_energy = battery_capacity * (soc_to_add / 100)
st.write(f"📊 **Session Objective:** Reach **{target_soc}%** from **{current_soc}%** (Needs roughly **{theoretical_energy:.2f} kWh**).")

results = []
for station in STATIONS:
    energy, duration, cost, status, hit_curve = calculate_dynamic_charge(
        station, current_soc, target_soc, max_ac_limit, max_dc_limit, battery_capacity, user_time_limit, user_budget
    )
    
    # Only show stations that gave you at least a minimal 1% charge within parameters
    if duration > 0:
        results.append({
            "name": station["name"],
            "type": station["type"],
            "power": f"{station['power_kw']} kW",
            "energy": energy,
            "time": duration,
            "cost": cost,
            "status": status,
            "hit_curve": hit_curve,
            "link": station["link"]
        })

results = sorted(results, key=lambda x: x["cost"])

# Display Content Output
st.write("---")
st.markdown("### 🏆 Filtered Matches Ranked by Cost Efficiency")

if not results:
    st.error("❌ No stations match your criteria under current time/budget caps. Try expanding limits or target less than 80%!")
else:
    for idx, charger in enumerate(results, 1):
        if "Partial" in charger["status"]:
            status_text = f"🟡 {charger['status']} — Timed Out / Budget Hit"
        else:
            status_text = "🟢 Full Target Reached"

        with st.expander(f"#{idx}: {charger['name']} ({charger['type']} {charger['power']}) — RM {charger['cost']:.2f}"):
            st.markdown(f"**Session Outcome:** {status_text}")
            
            if charger["hit_curve"] and charger["type"] == "DC":
                st.warning("⚠️ *Note: This session crossed past 80% battery capacity. The app factored in a significant automatic charging speed slowdown.*")

            col1, col2, col3 = st.columns(3)
            col1.metric("Calculated Cost", f"RM {charger['cost']:.2f}")
            col2.metric("Energy Delivered", f"{charger['energy']:.2f} kWh")
            col3.metric("Duration Required", f"{charger['time']:.1f} mins")
            
            st.markdown(f"[📍 Directions & Mapping Resources]({charger['link']})")

st.caption("ℹ️ Curve logic: AC power remains steady. DC speeds taper by 50% between 80-90% SoC, and drop down to cell-balancing levels past 90% SoC.")
