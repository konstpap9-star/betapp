import streamlit as st
import random
from itertools import combinations

# 1. ΑΡΧΙΚΟΠΟΙΗΣΗ ΜΝΗΜΗΣ
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'last_random_combos' not in st.session_state: st.session_state.last_random_combos = []
if 'options' not in st.session_state:
    st.session_state.options = [
        "1", "X", "2", "1X", "X2", "12", "G/G", "N/G", 
        "Over 1.5", "Under 1.5", "Over 2.5", "Under 2.5", "Over 3.5", "Under 3.5",
        "Γ Over 0.5", "Φ Over 0.5", "Γ Over 1.5", "Φ Over 1.5", 
        "Γ Over 2.5", "Φ Over 2.5", "Γ Over 3.5", "Φ Over 3.5"
    ]

st.set_page_config(page_title="BigBet Pro", layout="wide")

# 2. CSS (ΧΡΩΜΑΤΑ & ΠΑΓΩΜΑ ΠΛΗΚΤΡΟΛΟΓΙΟΥ)
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    div[data-baseweb="select"] input { inputmode: none !important; caret-color: transparent !important; }
    input { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; font-weight: bold !important; }
    div[data-baseweb="select"] > div { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; }
    .column-box { background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 5px solid #0D47A1; margin-bottom: 5px; font-family: monospace; font-size: 14px; }
    .random-box { background-color: #FFF9C4; padding: 10px; border-radius: 5px; border-left: 5px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 5px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 BigBet Printer Pro")

# --- ΕΝΟΤΗΤΑ 1: ΕΙΣΑΓΩΓΗ ---
with st.container():
    col_r1, col_r2 = st.columns(2)
    s_range = col_r1.text_input("ΑΠΟ", key="s", max_chars=3)
    e_range = col_r2.text_input("ΕΩΣ", key="e", max_chars=3)

    if st.button("ΠΡΟΣΘΗΚΗ ΕΥΡΟΥΣ ➕", use_container_width=True):
        if s_range.isdigit() and e_range.isdigit():
            for code in range(int(s_range), int(e_range) + 1):
                fmt = str(code).zfill(3)
                if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
                    st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})
            st.rerun()

    # Χειροκίνητος Κωδικός με έλεγχο για να μην "παγώνει" τη σελίδα
    u_input = st.text_input("📍 ΚΩΔΙΚΟΣ (3 ψηφία)", key="manual", max_chars=3)
    if u_input and len(u_input) == 3 and u_input.isdigit():
        if not any(x['Κ'] == u_input for x in st.session_state.my_bet):
            st.session_state.my_bet.append({"Κ": u_input, "Σ": "1"})
            # Καθαρίζουμε το πεδίο χειροκίνητα για την επόμενη εισαγωγή
            st.session_state.manual = "" 
            st.rerun()

# --- ΕΝΟΤΗΤΑ 2: ΤΥΧΑΙΑ ΣΥΜΠΛΗΡΩΣΗ (Μόνο αν υπάρχ
