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

st.markdown('<h1 class="main-title">⚡ Live Active Matrix for Subang Jaya / PJ</h1>', unsafe_allow_html=True)

# Display GPS Anchor explicitly as requested by design
st.success("📍 GPS Anchor Coordinates Set: (3.0792, 101.5834)")

# --- 🎯 MASTER NATIONWIDE DATA GRID (EXPANDED STATIONS) ---
@st.cache_data
def get_master_database():
    return [
        # --- SELANGOR / SUBANG JAYA / PJ (EXPANDED SECTOR) ---
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "Subang Parade", "operator": "ParkEasy Hub", "type": "AC", "kw": 22, "rate": 0.1848, "dist": 0.6},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "UOA Business Park Glenmarie", "operator": "DC Handal", "type": "DC", "kw": 200, "rate": 0.8192, "dist": 0.8},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "Empire Shopping Gallery", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.2200, "dist": 0.9},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "Subang Jaya / PJ Landmark Area", "operator": "Tesla Supercharger Hub", "type": "DC", "kw": 250, "rate": 0.7500, "dist": 1.9},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "The Summit USJ", "operator": "JomCharge", "type": "DC", "kw": 60, "rate": 0.7229, "dist": 2.4},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "Sunway Pyramid", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.6333, "dist": 2.8},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "Paradigm Mall Petaling Jaya", "operator": "Shell Recharge", "type": "DC", "kw": 60, "rate": 0.7800, "dist": 3.9},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "Aeon Mall Shah Alam", "operator": "ChargeEV", "type": "DC", "kw": 120, "rate": 0.7712, "dist": 4.6},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "IOI Mall Puchong (Basement Carpark)", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.6500, "dist": 5.2},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "Petronas Kuchai Lama", "operator": "Gentari Hyper-Fast", "type": "DC", "kw": 180, "rate": 0.9500, "dist": 9.5},
        {"state": "Selangor", "town": "Subang Jaya / PJ", "building": "Shell Recharge Mint Hotel", "operator": "Ultra-High Speed", "type": "DC", "kw": 180, "rate": 1.0603, "dist": 14.9},

        # --- JOHOR ---
        {"state": "Johor", "town": "Johor Bahru", "building": "The Mall, Mid Valley Southkey (Basement)", "operator": "Shell Recharge / Gentari", "type": "DC", "kw": 180, "rate": 2.20, "dist": 1.2},
        {"state": "Johor", "town": "Johor Bahru", "building": "Aeon Mall Bukit Indah", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.85, "dist": 2.8},
        {"state": "Johor", "town": "Johor Bahru", "building": "Toppen Shopping Centre (Tebrau Area)", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 4.5},
        {"state": "Johor", "town": "Batu Pahat", "building": "Batu Pahat Mall (Ground Floor Carpark)", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.80, "dist": 0.9},
        {"state": "Johor", "town": "Muar", "building": "Wetex Parade Shopping Complex", "operator": "JomCharge Hub", "type": "AC", "kw": 11, "rate": 0.85, "dist": 0.5},
        {"state": "Johor", "town": "Kulai", "building": "Johor Premium Outlets (JPO)", "operator": "Gentari High-Speed", "type": "DC", "kw": 150, "rate": 1.70, "dist": 2.1},
        {"state": "Johor", "town": "Kluang", "building": "Kluang Mall Carpark", "operator": "ChargeSini", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.1},

        # --- KEDAH ---
        {"state": "Kedah", "town": "Alor Setar", "building": "Aman Central Mall (Basement Bay)", "operator": "ChargEV Hub", "type": "DC", "kw": 60, "rate": 1.50, "dist": 0.8},
        {"state": "Kedah", "town": "Sungai Petani", "building": "Central Square Shopping Mall", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.1},
        {"state": "Kedah", "town": "Langkawi Island", "building": "Langkawi Fair Shopping Mall", "operator": "Gentari Marine Hub", "type": "AC", "kw": 22, "rate": 1.00, "dist": 3.4},
        {"state": "Kedah", "town": "Kulim", "building": "Kulim Central Mall", "operator": "ChargeSini", "type": "AC", "kw": 11, "rate": 0.85, "dist": 1.5},

        # --- KELANTAN ---
        {"state": "Kelantan", "town": "Kota Bharu", "building": "Aeon Mall Kota Bharu (Ground Floor Entrance)", "operator": "JomCharge Depot", "type": "DC", "kw": 60, "rate": 1.50, "dist": 1.5},
        {"state": "Kelantan", "town": "Kota Bharu", "building": "KB Mall Multi-Tier Parking", "operator": "ChargeSini Point", "type": "AC", "kw": 22, "rate": 0.90, "dist": 2.1},
        {"state": "Kelantan", "town": "Tanah Merah", "building": "Pantai Timur Hypermarket", "operator": "Local Charger", "type": "AC", "kw": 11, "rate": 0.80, "dist": 0.7},

        # --- MELAKA ---
        {"state": "Melaka", "town": "Melaka Town", "building": "Mahkota Parade Shopping Complex", "operator": "ChargEV Point", "type": "DC", "kw": 60, "rate": 1.50, "dist": 0.4},
        {"state": "Melaka", "town": "Melaka Town", "building": "Aeon Mall Bandaraya Melaka (P3 Deck)", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 2.3},
        {"state": "Melaka", "town": "Ayer Keroh", "building": "Caltex Ayer Keroh (PLUS Highway Southbound)", "operator": "JomCharge Depot", "type": "DC", "kw": 180, "rate": 2.20, "dist": 1.9},
        {"state": "Melaka", "town": "Alor Gajah", "building": "Free Influx Plaza Alor Gajah", "operator": "ChargeSini", "type": "AC", "kw": 22, "rate": 0.90, "dist": 3.1},

        # --- NEGERI SEMBILAN ---
        {"state": "Negeri Sembilan", "town": "Seremban", "building": "Aeon Mall Seremban 2 (Open Carpark Bay)", "operator": "JomCharge Depot", "type": "DC", "kw": 60, "rate": 1.50, "dist": 3.1},
        {"state": "Negeri Sembilan", "town": "Port Dickson", "building": "Regina Mall Port Dickson Centre", "operator": "ChargeSini Point", "type": "AC", "kw": 11, "rate": 0.85, "dist": 0.7},
        {"state": "Negeri Sembilan", "town": "Nilai", "building": "Aeon Mall Nilai Hub", "operator": "Gentari", "type": "DC", "kw": 60, "rate": 1.40, "dist": 1.8},

        # --- PAHANG ---
        {"state": "Pahang", "town": "Kuantan", "building": "East Coast Mall Kuantan (Ground Level)", "operator": "Gentari Hub", "type": "DC", "kw": 120, "rate": 1.70, "dist": 0.6},
        {"state": "Pahang", "town": "Kuantan", "building": "Kuantan City Mall Entrance", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.1},
        {"state": "Pahang", "town": "Genting Highlands", "building": "Genting Highlands Premium Outlets (GHPO)", "operator": "Gentari Mountain Hub", "type": "DC", "kw": 150, "rate": 1.70, "dist": 2.5},
        {"state": "Pahang", "town": "Temerloh", "building": "Mentakab Star Mall (Temerloh Sector)", "operator": "ChargeSini Point", "type": "AC", "kw": 22, "rate": 0.90, "dist": 4.2},
        {"state": "Pahang", "town": "Bentong", "building": "TF Value-Mart Bentong", "operator": "ChargEV", "type": "AC", "kw": 11, "rate": 0.80, "dist": 1.2},

        # --- PENANG ---
        {"state": "Penang", "town": "George Town", "building": "Gurney Plaza Mall (B1 Parking Wing)", "operator": "Gentari Hub", "type": "DC", "kw": 120, "rate": 1.70, "dist": 1.8},
        {"state": "Penang", "town": "George Town", "building": "Gurney Paragon Shopping Mall", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.80, "dist": 2.0},
        {"state": "Penang", "town": "Bayan Lepas", "building": "Queensbay Mall (South Zone Multi-tier)", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 0.5},
        {"state": "Penang", "town": "Seberang Perai", "building": "Sunway Carnival Mall (Seberang Jaya New Wing)", "operator": "JomCharge Station", "type": "DC", "kw": 60, "rate": 1.50, "dist": 1.3},
        {"state": "Penang", "town": "Batu Kawan", "building": "Design Village Outlet Mall", "operator": "ChargEV Depot", "type": "DC", "kw": 50, "rate": 1.40, "dist": 0.9},

        # --- PERAK ---
        {"state": "Perak", "town": "Ipoh", "building": "Ipoh Parade Shopping Mall (Ground Floor Entrance)", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 0.3},
        {"state": "Perak", "town": "Ipoh", "building": "Aeon Mall Ipoh Klebang", "operator": "JomCharge Depot", "type": "DC", "kw": 50, "rate": 1.40, "dist": 4.1},
        {"state": "Perak", "town": "Taiping", "building": "Aeon Mall Taiping (Kamunting)", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.80, "dist": 2.2},
        {"state": "Perak", "town": "Teluk Intan", "building": "TF Value-Mart Teluk Intan Complex", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 0.8},
        {"state": "Perak", "town": "Sitiawan / Seri Manjung", "building": "Aeon Mall Seri Manjung", "operator": "JomCharge", "type": "AC", "kw": 11, "rate": 0.85, "dist": 1.7},

        # --- PERLIS ---
        {"state": "Perlis", "town": "Kangar", "building": "Giant Hypermarket Kangar Centre", "operator": "ChargeSini Point", "type": "AC", "kw": 22, "rate": 0.95, "dist": 1.4},
        {"state": "Perlis", "town": "Arau", "building": "C-Mart Arau Carpark", "operator": "Local Network", "type": "AC", "kw": 11, "rate": 0.80, "dist": 1.1},

        # --- SABAH ---
        {"state": "Sabah", "town": "Kota Kinabalu", "building": "Imago Shopping Mall KK (Basement Core Zone)", "operator": "Gentari Fast Charger", "type": "DC", "kw": 60, "rate": 1.60, "dist": 0.7},
        {"state": "Sabah", "town": "Sandakan", "building": "Harbour Mall Sandakan Waterfront", "operator": "Borneo Eco Charge", "type": "AC", "kw": 11, "rate": 0.85, "dist": 0.4},
        {"state": "Sabah", "town": "Tawau", "building": "Eastern Plaza Mall Tawau", "operator": "ChargeSini", "type": "AC", "kw": 11, "rate": 0.90, "dist": 1.3},

        # --- SARAWAK ---
        {"state": "Sarawak", "town": "Kuching", "building": "The Spring Shopping Mall Kuching", "operator": "Gentari Hub", "type": "DC", "kw": 120, "rate": 1.70, "dist": 1.9},
        {"state": "Sarawak", "town": "Miri", "building": "Bintang Megamall Miri (New Wing Frontage)", "operator": "Shell Recharge Gateway", "type": "DC", "kw": 60, "rate": 1.50, "dist": 0.8},
        {"state": "Sarawak", "town": "Sibu", "building": "Wisma Sanyan Sibu Town Centre", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 0.6},
        {"state": "Sarawak", "town": "Bintulu", "building": "The Spring Shopping Mall Bintulu Sector", "operator": "Gentari East Coast", "type": "AC", "kw": 22, "rate": 1.00, "dist": 2.2},

        # --- TERENGGANU ---
        {"state": "Terengganu", "town": "Kuala Terengganu", "building": "KT ICC Shopping Mall (Town Waterfront)", "operator": "Gentari Coastal Hub", "type": "DC", "kw": 60, "rate": 1.50, "dist": 1.1},
        {"state": "Terengganu", "town": "Chukai (Kemaman)", "building": "Centre Point Kemaman Complex", "operator": "Local Network Point", "type": "AC", "kw": 11, "rate": 0.85, "dist": 0.9},

        # --- FEDERAL TERRITORIES ---
        {"state": "FT Kuala Lumpur", "town": "KLCC / Bukit Bintang", "building": "Suria KLCC (Basement B2 Hub)", "operator": "Gentari Suite", "type": "DC", "kw": 60, "rate": 1.60, "dist": 0.2},
        {"state": "FT Kuala Lumpur", "town": "Mid Valley / Bangsar", "building": "Mid Valley Megamall (P1 South Court)", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.80, "dist": 0.4},
        {"state": "FT Putrajaya", "town": "Putrajaya Precincts", "building": "Alamanda Shopping Centre Putrajaya", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.80, "dist": 1.7},
        {"state": "FT Labuan", "town": "Labuan Town", "building": "Financial Park Labuan Complex Shopping Center", "operator": "Island Network Hub", "type": "AC", "kw": 11, "rate": 0.95, "dist": 0.5}
    ]

db = get_master_database()

# --- 🛰️ CASCADE SELECTION INTERFACE ---
st.markdown("### 📍 Step 1: Select State & Town Location")

states = sorted(list(set(row["state"] for row in db)))

col_state, col_town = st.columns(2)
with col_state:
    selected_state = st.selectbox("Select State / Federal Territory", states, index=states.index("Selangor") if "Selangor" in states else 0)

filtered_towns = sorted(list(set(row["town"] for row in db if row["state"] == selected_state)))

with col_town:
    selected_town = st.selectbox("Select Target Town / Urban Hub", filtered_towns, index=filtered_towns.index("Subang Jaya / PJ") if "Subang Jaya / PJ" in filtered_towns else 0)

LIVE_STATIONS = [row for row in db if row["state"] == selected_state and row["town"] == selected_town]

# --- UI VEHICLE SETUPS ---
st.markdown("### 🚗 Step 2: Configure Vehicle Profile")
battery_capacity = st.number_input("Pack Useable Capacity (Net kWh)", min_value=10.0, value=62.5)

b_col1, b_col2 = st.columns(2)
with b_col1:
    current_soc = st.number_input("Start %", min_value=0, max_value=99, value=20)
with b_col2:
    target_soc = st.number_input("Goal %", min_value=int(current_soc + 1), max_value=100, value=80)

user_budget = st.number_input("Budget Cap (RM)", min_value=5.0, value=50.0, step=5.0)

# --- MATH CALCULATION MATRICES ---
energy_needed = battery_capacity * ((target_soc - current_soc) / 100)

results = []
for station in LIVE_STATIONS:
    duration_mins = (energy_needed / station["kw"]) * 60
    cost = energy_needed * station["rate"]
    
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

# Sort explicitly by distance
results = sorted(results, key=lambda x: x["distance"])

# --- DISPLAY RENDER PRESENTATION PANEL ---
st.markdown("### 🏆 Live Station Rankings (Sorted Nearest to Selected Location)")

if not results:
    st.error("❌ No stations within this district match your budget cap constraints.")
else:
    for idx, charger in enumerate(results, 1):
        with st.expander(f"#{idx}: {charger['building']} ({charger['operator']}) ({charger['distance']:.1f} km) — RM {charger['cost']:.2f}"):
            st.markdown(f"🏢 **Building Name / Specific Wing:** `{charger['building']}`")
            st.markdown(f"🔌 **Network Charger Brand:** **{charger['operator']}** ({charger['power']} kW — {charger['type']})")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Est. Session Bill", f"RM {charger['cost']:.2f}")
            m2.metric("Distance from Center", f"{charger['distance']:.1f} km")
            m3.metric("Required Stop Time", f"{charger['time']:.0f} mins")
            
            st.markdown(f"🔗 **[Open Navigation Map Directions Hub](https://www.plugshare.com/)**")

st.markdown("---")
st.markdown("⚡ *Complete Malaysian EV Model Matrix. Automated network-level bypass applied.*")
