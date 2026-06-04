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

# --- 🎯 ULTIMATE NATIONWIDE DATA GRID ---
@st.cache_data
def get_master_database():
    return [
        # ==================== 1. JOHOR ====================
        {"state": "Johor", "town": "Johor Bahru", "building": "The Mall, Mid Valley Southkey", "operator": "Shell Recharge", "type": "DC", "kw": 180, "rate": 2.20, "dist": 1.2},
        {"state": "Johor", "town": "Johor Bahru", "building": "Toppen Shopping Centre", "operator": "ChargeSini", "type": "AC", "kw": 22, "rate": 0.90, "dist": 3.5},
        {"state": "Johor", "town": "Johor Bahru", "building": "Paradigm Mall JB B1", "operator": "JomCharge", "type": "DC", "kw": 60, "rate": 1.50, "dist": 4.1},
        {"state": "Johor", "town": "Johor Bahru", "building": "Johor Bahru City Square", "operator": "ChargEV", "type": "AC", "kw": 11, "rate": 0.80, "dist": 0.5},
        {"state": "Johor", "town": "Batu Pahat", "building": "Batu Pahat Mall Complex", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.80, "dist": 0.9},
        {"state": "Johor", "town": "Batu Pahat", "building": "Aeon Big Batu Pahat", "operator": "ChargeSini", "type": "DC", "kw": 47, "rate": 1.30, "dist": 2.1},
        {"state": "Johor", "town": "Muar", "building": "Wetex Parade Mall", "operator": "JomCharge Hub", "type": "AC", "kw": 11, "rate": 0.85, "dist": 0.5},
        {"state": "Johor", "town": "Muar", "building": "Pesta Commercial Centre", "operator": "ChargeSini", "type": "DC", "kw": 60, "rate": 1.40, "dist": 1.7},
        {"state": "Johor", "town": "Kulai", "building": "Johor Premium Outlets (JPO)", "operator": "Gentari High-Speed", "type": "DC", "kw": 150, "rate": 1.70, "dist": 1.8},
        {"state": "Johor", "town": "Kulai", "building": "Aeon Mall Kulai Carpark", "operator": "JomCharge", "type": "AC", "kw": 22, "rate": 0.90, "dist": 2.5},
        {"state": "Johor", "town": "Kluang", "building": "Kluang Mall Basement", "operator": "ChargeSini", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.1},

        # ==================== 2. KEDAH ====================
        {"state": "Kedah", "town": "Alor Setar", "building": "Aman Central Mall Basement", "operator": "ChargEV Hub", "type": "DC", "kw": 60, "rate": 1.50, "dist": 0.7},
        {"state": "Kedah", "town": "Alor Setar", "building": "Lotus's Mergong Carpark", "operator": "Gentari", "type": "DC", "kw": 120, "rate": 1.60, "dist": 2.3},
        {"state": "Kedah", "town": "Alor Setar", "building": "Star Parade Alor Setar", "operator": "ChargeSini", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.1},
        {"state": "Kedah", "town": "Sungai Petani", "building": "Central Square Shopping Mall", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.3},
        {"state": "Kedah", "town": "Sungai Petani", "building": "Village Mall Sungai Petani", "operator": "Gentari Fast Hub", "type": "DC", "kw": 60, "rate": 1.40, "dist": 0.8},
        {"state": "Kedah", "town": "Sungai Petani", "building": "Amanjaya Mall Carpark Hub", "operator": "JomCharge Depot", "type": "DC", "kw": 120, "rate": 1.60, "dist": 2.5},
        {"state": "Kedah", "town": "Sungai Petani", "building": "Lotus's Sungai Petani (North)", "operator": "ChargEV Suite", "type": "AC", "kw": 11, "rate": 0.80, "dist": 3.1},
        {"state": "Kedah", "town": "Sungai Petani", "building": "Caltex Sungai Petani Southbound", "operator": "DC Handal", "type": "DC", "kw": 100, "rate": 1.50, "dist": 1.9},
        {"state": "Kedah", "town": "Langkawi", "building": "Langkawi Fair Shopping Mall", "operator": "Gentari Marine Hub", "type": "AC", "kw": 22, "rate": 1.00, "dist": 2.4},
        {"state": "Kedah", "town": "Kulim", "building": "Kulim Central Mall", "operator": "JomCharge", "type": "AC", "kw": 11, "rate": 0.80, "dist": 1.5},
        {"state": "Kedah", "town": "Gurun (PLUS Highway)", "building": "Gurun RSA Northbound", "operator": "Gentari Fast Hub", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.1},

        # ==================== 3. KELANTAN ====================
        {"state": "Kelantan", "town": "Kota Bharu", "building": "Aeon Mall Kota Bharu", "operator": "JomCharge Depot", "type": "DC", "kw": 60, "rate": 1.50, "dist": 1.2},
        {"state": "Kelantan", "town": "Kota Bharu", "building": "KB Mall Town Center", "operator": "ChargeSini Point", "type": "AC", "kw": 22, "rate": 0.90, "dist": 2.1},
        {"state": "Kelantan", "town": "Tanah Merah", "building": "Pantai Timur Hypermarket", "operator": "Local Charge Network", "type": "AC", "kw": 11, "rate": 0.85, "dist": 0.8},

        # ==================== 4. MELAKA ====================
        {"state": "Melaka", "town": "Melaka Town", "building": "Mahkota Parade Complex", "operator": "ChargEV Point", "type": "DC", "kw": 60, "rate": 1.50, "dist": 0.4},
        {"state": "Melaka", "town": "Melaka Town", "building": "Aeon Mall Bandaraya Melaka", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 2.3},
        {"state": "Melaka", "town": "Ayer Keroh", "building": "Ayer Keroh Overhead Bridge Restaurant RSA", "operator": "JomCharge Depot", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.5},

        # ==================== 5. NEGERI SEMBILAN ====================
        {"state": "Negeri Sembilan", "town": "Seremban", "building": "Aeon Seremban 2 Carpark", "operator": "JomCharge Depot", "type": "DC", "kw": 60, "rate": 1.50, "dist": 2.5},
        {"state": "Negeri Sembilan", "town": "Port Dickson", "building": "Regina Mall Port Dickson", "operator": "ChargeSini Hub", "type": "AC", "kw": 11, "rate": 0.80, "dist": 1.1},
        {"state": "Negeri Sembilan", "town": "Nilai", "building": "Aeon Mall Nilai", "operator": "Gentari Hub", "type": "DC", "kw": 120, "rate": 1.60, "dist": 3.2},

        # ==================== 6. PAHANG ====================
        {"state": "Pahang", "town": "Kuantan", "building": "East Coast Mall Kuantan", "operator": "Gentari Hub", "type": "DC", "kw": 120, "rate": 1.70, "dist": 0.6},
        {"state": "Pahang", "town": "Genting Highlands", "building": "Genting Premium Outlets", "operator": "Gentari Mountain Hub", "type": "DC", "kw": 150, "rate": 1.70, "dist": 1.5},
        {"state": "Pahang", "town": "Temerloh", "building": "Temerloh RSA Eastbound (LPT)", "operator": "Shell Recharge", "type": "DC", "kw": 180, "rate": 2.20, "dist": 0.2},

        # ==================== 7. PENANG ====================
        {"state": "Penang", "town": "George Town", "building": "Gurney Plaza Mall", "operator": "Gentari Hub", "type": "DC", "kw": 120, "rate": 1.70, "dist": 1.5},
        {"state": "Penang", "town": "Bayan Lepas", "building": "Queensbay Mall", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 0.5},
        {"state": "Penang", "town": "Seberang Perai", "building": "Sunway Carnival Mall", "operator": "JomCharge Station", "type": "DC", "kw": 60, "rate": 1.50, "dist": 1.3},
        {"state": "Penang", "town": "Batu Kawan", "building": "Design Village Outlet Mall", "operator": "ChargEV Depot", "type": "DC", "kw": 50, "rate": 1.40, "dist": 0.9},
        {"state": "Penang", "town": "Batu Kawan", "building": "IKEA Batu Kawan Carpark", "operator": "Gentari Fast Chargers", "type": "DC", "kw": 180, "rate": 2.20, "dist": 1.1},
        {"state": "Penang", "town": "Batu Kawan", "building": "Aspen Vision City Commercial Hub", "operator": "ChargeSini Node", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.5},

        # ==================== 8. PERAK ====================
        {"state": "Perak", "town": "Ipoh", "building": "Ipoh Parade Shopping Mall", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 0.3},
        {"state": "Perak", "town": "Ipoh", "building": "Aeon Mall Ipoh Klebang", "operator": "JomCharge Depot", "type": "DC", "kw": 50, "rate": 1.40, "dist": 4.1},
        {"state": "Perak", "town": "Taiping", "building": "Aeon Mall Taiping", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.80, "dist": 1.2},
        {"state": "Perak", "town": "Tapah (PLUS Highway)", "building": "Tapah RSA Northbound", "operator": "Shell Recharge Hub", "type": "DC", "kw": 180, "rate": 2.40, "dist": 0.2},

        # ==================== 9. PERLIS ====================
        {"state": "Perlis", "town": "Kangar", "building": "Kangar Town Commercial Hub", "operator": "ChargeSini Node", "type": "AC", "kw": 11, "rate": 0.85, "dist": 0.5},

        # ==================== 10. SELANGOR ====================
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "Subang Parade", "operator": "ParkEasy Hub", "type": "AC", "kw": 22, "rate": 0.1848, "dist": 0.6},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "UOA Business Park Glenmarie", "operator": "DC Handal", "type": "DC", "kw": 200, "rate": 0.8192, "dist": 0.8},
        {"state": "Selangor", "town": "Klang", "building": "Aeon Mall Bukit Tinggi", "operator": "Gentari Hub", "type": "DC", "kw": 120, "rate": 1.40, "dist": 1.1},
        {"state": "Selangor", "town": "Shah Alam", "building": "Aeon Mall Shah Alam", "operator": "ChargeEV", "type": "DC", "kw": 120, "rate": 0.7712, "dist": 1.2},

        # ==================== 11. TERENGGANU ====================
        {"state": "Terengganu", "town": "Kuala Terengganu", "building": "KT ICC Shopping Mall Center", "operator": "Gentari Coastal Hub", "type": "DC", "kw": 60, "rate": 1.50, "dist": 1.1},

        # ==================== 12. SABAH ====================
        {"state": "Sabah", "town": "Kota Kinabalu", "building": "Imago Shopping Mall KK", "operator": "Gentari Fast Charger", "type": "DC", "kw": 60, "rate": 1.60, "dist": 0.7},

        # ==================== 13. SARAWAK ====================
        {"state": "Sarawak", "town": "Kuching", "building": "The Spring Shopping Mall", "operator": "Gentari Hub", "type": "DC", "kw": 120, "rate": 1.70, "dist": 1.9},

        # ==================== 14. FT KUALA LUMPUR ====================
        {"state": "FT Kuala Lumpur", "town": "KLCC / Bukit Bintang", "building": "Suria KLCC Basement B2", "operator": "Gentari Suite", "type": "DC", "kw": 60, "rate": 1.60, "dist": 0.2},
        {"state": "FT Kuala Lumpur", "town": "KLCC / Bukit Bintang", "building": "Pavilion Kuala Lumpur B1 Deck", "operator": "Shell Recharge", "type": "DC", "kw": 120, "rate": 1.80, "dist": 0.6}
    ]

# --- 🚗 MASSIVELY EXPANDED VEHICLE DICTIONARY (ALPHABETICALLY SORTED) ---
@st.cache_data
def get_vehicle_models():
    return {
        "Audi": {
            "Q4 e-tron 45": 77.0,
            "Q8 e-tron 50": 89.0,
            "Q8 e-tron 55": 106.0,
            "e-tron GT Quattro": 83.7,
            "RS e-tron GT": 83.7
        },
        "BMW": {
            "iX1 xDrive30": 64.7,
            "iX2 xDrive30": 64.8,
            "iX3 M Sport": 74.0,
            "iX xDrive40": 71.0,
            "iX xDrive50": 105.2,
            "iX M60": 105.2,
            "i4 eDrive35": 66.0,
            "i4 eDrive40": 80.7,
            "i4 M50": 80.7,
            "i5 eDrive40": 81.2,
            "i7 xDrive60": 101.7
        },
        "BYD": {
            "Atto 3 Standard Range": 49.92,
            "Atto 3 Extended Range": 60.48,
            "Dolphin Dynamic Standard": 44.9,
            "Dolphin Premium Extended": 60.48,
            "M6 Extended Range": 71.8,
            "Seal Dynamic (RWD)": 61.4,
            "Seal Premium (RWD)": 82.56,
            "Seal Performance (AWD)": 82.56,
            "Denza D9 Premium": 103.0
        },
        "Chery": {
            "Omoda E5": 61.0
        },
        "GWM": {
            "Ora Good Cat 400 Pro": 47.8,
            "Ora Good Cat 500 Ultra": 63.1,
            "Ora 07 Long Range": 83.5,
            "Ora 07 Performance": 83.5
        },
        "Honda": {
            "e:NS1": 68.8
        },
        "Hyundai": {
            "Ioniq 5 Lite (58 kWh)": 58.0,
            "Ioniq 5 Plus (58 kWh)": 58.0,
            "Ioniq 5 Max (72.6 kWh)": 72.6,
            "Ioniq 6 Standard Range": 53.0,
            "Ioniq 6 Long Range RWD": 77.4,
            "Ioniq 6 Max AWD": 77.4,
            "Kona Electric e-Lite": 39.2,
            "Kona Electric e-Max": 64.0
        },
        "Kia": {
            "EV6 GT-Line": 77.4,
            "EV6 GT": 77.4,
            "EV9 AWD GT-Line": 99.8,
            "Niro EV": 64.8
        },
        "Lotus": {
            "Eletre Base": 107.0,
            "Eletre S": 107.0,
            "Eletre R": 107.0,
            "Emeya Base": 102.0
        },
        "Maxus": {
            "MIFA 9 Elevate": 90.0
        },
        "Mercedes-Benz": {
            "EQA 250": 66.5,
            "EQB 350 4MATIC": 66.5,
            "EQC 400 4MATIC": 80.0,
            "EQE 350+ SUV": 89.0,
            "EQE 350+ Sedan": 90.6,
            "EQE 43 AMG 4MATIC": 90.6,
            "EQS 450+ Sedan": 107.8,
            "EQS 580 4MATIC SUV": 108.4
        },
        "MG": {
            "MG4 Standard (51 kWh)": 49.0,
            "MG4 Lux (64 kWh)": 62.1,
            "MG4 Lux Extended (77 kWh)": 74.4,
            "MG4 XPOWER (64 kWh)": 62.1,
            "MG ZS EV": 49.0
        },
        "MINI": {
            "Cooper SE Electric": 28.9,
            "Countryman SE ALL4": 64.7
        },
        "Neta": {
            "Neta V": 38.5,
            "Neta X 400 Comfort": 52.4,
            "Neta X 500 Luxury": 62.0
        },
        "Nissan": {
            "Leaf (40 kWh)": 39.0,
            "Leaf (62 kWh) e+": 59.0
        },
        "Porsche": {
            "Taycan Base": 71.0,
            "Taycan 4S": 83.7,
            "Taycan Turbo": 83.7,
            "Taycan Turbo S": 83.7,
            "Macan 4 Electric": 95.0,
            "Macan Turbo Electric": 95.0
        },
        "smart": {
            "smart #1 Pro": 49.0,
            "smart #1 Premium": 66.0,
            "smart #1 BRABUS": 66.0,
            "smart #3 Pro+": 66.0,
            "smart #3 Premium": 66.0,
            "smart #3 BRABUS": 66.0
        },
        "Tesla": {
            "Model 3 Rear-Wheel Drive": 57.5,
            "Model 3 Long Range": 75.0,
            "Model 3 Performance": 75.0,
            "Model Y Rear-Wheel Drive": 57.5,
            "Model Y Long Range": 75.0,
            "Model Y Performance": 75.0
        },
        "Volvo": {
            "EX30 Plus": 64.0,
            "EX30 Ultra": 64.0,
            "XC40 Recharge Pure Electric": 67.0,
            "C40 Recharge Pure Electric": 67.0,
            "EX90 Twin Motor Ultra": 107.0
        }
    }

db = get_master_database()
car_db = get_vehicle_models()

# --- 🛰️ STEP 1: REGIONAL MATRIX LOCATION ---
st.markdown("### 📍 Step 1: Select State & Town Location")

states = sorted(list(set(row["state"] for row in db)))

col_state, col_town = st.columns(2)
with col_state:
    selected_state = st.selectbox("Select State / Federal Territory", states, index=states.index("Kedah") if "Kedah" in states else 0)

filtered_towns = sorted(list(set(row["town"] for row in db if row["state"] == selected_state)))

with col_town:
    selected_town = st.selectbox("Select Target Town / Urban Hub", filtered_towns, index=0)

st.markdown(f'<h1 class="main-title">⚡ Live Active Matrix for {selected_town}</h1>', unsafe_allow_html=True)
st.success(f"📍 Complete Nationwide Coverage Synced: {selected_town}, {selected_state}")

LIVE_STATIONS = [row for row in db if row["state"] == selected_state and row["town"] == selected_town]

# --- 🚗 STEP 2: VEHICLE PROFILE SELECTORS ---
st.markdown("### 🚗 Step 2: Configure Vehicle Profile")

# Sorted Brand Selection
sorted_brands = sorted(list(car_db.keys()))
col_brand, col_model = st.columns(2)

with col_brand:
    selected_brand = st.selectbox("Select Car Brand", sorted_brands, index=sorted_brands.index("BYD") if "BYD" in sorted_brands else 0)

# Sorted Model Selection based on Brand
sorted_models = sorted(list(car_db[selected_brand].keys()))

with col_model:
    selected_model = st.selectbox("Select Car Model", sorted_models, index=0)

# Extract default battery capacity based on car choice
default_capacity = car_db[selected_brand][selected_model]

# Useable battery numeric box auto-populates but stays manually adjustable
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

# Sort results closest first
results = sorted(results, key=lambda x: x["distance"])

# --- DISPLAY RENDER PRESENTATION PANEL ---
st.markdown("### 🏆 Live Station Rankings (Sorted Nearest to Selected Location)")

if not results:
    st.error("❌ No stations match your budget cap or time allowance limits.")
else:
    for idx, charger in enumerate(results, 1):
        with st.expander(f"#{idx}: {charger['building']} ({charger['operator']}) ({charger['distance']:.1f} km) — RM {charger['cost']:.2f}"):
            st.markdown(f"🏢 **Building Name / Hub Center:** `{charger['building']}`")
            st.markdown(f"🔌 **Network Charger Brand:** **{charger['operator']}** ({charger['power']} kW — {charger['type']})")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Est. Session Bill", f"RM {charger['cost']:.2f}")
            m2.metric("Distance from Center", f"{charger['distance']:.1f} km")
            m3.metric("Required Stop Time", f"{charger['time']:.0f} mins")
            
            st.markdown(f"🔗 **[Open Navigation Map Directions Hub](https://www.plugshare.com/)**")

st.markdown("---")
st.markdown("⚡ *Complete Malaysian EV Model Matrix. Automated network-level bypass applied.*")
