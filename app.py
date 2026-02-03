import streamlit as st
import random
from itertools import combinations

# 1. ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ
st.set_page_config(page_title="BigBet Pro", layout="wide")

# 2. ΑΡΧΙΚΟΠΟΙΗΣΗ SESSION STATE
if 'options' not in st.session_state:
    st.session_state.options = [
        "1", "X", "2", "1X", "X2", "12", "G/G", "N/G", 
        "Over 1.5", "Under 1.5", "Over 2.5", "Under 2.5", "Over 3.5", "Under 3.5",
        "Γ Over 0.5", "Φ Over 0.5", "Γ Over 1.5", "Φ Over 1.5", 
        "Γ Over 2.5", "Φ Over 2.5", "Γ Over 3.5", "Φ Over 3.5",
        "Γ Under 0.5", "Φ Under 0.5", "Γ Under 1.5", "Φ Under 1.5", 
        "Γ Under 2.5", "Φ Under 2.5", "Γ Under 3.5", "Φ Under 3.5"
    ]
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'last_random_combos' not in st.session_state: st.session_state.last_random_combos = []

# 3. CSS ΓΙΑ STYLING & MOBILE KEYBOARD FIX
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    /* Mobile Keyboard Fix: Εμποδίζει το πληκτρολόγιο στα selectboxes */
    div[data-baseweb="select"] input { inputmode: none !important; caret-color: transparent !important; }
    
    input { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; font-weight: bold !important; }
    div[data-baseweb="select"] > div { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; }
    
    .column-box { background-color: #f0f2f6; padding: 10px; border-radius: 5px; font-family: monospace; border-left: 5px solid #0D47A1; margin-bottom: 5px; font-size: 14px; }
    .random-box { background-color: #FFF9C4; padding: 10px; border-radius: 5px; font-family: monospace; border-left: 5px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 5px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# 4. ΣΥΝΑΡΤΗΣΕΙΣ (Callbacks)
def add_range_callback():
    s = st.session_state.s
