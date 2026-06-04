import streamlit as st

# 1. PAGE CONFIG & DESIGN
st.set_page_config(page_title="Malaysia EV Navigator", page_icon="⚡", layout="centered")

# --- 🎯 MASTER DATABASE (INTEGRATED & CATEGORIZED) ---
@st.cache_data
def get_master_database():
    return [
        # --- HIGHWAY CORRIDORS ---
        {"cat": "Highway Corridor", "state": "Johor", "town": "PLUS Highway (South)", "building": "Pagoh RSA Northbound (TNB Electron)", "kw": 180, "rate": 2.20},
        {"cat": "Highway Corridor", "state": "Perak", "town": "PLUS Highway (North)", "building": "Tapah RSA Northbound (TNB Electron)", "kw": 180, "rate": 2.20},
        {"cat": "Highway Corridor", "state": "Pahang", "town": "LPT East Coast", "building": "Temerloh RSA Eastbound (TNB Electron)", "kw": 180, "rate": 2.20},
        
        # --- TOWN/CITY LOCATIONS (Fully Restored) ---
        {"cat": "Town/City", "state": "Johor", "town": "Johor Bahru", "building": "Mid Valley Southkey (Shell)", "kw": 180, "rate": 2.20},
        {"cat": "Town/City", "state": "Penang", "town": "Batu Kawan", "building": "Design Village Outlet (ChargEV)", "kw": 50, "rate": 1.40},
        {"cat": "Town/City", "state": "Kedah", "town": "Sungai Petani", "building": "Central Square Mall (ChargeSini)", "kw": 22, "rate": 0.90},
        {"cat": "Town/City", "state": "FT Kuala Lumpur", "town": "Kuala Lumpur", "building": "Suria KLCC (Gentari)", "kw": 60, "rate": 1.60},
        {"cat": "Town/City", "state": "Selangor", "town": "Subang Jaya", "building": "Subang Parade (ParkEasy)", "kw": 22, "rate": 0.18},
        {"cat": "Town/City", "state": "Sabah", "town": "Kota Kinabalu", "building": "Imago Mall (Gentari)", "kw": 60, "rate": 1.60},
        {"cat": "Town/City", "state": "Sarawak", "town": "Kuching", "building": "The Spring Mall (Gentari)", "kw": 120, "rate": 1.70}
    ]

# --- NAVIGATION LOGIC ---
db = get_master_database()

st.markdown("### 📍 Location Filter")
category = st.radio("Select Navigation Type", ["Town/City", "Highway Corridor"])

cat_db = [d for d in db if d["cat"] == category]
states = sorted(list(set(d["state"] for d in cat_db)))
selected_state = st.selectbox("Select State", states)

towns = sorted(list(set(d["town"] for d in cat_db if d["state"] == selected_state)))
selected_town = st.selectbox("Select Town/Highway Section", towns)

# Display Logic
st.write(f"### Results for {selected_town}, {selected_state}")
filtered_results = [d for d in cat_db if d["state"] == selected_state and d["town"] == selected_town]

for item in filtered_results:
    st.info(f"**{item['building']}** | Power: {item['kw']}kW | Rate: RM{item['rate']}/kWh")
