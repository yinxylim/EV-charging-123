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

# --- 🗺️ THE ABSOLUTE MASTER MALAYSIAN NATIONWIDE GEOGRAPHIC DATABASE ---
# Covers all 13 states + 3 Federal Territories with major commercial town hubs and actual buildings
NATIONWIDE_DATABASE = {
    "Johor": {
        "Johor Bahru": {
            "center": (1.4556, 103.7611),
            "stations": [
                {"building": "The Mall, Mid Valley Southkey (Basement)", "operator": "Shell Recharge / Gentari", "type": "DC", "kw": 180, "rate": 2.20},
                {"building": "Toppen Shopping Centre (Tebrau)", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90}
            ]
        },
        "Batu Pahat": {
            "center": (1.8500, 102.9300),
            "stations": [
                {"building": "Batu Pahat Mall (Ground Floor Carpark)", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.80},
                {"building": "Square One Shopping Mall", "operator": "ChargeSini", "type": "AC", "kw": 22, "rate": 0.90}
            ]
        },
        "Muar": {
            "center": (2.0400, 102.5600),
            "stations": [
                {"building": "Wetex Parade Shopping Complex", "operator": "JomCharge Hub", "type": "AC", "kw": 11, "rate": 0.85},
                {"building": "Shell Muar Bypass Station", "operator": "Shell Recharge", "type": "DC", "kw": 60, "rate": 1.50}
            ]
        },
        "Kulai / Iskandar Puteri": {
            "center": (1.6139, 103.6212),
            "stations": [
                {"building": "Johor Premium Outlets (JPO Entrance Plaza)", "operator": "Gentari High-Speed", "type": "DC", "kw": 150, "rate": 1.70},
                {"building": "Mall of Medini Nusajaya", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.80}
            ]
        }
    },
    "Kedah": {
        "Alor Setar": {
            "center": (6.1167, 100.3667),
            "stations": [
                {"building": "Aman Central Mall (Basement Bay)", "operator": "ChargEV Hub", "type": "DC", "kw": 60, "rate": 1.50},
                {"building": "Star Parade Mall Centre", "operator": "ChargeSini Point", "type": "AC", "kw": 22, "rate": 0.90}
            ]
        },
        "Sungai Petani": {
            "center": (5.6500, 100.4800),
            "stations": [
                {"building": "Central Square Shopping Mall", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90},
                {"building": "Village Mall Sungai Petani", "operator": "JomCharge Station", "type": "DC", "kw": 50, "rate": 1.40}
            ]
        },
        "Langkawi Island": {
            "center": (6.3265, 99.8514),
            "stations": [
                {"building": "Langkawi Fair Shopping Mall", "operator": "Gentari Marine Hub", "type": "AC", "kw": 22, "rate": 1.00},
                {"building": "The Danna Langkawi Luxury Resort", "operator": "ChargEV Point", "type": "AC", "kw": 11, "rate": 0.80}
            ]
        }
    },
    "Kelantan": {
        "Kota Bharu": {
            "center": (6.1333, 102.2500),
            "stations": [
                {"building": "Aeon Mall Kota Bharu (Ground Floor Entrance)", "operator": "JomCharge Depot", "type": "DC", "kw": 60, "rate": 1.50},
                {"building": "KB Mall Town Complex", "operator": "ChargeSini Point", "type": "AC", "kw": 22, "rate": 0.90}
            ]
        }
    },
    "Melaka": {
        "Melaka Town": {
            "center": (2.1889, 102.2511),
            "stations": [
                {"building": "Mahkota Parade Shopping Complex", "operator": "ChargEV Point", "type": "DC", "kw": 60, "rate": 1.50},
                {"building": "Aeon Mall Bandaraya Melaka (P3 Deck)", "operator": "ChargeSini Hub", "type": "AC", "kw": 22, "rate": 0.90},
                {"building": "Hatten Hotel Melaka City (Tower Block)", "operator": "Tesla Destination", "type": "AC", "kw": 11, "rate": 1.00}
            ]
        },
        "Ayer Keroh": {
            "center": (2.2764
