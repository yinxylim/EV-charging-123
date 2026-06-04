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

st.markdown('<h1 class="main-title">⚡ Malaysia Master EV Navigator</h1>', unsafe_allow_html=True)

# --- 🎯 MASTER FLATTENED NATIONWIDE DATA GRID (NO NESTING SYNTAX TRAPS) ---
@st.cache_data
def get_master_database():
    return [
        # --- JOHOR ---
        {"state": "Johor", "town": "Johor Bahru", "center": (1.4556, 103.7611), "building": "The Mall, Mid Valley Southkey (Basement)", "operator": "Shell Recharge / Gentari", "type": "DC", "kw": 180, "rate": 2.20, "dist": 1.2},
        {"state": "Johor", "town": "Johor Bahru", "center": (1.4556, 103.7611), "building": "Toppen Shopping Centre (Tebrau Area)", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 4.5},
        {"state": "Johor", "town": "Batu Pahat", "center": (1.8500, 102.9300), "building": "Batu Pahat Mall (Ground Floor Carpark)", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.80, "dist": 0.9},
        {"state": "Johor", "town": "Muar", "center": (2.0400, 102.5600), "building": "Wetex Parade Shopping Complex", "operator": "JomCharge Hub", "type": "AC", "kw": 11, "rate": 0.85, "dist": 0.5},
        {"state": "Johor", "town": "Kulai / Iskandar Puteri", "center": (1.6139, 103.6212), "building": "Johor Premium Outlets (JPO Plaza Entrance)", "operator": "Gentari High-Speed", "type": "DC", "kw": 150, "rate": 1.70, "dist": 2.1},

        # --- KEDAH ---
        {"state": "Kedah", "town": "Alor Setar", "center": (6.1167, 100.3667), "building": "Aman Central Mall (Basement Bay)", "operator": "ChargEV Hub", "type": "DC", "kw": 60, "rate": 1.50, "dist": 0.8},
        {"state": "Kedah", "town": "Sungai Petani", "center": (5.6500, 100.4800), "building": "Central Square Shopping Mall", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 1.1},
        {"state": "Kedah", "town": "Langkawi Island", "center": (6.3265, 99.8514), "building": "Langkawi Fair Shopping Mall", "operator": "Gentari Marine Hub", "type": "AC", "kw": 22, "rate": 1.00, "dist": 3.4},

        # --- KELANTAN ---
        {"state": "Kelantan", "town": "Kota Bharu", "center": (6.1333, 102.2500), "building": "Aeon Mall Kota Bharu (Ground Floor Entrance)", "operator": "JomCharge Depot", "type": "DC", "kw": 60, "rate": 1.50, "dist": 1.5},

        # --- MELAKA ---
        {"state": "Melaka", "town": "Melaka Town", "center": (2.1889, 102.2511), "building": "Mahkota Parade Shopping Complex", "operator": "ChargEV Point", "type": "DC", "kw": 60, "rate": 1.50, "dist": 0.4},
        {"state": "Melaka", "town": "Melaka Town", "center": (2.1889, 102.2511), "building": "Aeon Mall Bandaraya Melaka (P3 Deck)", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90, "dist": 2.3},
        {"state": "Melaka", "town": "Ayer Keroh", "center": (2.2764, 102.2858), "building": "Caltex Ayer Keroh (PLUS Highway Southbound)", "operator": "JomCharge Depot", "type": "DC", "kw": 180, "rate": 2.20, "dist": 1.9},

        # --- NEGERI SEMBILAN ---
        {"state": "Negeri Sembilan", "town": "Seremban", "center": (2.7297, 101.9381), "building": "Aeon Mall Seremban 2 (Open Carpark Bay)", "operator": "JomCharge Depot", "type": "DC", "kw": 60, "rate": 1.50, "dist": 3.1},
        {"state": "Negeri Sembilan", "town": "Port Dickson", "center": (2.5222, 101.7975), "building": "Regina Mall Port Dickson Centre", "operator": "ChargeSini Point", "type": "AC", "kw": 11, "rate": 0.85, "dist": 0.7},

        # --- PAHANG ---
        {"state": "Pahang", "town": "Kuantan", "center": (3.8167, 103.3333), "building": "East Coast Mall Kuantan (Ground Level)", "operator": "Gentari Hub", "type": "DC", "kw": 120, "rate": 1.70, "dist": 0.6},
        {"state": "Pahang", "town": "Genting Highlands", "center": (3.4236, 101.7942), "building": "Genting Highlands Premium Outlets (GHPO)", "operator": "Gentari Mountain Hub", "type": "DC", "kw": 150, "rate": 1.70, "dist": 2.5},
        {"state": "Pahang", "town": "Temerloh", "center": (3.4478, 102.4175), "building": "Mentakab Star Mall (Temerloh Sector)", "operator": "ChargeSini Point", "type": "AC", "kw": 22, "rate":
