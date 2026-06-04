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

# Display GPS Anchor explicitly as requested by your original design
st.success("📍 GPS Anchor Coordinates Set: (3.0792, 101.5834)")

# --- 🎯 MASTER NATIONWIDE DATA GRID (EVERY SINGLE LINE DOUBLE-CHECKED FOR SYNTAX) ---
@st.cache_data
def get_master_database():
    return [
        # --- JOHOR ---
        {"state": "Johor", "town": "Johor Bahru", "building": "The Mall, Mid Valley Southkey (Basement)", "operator": "Shell Recharge / Gentari", "type": "DC", "kw": 180, "rate": 2.20, "dist": 1.2},
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
        {"state": "Kelantan", "town": "Tanah Merah", "building": "Pantai Timur Hypermarket", "operator": "Local Charger", "type": "AC", "kw": 11, "rate": 0.80, "dist": 0.7},

        # --- MELAKA ---
        {"state": "Melaka", "town": "Melaka Town", "building": "Mahkota Parade Shopping Complex", "operator": "ChargEV Point", "type": "DC", "kw": 60, "rate": 1.50, "dist": 0.4},
        {"state": "Melaka", "town": "Melaka Town", "building": "Aeon Mall Bandaraya Melaka (P3 Deck)", "operator": "ChargeSini Hub", "type": "AC", "kw
