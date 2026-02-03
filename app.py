import streamlit as st
import math
import random
from itertools import combinations

# 1. ΣΤΑΘΕΡΗ ΛΙΣΤΑ ΣΗΜΕΙΩΝ
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

st.set_page_config(page_title="BigBet Pro", layout="wide")

# 2. CSS ΓΙΑ MOBILE KEYBOARD FIX & ΚΙΤΡΙΝΑ ΠΕΔΙΑ
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    /* Mobile Keyboard Fix */
    div[data-baseweb="select"] input { inputmode: none !important; caret-color: transparent !important; }
    input { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; font-weight: bold !important; }
    div[data-baseweb="select"] > div { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; }
    .column-box { background-color: #f0f2f6; padding: 10px; border-radius: 5px; font-family: monospace; border-left: 5px solid #0D47A1; margin-bottom: 5px; }
    .random-box { background-color: #FFF9C4; padding: 10px; border-radius: 5px; font-family: monospace; border-left: 5px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. ΛΕΙΤΟΥΡΓΙΑ ΤΥΧΑΙΑΣ ΕΠΙΛΟΓΗΣ
def randomize_all():
    # Χρησιμοποιεί τα επιλεγμένα από το multiselect ή όλα αν είναι κενό
    pool = st.session_state.allowed_points if st.session_state.get('allowed_points') else st.session_state.options
    for i in range(len(st.session_state.my_bet)):
        st.session_state.my_bet[i]['Σ'] = random.choice(pool)

st.title("🏆 BigBet Printer Pro")

# --- ΕΙΣΑΓΩΓΗ ---
c1, c2 = st.columns(2)
with c1: s_range = st.text_input("ΑΠΟ", key="s", max_chars=3)
with c2: e_range = st.text_input("ΕΩΣ", key="e", max_chars=3)

if st.button("ΠΡΟΣΘΗΚΗ ΕΥΡΟΥΣ ➕"):
    if s_range.isdigit() and e_range.isdigit():
        for code in range(int(s_range), int(e_range) + 1):
            fmt = str(code).zfill(3)
            if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
                st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})
        st.rerun()

u_input = st.text_input("📍 ΚΩΔΙΚΟΣ", key="manual", max_chars=3)
if len(u_input) == 3 and u_input.isdigit():
    if not any(x['Κ'] == u_input for x in st.session_state.my_bet):
        st.session_state.my_bet.append({"Κ": u_input, "Σ": "1"})
        st.rerun()

# --- ΤΥΧΑΙΑ ΦΙΛΤΡΑ ---
if st.session_state.my_bet:
    st.divider()
    st.multiselect("🎯 Διάλεξε σημεία για την Τύχη (π.χ. 1, Χ, 2)", options=st.session_state.options, key="allowed_points")
    if st.button("🎲 ΤΥΧΑΙΑ ΣΥΜΠΛΗΡΩΣΗ ΑΓΩΝΩΝ"):
        randomize_all()
        st.rerun()

# --- ΛΙΣΤΑ ΑΓΩΝΩΝ ---
st.subheader(f"Αγώνες: {len(st.session_state.my_bet)}")
for i, item in enumerate(st.session_state.my_bet):
    col_k, col_s, col_d = st.columns([0.6, 2, 0.5])
    with col_k: st.write(f"**{item['Κ']}**")
    with col_s:
        choice = st.selectbox(f"Σ_{item['Κ']}", st.session_state.options, 
            index=st.session_state.options.index(item['Σ']) if item['Σ'] in st.session_state.options else 0,
            key=f"sel_{i}", label_visibility="collapsed")
        st.session_state.my_bet[i]['Σ'] = choice
    with col_d:
        if st.button("✕", key=f"del_{i}"):
            st.session_state.my_bet.pop(i)
            st.rerun()

# --- ΑΝΑΠΤΥΞΗ ---
if st.session_state.my_bet:
    st.divider()
    n = len(st.session_state.my_bet)
    k = st.number_input("Ζητούμενα", 1, n, min(n, 3) if n>=3 else 1)
    all_combos = list(combinations(st.session_state.my_bet, k))
    
    st.write(f"Σύνολο: **{len(all_combos)} στήλες**")
    
    if st.button("ΠΑΡΑΓΩΓΗ ΤΥΧΑΙΩΝ 🎰"):
        st.session_state.last_random_combos = random.sample(all_combos, min(len(all_combos), 10))

    if st.session_state.last_random_combos:
        for idx, combo in enumerate(st.session_state.last_random_combos):
            txt = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="random-box">Τυχαία {idx+1}: {txt}</div>', unsafe_allow_html=True)

    with st.expander("🔍 Πλήρης Ανάπτυξη"):
        for idx, combo in enumerate(all_combos):
            txt = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="column-box">Στήλη {idx+1}: {txt}</div>', unsafe_allow_html=True)

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ"):
        st.session_state.my_bet = []
        st.session_state.last_random_combos = []
        st.rerun()
