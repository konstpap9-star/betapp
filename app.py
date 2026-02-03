import streamlit as st
import math
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

st.set_page_config(page_title="BigBet Full Pro", layout="wide")

# 2. CSS για Mobile & Κίτρινα Πεδία
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    input { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; font-weight: bold !important; }
    div[data-baseweb="select"] > div { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; }
    .stButton>button { width: 100%; }
    .column-box { 
        background-color: #f0f2f6; padding: 10px; border-radius: 5px; 
        font-family: monospace; font-size: 14px; margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'my_bet' not in st.session_state: st.session_state.my_bet = []

st.title("🏆 BigBet Printer Pro")

# --- ΕΙΣΑΓΩΓΗ ---
with st.container():
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

# --- ΛΙΣΤΑ ---
st.subheader(f"Αγώνες: {len(st.session_state.my_bet)}")

# Δείχνουμε τη λίστα
for i, item in enumerate(st.session_state.my_bet):
    col_k, col_s, col_d = st.columns([0.6, 2, 0.5])
    with col_k: st.write(f"**{item['Κ']}**")
    with col_s:
        choice = st.selectbox(
            "Σημείο", st.session_state.options, 
            index=st.session_state.options.index(item['Σ']) if item['Σ'] in st.session_state.options else 0,
            key=f"sel_{i}", label_visibility="collapsed"
        )
        st.session_state.my_bet[i]['Σ'] = choice
    with col_d:
        if st.button("✕", key=f"del_{i}"):
            st.session_state.my_bet.pop(i)
            st.rerun()

# --- ΣΥΣΤΗΜΑ & ΑΝΑΠΤΥΞΗ ---
if st.session_state.my_bet:
    st.divider()
    n = len(st.session_state.my_bet)
    k = st.number_input("Ζητούμενα (Σύστημα)", 1, n, min(n, 3) if n>=3 else 1)
    
    # Υπολογισμός Συνδυασμών
    combos = list(combinations(st.session_state.my_bet, k))
    st.write(f"Σύνολο Στηλών: **{len(combos)}**")
    
    # Εμφάνιση Ανάπτυξης
    with st.expander("🔍 Δες την Ανάπτυξη των Στηλών"):
        for idx, combo in enumerate(combos):
            codes = [c['Κ'] for c in combo]
            signs = [c['Σ'] for c in combo]
            txt = " | ".join([f"{c}({s})" for c, s in zip(codes, signs)])
            st.markdown(f'<div class="column-box">Στήλη {idx+1}: {txt}</div>', unsafe_allow_html=True)

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ ΟΛΩΝ"):
        st.session_state.my_bet = []
        st.rerun()
