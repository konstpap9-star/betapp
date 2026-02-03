import streamlit as st
import random
from itertools import combinations

# 1. ΑΡΧΙΚΟΠΟΙΗΣΗ ΜΝΗΜΗΣ
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
if 'rand_key' not in st.session_state: st.session_state.rand_key = 0

st.set_page_config(page_title="BigBet Pro", layout="wide")

# 2. CSS ΓΙΑ ΧΡΩΜΑΤΑ & MOBILE FIX
st.markdown(f"""
    <style>
    .stApp {{ background-color: #E3F2FD; }}
    div[data-baseweb="select"] input {{ inputmode: none !important; caret-color: transparent !important; }}
    input {{ background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; font-weight: bold !important; }}
    div[data-baseweb="select"] > div {{ background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; }}
    .column-box {{ background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 5px solid #0D47A1; margin-bottom: 5px; font-family: monospace; font-size: 14px; }}
    .random-box {{ background-color: #FFF9C4; padding: 10px; border-radius: 5px; border-left: 5px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 5px; font-size: 14px; }}
    </style>
    """, unsafe_allow_html=True)

# 3. ΛΕΙΤΟΥΡΓΙΕΣ
def add_range():
    s, e = st.session_state.s, st.session_state.e
    if s.isdigit() and e.isdigit():
        for code in range(int(s), int(e) + 1):
            fmt = str(code).zfill(3)
            if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
                st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})

def randomize_action():
    pool = st.session_state.allowed_points if st.session_state.get('allowed_points') else st.session_state.options
    for i in range(len(st.session_state.my_bet)):
        st.session_state.my_bet[i]['Σ'] = random.choice(pool)
    # Αλλάζοντας αυτό το νούμερο, αναγκάζουμε το Streamlit να ξανασχεδιάσει τα selectboxes
    st.session_state.rand_key += 1

# 4. ΚΥΡΙΟ UI
st.title("🏆 BigBet Printer Pro")

# Ενότητα Εισαγωγής
with st.container():
    c1, c2 = st.columns(2)
