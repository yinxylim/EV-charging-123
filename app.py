import streamlit as st

# 1. PAGE CONFIG & MODERN STYLE INJECTION
st.set_page_config(
    page_title="Ultimate EV Optimizer", 
    page_icon="⚡", 
    layout="centered"
)

# Cleaned CSS (Fixes the TypeError crash while preserving the vibrant look)
st.markdown("""
    <style>
    /* Dark Slate Background */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Modern Bold Gradient Title */
    .main-title {
        font-size: 2.3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    
    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Premium Styling for Info/Metric Display Cards */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #38bdf8 !important;
    }
    
    /* Sleek container styles for user options */
    .stExpander {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Render Styled Headers
st.markdown('<h1 class="main-title">⚡ Ultimate EV Charger Optimizer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Subang Jaya Station Matcher & Smart Curve Simulator</p>', unsafe_allow_html=True)

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

STATIONS = [
    {"name": "Subang Parade (ParkEasy Hub)", "type": "AC", "power_kw": 22, "rate_per_kwh": 1.00, "rate_per_min": 0.0, "link": "https://www.plugshare.com/location/587223"},
    {"name": "Sunway Pyramid (ChargeSini Hub)", "type": "AC", "power_kw": 22, "rate_per_kwh": 0.00, "rate_per_min": 0.40, "link": "https://www.chargesini.com/"},
    {"name": "The Summit USJ (JomCharge)", "type": "DC", "power_kw": 60, "rate_per_kwh": 1.50, "rate_per_min": 0.0, "link": "https://cardog.app/tools/charging/my/subang-jaya-10"},
    {"name": "UOA Business Park Glenmarie (DC Handal)", "type": "DC", "power_kw": 200, "rate_per_kwh": 1.70, "rate_per_min": 0.0, "link": "https://cardog.app/tools/charging/my/subang-jaya-10"},
    {"name": "Shell Recharge Mint Hotel (High Speed)", "type": "DC", "power_kw": 180, "rate_per_kwh": 2.20, "rate_per_min": 0.0, "link": "https://www.gentari.com/go/charging-network/malaysia"}
]

# --- MAIN SCREEN INPUTS ---
st.markdown("### 🚗 Step 1: Select Your Vehicle Profile")
selected_brand = st.selectbox("Choose Model Variant", list(EV_MODELS.keys()))
default_specs = EV_MODELS[selected_brand]

# Expandable Fine-Tuning Box for enthusiasts
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
    energy, duration, cost, outcome, slowed = simulate_charging_session(
        station, current_soc, target_soc, max_ac_limit, max_dc_limit, battery_capacity, user_time_limit, user_budget
    )
    if duration > 0:
        results.append({
            "name": station["name"], "type": station["type"], "power": f"{station['power_kw']} kW",
            "energy": energy, "time": duration, "cost": cost, "outcome": outcome, "slowed": slowed, "link": station["link"]
        })

results = sorted(results, key=lambda x: x["cost"])

# --- DISPLAY OUTPUT RESULTS PANEL ---
st.markdown("### 🏆 Cost-Efficiency Station Rankings")

if not results:
    st.error("❌ No options match your boundaries. Try expanding your parameters or lowering your target battery goal percentage.")
else:
    for idx, charger in enumerate(results, 1):
        if charger["outcome"] == "Yes":
            badge = "🟢 **Full Goal Reached**"
        else:
            badge = f"🟡 **{charger['outcome']}**"
            
        with st.expander(f"#{idx}: {charger['name']} [{charger['type']} {charger['power']}] — RM {charger['cost']:.2f}"):
            st.markdown(f"⚡ **Status Indicator:** {badge}")
            
            if charger["slowed"] and charger["type"] == "DC":
                st.warning("⚠️ *Battery crossed 80%. Multi-stage speed throttling was applied automatically.*")
                
            m1, m2, m3 = st.columns(3)
            m1.metric("Est. Total Bill", f"RM {charger['cost']:.2f}")
            m2.metric("Energy Transferred", f"{charger['energy']:.2f} kWh")
            m3.metric("Required Stop Time", f"{charger['time']:.1f} mins")
            
            st.markdown(f"🎯 **[Tap to Open Navigation Map & Station Rules]({charger['link']})**")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>⚡ Built by an independent local developer. Save this link to calculate any road trip stop! ☕</p>", unsafe_allow_html=True)
