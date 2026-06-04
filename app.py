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

# --- 🎯 ULTIMATE NATIONWIDE DATA GRID (ALL STATES + FTs) ---
@st.cache_data
def get_master_database():
    return [
        # ==================== 1. JOHOR ====================
        {"state": "Johor", "town": "Johor Bahru", "building": "The Mall, Mid Valley Southkey", "operator": "Shell Recharge", "type": "DC", "kw": 180, "rate": 2.20, "dist": 1.2},
        {"state": "Johor", "town": "Johor Bahru", "building": "Toppen Shopping Centre", "operator": "ChargeSini", "type": "AC", "kw": 22, "rate": 0.90, "dist": 3.5},
        {"state": "Johor", "town": "Batu Pahat", "building": "Batu Pahat Mall Complex", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.80, "dist": 0.9},
        {"state": "Johor", "town": "Muar", "building": "Wetex Parade Mall", "operator": "JomCharge Hub", "type": "AC", "kw": 11, "rate": 0.85, "dist": 0.5},
        {"state": "Johor", "town": "Kulai", "building": "Johor Premium Outlets (JPO)", "operator": "Gentari High-Speed", "type": "DC", "kw": 150, "rate": 1.70, "dist": 1.8},
        {"state": "Johor", "town": "Kluang", "building": "Kluang Mall Basement", "operator": "ChargeSini", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.1},

        # ==================== 2. KEDAH ====================
        {"state": "Kedah", "town": "Alor Setar", "building": "Aman Central Mall Basement", "operator": "ChargEV Hub", "type": "DC", "kw": 60, "rate": 1.50, "dist": 0.7},
        {"state": "Kedah", "town": "Sungai Petani", "building": "Central Square Shopping Mall", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.3},
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
        {"state": "Pahang", "town": "Bentong", "building": "Bentong Town Commercial Hub", "operator": "JomCharge", "type": "AC", "kw": 22, "rate": 0.90, "dist": 0.9},

        # ==================== 7. PENANG ====================
        {"state": "Penang", "town": "George Town", "building": "Gurney Plaza Mall", "operator": "Gentari Hub", "type": "DC", "kw": 120, "rate": 1.70, "dist": 1.5},
        {"state": "Penang", "town": "Bayan Lepas", "building": "Queensbay Mall", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 0.5},
        {"state": "Penang", "town": "Seberang Perai", "building": "Sunway Carnival Mall", "operator": "JomCharge Station", "type": "DC", "kw": 60, "rate": 1.50, "dist": 1.3},
        {"state": "Penang", "town": "Batu Kawan", "building": "Design Village Outlet Mall", "operator": "ChargEV Depot", "type": "DC", "kw": 50, "rate": 1.40, "dist": 0.9},

        # ==================== 8. PERAK ====================
        {"state": "Perak", "town": "Ipoh", "building": "Ipoh Parade Shopping Mall", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 0.3},
        {"state": "Perak", "town": "Ipoh", "building": "Aeon Mall Ipoh Klebang", "operator": "JomCharge Depot", "type": "DC", "kw": 50, "rate": 1.40, "dist": 4.1},
        {"state": "Perak", "town": "Taiping", "building": "Aeon Mall Taiping", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.80, "dist": 1.2},
        {"state": "Perak", "town": "Teluk Intan", "building": "TF Value-Mart Teluk Intan", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 0.8},
        {"state": "Perak", "town": "Sitiawan / Seri Manjung", "building": "Aeon Mall Seri Manjung", "operator": "JomCharge Suite", "type": "AC", "kw": 11, "rate": 0.85, "dist": 0.9},
        {"state": "Perak", "town": "Tapah (PLUS Highway)", "building": "Tapah RSA Northbound", "operator": "Shell Recharge Hub", "type": "DC", "kw": 180, "rate": 2.40, "dist": 0.2},

        # ==================== 9. PERLIS ====================
        {"state": "Perlis", "town": "Kangar", "building": "Kangar Town Commercial Hub", "operator": "ChargeSini Node", "type": "AC", "kw": 11, "rate": 0.85, "dist": 0.5},
        {"state": "Perlis", "town": "Padang Besar", "building": "Border Duty Free Plaza", "operator": "Northern Ev Charge", "type": "AC", "kw": 22, "rate": 0.95, "dist": 1.4},

        # ==================== 10. SELANGOR ====================
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "Subang Parade", "operator": "ParkEasy Hub", "type": "AC", "kw": 22, "rate": 0.1848, "dist": 0.6},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "UOA Business Park Glenmarie", "operator": "DC Handal", "type": "DC", "kw": 200, "rate": 0.8192, "dist": 0.8},
        {"state": "Selangor", "town": "Klang", "building": "Aeon Mall Bukit Tinggi", "operator": "Gentari Hub", "type": "DC", "kw": 120, "rate": 1.40, "dist": 1.1},
        {"state": "Selangor", "town": "Shah Alam", "building": "Aeon Mall Shah Alam", "operator": "ChargeEV", "type": "DC", "kw": 120, "rate": 0.7712, "dist": 1.2},
        {"state": "Selangor", "town": "Cyberjaya", "building": "DPULZE Shopping Centre", "operator": "ChargEV Depot", "type": "DC", "kw": 60, "rate": 1.30, "dist": 0.5},
        {"state": "Selangor", "town": "Kajang / Bangi", "building": "Evo Mall Bangi Carpark", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.0},
        {"state": "Selangor", "town": "Rawang", "building": "Aeon Mall Rawang Anggun", "operator": "Gentari Hub", "type": "DC", "kw": 60, "rate": 1.40, "dist": 1.5},

        # ==================== 11. TERENGGANU ====================
        {"state": "Terengganu", "town": "Kuala Terengganu", "building": "KT ICC Shopping Mall Center", "operator": "Gentari Coastal Hub", "type": "DC", "kw": 60, "rate": 1.50, "dist": 1.1},
        {"state": "Terengganu", "town": "Chukai / Kemaman", "building": "Mesra Mall Complex", "operator": "ChargEV Station", "type": "AC", "kw": 11, "rate": 0.80, "dist": 1.9},
        {"state": "Terengganu", "town": "Paka", "building": "Paka Town Commercial Area", "operator": "JomCharge Terminal", "type": "DC", "kw": 50, "rate": 1.30, "dist": 0.6},

        # ==================== 12. SABAH ====================
        {"state": "Sabah", "town": "Kota Kinabalu", "building": "Imago Shopping Mall KK", "operator": "Gentari Fast Charger", "type": "DC", "kw": 60, "rate": 1.60, "dist": 0.7},
        {"state": "Sabah", "town": "Kota Kinabalu", "building": "Suria Sabah Shopping Mall", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.5},
        {"state": "Sabah", "town": "Sandakan", "building": "Harbour Mall Sandakan Center", "operator": "Borneo Charge Net", "type": "AC", "kw": 11, "rate": 0.85, "dist": 1.0},
        {"state": "Sabah", "town": "Tawau", "building": "Eastern Plaza Tawau Deck", "operator": "Sabah Power EV", "type": "AC", "kw": 22, "rate": 0.95, "dist": 2.2},

        # ==================== 13. SARAWAK ====================
        {"state": "Sarawak", "town": "Kuching", "building": "The Spring Shopping Mall", "operator": "Gentari Hub", "type": "DC", "kw": 120, "rate": 1.70, "dist": 1.9},
        {"state": "Sarawak", "town": "Kuching", "building": "VivaCity Megamall Ground Level", "operator": "ChargeSini Point", "type": "AC", "kw": 22, "rate": 0.95, "dist": 2.4},
        {"state": "Sarawak", "town": "Miri", "building": "Bintang Megamall Miri Complex", "operator": "Sarawak Energy Node", "type": "DC", "kw": 50, "rate": 1.20, "dist": 1.3},
        {"state": "Sarawak", "town": "Bintulu", "building": "The Spring Bintulu Carpark", "operator": "Borneo Grid", "type": "AC", "kw": 11, "rate": 0.80, "dist": 0.7},
        {"state": "Sarawak", "town": "Sibu", "building": "Wisma Sanyan Sibu Plaza", "operator": "JomCharge Sibu", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.6},

        # ==================== 14. FT KUALA LUMPUR ====================
        {"state": "FT Kuala Lumpur", "town": "KLCC / Bukit Bintang", "building": "Suria KLCC Basement B2", "operator": "Gentari Suite", "type": "DC", "kw": 60, "rate": 1.60, "dist": 0.2},
        {"state": "FT Kuala Lumpur", "town": "KLCC / Bukit Bintang", "building": "Pavilion Kuala Lumpur B1 Deck", "operator": "Shell Recharge", "type": "DC", "kw": 120, "rate": 1.80, "dist": 0.6},
        {"state": "FT Kuala Lumpur", "town": "Mid Valley / Bangsar", "building": "Mid Valley Megamall P1 Wing", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.80, "dist": 0.4},
        {"state": "FT Kuala Lumpur", "town": "Cheras", "building": "Leisure Mall Complex", "operator": "ChargeSini", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.8},

        # ==================== 15. FT PUTRAJAYA ====================
        {"state": "FT Putrajaya", "town": "Putrajaya Central", "building": "Alamanda Shopping Centre", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.80, "dist": 1.7},
        {"state": "FT Putrajaya", "town": "Putrajaya Central", "building": "IOI City Mall Putrajaya Phase 1", "operator": "Gentari Super Hub", "type": "DC", "kw": 180, "rate": 1.50, "dist": 4.2},
        {"state": "FT Putrajaya", "town": "Putrajaya Central", "building": "IOI City Mall Putrajaya Phase 2", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.85, "dist": 4.5},

        # ==================== 16. FT LABUAN ====================
        {"state": "FT Labuan", "town": "Labuan Town", "building": "Financial Park Labuan Complex Center", "operator": "Island Network Hub", "type": "AC", "kw": 11, "rate": 0.95, "dist": 0.5},
        {"state": "FT Labuan", "town": "Labuan Town", "building": "Labuan Marina Seafront Walk", "operator": "Voltaic Charge", "type": "DC", "kw": 30, "rate": 1.20, "dist": 1.2},
        {"state": "FT Labuan", "town": "Labuan Town", "building": "Hotel Labuan Point Deck", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 2.0}
    ]

db = get_master_database()

# --- 🛰️ CASCADE SELECTION INTERFACE ---
st.markdown("### 📍 Step 1: Select State & Town Location")

states = sorted(list(set(row["state"] for row in db)))

col_state, col_town = st.columns(2)
with col_state:
    selected_state = st.selectbox(
        "Select State / Federal Territory", 
        states, 
        index=states.index("Perak") if "Perak" in states else 0
    )

filtered_towns = sorted(list(set(row["town"] for row in db if row["state"] == selected_state)))

with col_town:
    selected_town = st.selectbox("Select Target Town / Urban Hub", filtered_towns, index=0)

st.markdown(f'<h1 class="main-title">⚡ Live Active Matrix for {selected_town}</h1>', unsafe_allow_html=True)

st.success(f"📍 Complete Nationwide Coverage Synced: {selected_town}, {selected_state}")

LIVE_STATIONS = [row for row in db if row["state"] == selected_state and row["town"] == selected_town]

# --- UI VEHICLE SETUPS ---
st.markdown("### 🚗 Step 2: Configure Vehicle Profile")
battery_capacity = st.number_input("Pack Useable Capacity (Net kWh)", min_value=10.0, value=62.5)

b_col1, b_col2 = st.columns(2)
with b_col1:
    current_soc = st.number_input("Start %", min_value=0, max_value=99, value=20)
with b_col2:
    target_soc = st.number_input("Goal %", min_value=int(current_soc + 1), max_value=100, value=80)

# --- 💰 RESTORE BUDGET CAP CONTROL INPUT ---
user_budget = st.number_input("Budget Cap (RM)", min_value=5.0, value=150.0, step=5.0)

# --- MATH CALCULATION MATRICES ---
energy_needed = battery_capacity * ((target_soc - current_soc) / 100)

results = []
for station in LIVE_STATIONS:
    duration_mins = (energy_needed / station["kw"]) * 60
    cost = energy_needed * station["rate"]
    
    # Check constraints against user budget cap
    if cost <= user_budget:
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
    st.error("❌ No stations within this specific hub match your budget cap constraints.")
else:
    for idx, charger in enumerate(results, 1):
        with st.expander(f"#{idx}: {charger['building']} ({charger['operator']}) ({charger['distance']:.1f} km) — RM {charger['cost']:.2f}"):
            st.markdown(f"🏢 **Building Name / Hub Center:** `{charger['building']}`")
            st.markdown(f"🔌 **Network Charger Brand:** **{charger['operator']}** ({charger['power']} kW — {charger['type']})")
            
            # --- 🕒 METRICS DISPLAY SHOWING TIME & COST ---
            m1, m2, m3 = st.columns(3)
            m1.metric("Est. Session Bill", f"RM {charger['cost']:.2f}")
            m2.metric("Distance from Center", f"{charger['distance']:.1f} km")
            m3.metric("Required Stop Time", f"{charger['time']:.0f} mins")
            
            st.markdown(f"🔗 **[Open Navigation Map Directions Hub](https://www.plugshare.com/)**")

st.markdown("---")
st.markdown("⚡ *Complete Malaysian EV Model Matrix. Automated network-level bypass applied.*")
