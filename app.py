import streamlit as st

# 1. READ URL PARAMETERS FOR LIVE GPS ACCURACY
query_params = st.query_params

if "lat" in query_params and "lon" in query_params:
    lat = float(query_params["lat"])
    lon = float(query_params["lon"])
    
    # Update title dynamically to show GPS status is ACTIVE
    st.title("Live GPS Matcher & Smart Curve Simulator")
    st.success(f"📍 Location Engine Activated! Connected at Latitude: {lat}, Longitude: {lon}")
else:
    # Fallback default title using the regional baseline location
    st.title("Subang Jaya Station Matcher & Smart Curve Simulator")
    st.info("👋 Simulating from default home base. Grant location permissions to toggle live tracking.")

st.markdown("---")

# 2. SPECIFY MG S5 EV LUX AS THE DEFAULT VEHICLE BRAND
st.subheader("🚗 Vehicle Configuration")

# Populate fields using the exact updated specifications for the Malaysian market
car_model = st.text_input("Car Model Brand", value="MG S5 EV (Lux CKD)")

col1, col2, col3 = st.columns(3)

with col1:
    battery_capacity = st.number_input(
        "Battery Capacity (kWh)", 
        value=62.0, 
        help="Equipped with the SAIC-CATL thin LFP battery pack."
    )
with col2:
    motor_power = st.number_input(
        "Motor Max Power (kW)", 
        value=151, 
        help="Upgraded rear-mounted traction motor pushing 205 PS / 151 kW."
    )
with col3:
    motor_torque = st.number_input(
        "Max Torque (Nm)", 
        value=350, 
        help="Peak torque output for the local CKD assembled variant."
    )

st.markdown(f"**Current Active Baseline:** `{car_model}` | `{battery_capacity} kWh` | `{motor_power} kW` | `{motor_torque} Nm` ")

# [Rest of your map matching / smart curve physics calculation logic continues down here...]
