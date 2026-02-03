import streamlit as st
import random
from itertools import combinations

# --- 1. ΒΑΣΙΚΕΣ ΡΥΘΜΙΣΕΙΣ ---
st.set_page_config(page_title="BigBet Pro", layout="wide")

if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'last_random_combos' not in st.session_state: st.session_state.last_random_combos = []

# Σταθερή λίστα σημείων
OPTIONS = [
    "1", "X", "2", "1X", "X2", "12", "G/G", "N/G", 
    "Over 1.5", "Under 1.5", "Over 2.5", "Under 2.5", "Over 3.5", "Under 3.5",
    "Γ Over 0.5", "Φ Over 0.5", "Γ Over 1.5", "Φ Over 1.5"
]

# --- 2. CSS ΓΙΑ ΧΡΩΜΑΤΑ & MOBILE FIX ---
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    /* Mobile Keyboard Fix: Παγώνει το πληκτρολόγιο στα selectboxes */
    div[data-baseweb="select"] input { inputmode: none !important; caret-color: transparent !important; }
    input { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; font-weight: bold !important; }
    div[data-baseweb="select"] > div { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; }
    .column-box { background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 5px solid #0D47A1; margin-bottom: 5px; font-family: monospace; }
    .random-box { background-color: #FFF9C4; padding: 10px; border-radius: 5px; border-left: 5px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 BigBet Printer Pro")

# --- 3. ΕΝΟΤΗΤΑ ΕΙΣΑΓΩΓΗΣ ---
with st.sidebar:
    st.header("📍 Εισαγωγή Αγώνων")
    s_range = st.text_input("ΑΠΟ", key="s", max_chars=3)
    e_range = st.text_input("ΕΩΣ", key="e", max_chars=3)
    
    if st.button("ΠΡΟΣΘΗΚΗ ΕΥΡΟΥΣ ➕", use_container_width=True):
        if s_range.isdigit() and e_range.isdigit():
            for code in range(int(s_range), int(e_range) + 1):
                fmt = str(code).zfill(3)
                if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
                    st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})
            st.rerun()
    
    st.divider()
    u_input = st.text_input("ΜΕΜΟΝΩΜΕΝΟΣ ΚΩΔΙΚΟΣ", key="manual", max_chars=3)
    if len(u_input) == 3 and u_input.isdigit():
        if not any(x['Κ'] == u_input for x in st.session_state.my_bet):
            st.session_state.my_bet.append({"Κ": u_input, "Σ": "1"})
            st.rerun()

# --- 4. ΚΥΡΙΟ ΠΑΝΕΛ ---
if not st.session_state.my_bet:
    st.info("👈 Ξεκινήστε προσθέτοντας κωδικούς από το πλάι!")
else:
    # ΤΥΧΑΙΑ ΣΥΜΠΛΗΡΩΣΗ
    st.subheader("🎲 Τυχαία Επιλογή")
    allowed = st.multiselect("Φίλτρο Σημείων (π.χ. 1, X, 2):", OPTIONS, key="allowed_points")
    
    if st.button("🎲 ΤΥΧΑΙΑ ΣΥΜΠΛΗΡΩΣΗ ΣΕ ΟΛΟΥΣ ΤΟΥΣ ΑΓΩΝΕΣ", use_container_width=True):
        pool = allowed if allowed else OPTIONS
        for i in range(len(st.session_state.my_bet)):
            st.session_state.my_bet[i]['Σ'] = random.choice(pool)
        st.rerun()

    st.divider()

    # ΛΙΣΤΑ ΑΓΩΝΩΝ
    st.subheader("📋 Λίστα Αγώνων")
    for i in range(len(st.session_state.my_bet)):
        item = st.session_state.my_bet[i]
        c1, c2, c3 = st.columns([0.5, 2, 0.5])
        c1.write(f"**{item['Κ']}**")
        
        # Selectbox που αλλάζει βάσει της λίστας
        new_val = c2.selectbox(f"Σ_{item['Κ']}_{i}", OPTIONS, 
                               index=OPTIONS.index(item['Σ']) if item['Σ'] in OPTIONS else 0,
                               key=f"box_{item['Κ']}_{i}", label_visibility="collapsed")
        st.session_state.my_bet[i]['Σ'] = new_val
        
        if c3.button("✕", key=f"del_{i}"):
            st.session_state.my_bet.pop(i)
            st.rerun()

    # ΑΝΑΠΤΥΞΗ
    st.divider()
    k_sys = st.number_input("Σύστημα (π.χ. 3άδες, 4άδες)", 1, len(st.session_state.my_bet), value=min(len(st.session_state.my_bet), 3))
    all_combos = list(combinations(st.session_state.my_bet, k_sys))
    
    st.write(f"Σύνολο Στηλών: **{len(all_combos)}**")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("🎰 ΤΥΧΑΙΕΣ ΣΤΗΛΕΣ"):
            st.session_state.last_random_combos = random.sample(all_combos, min(len(all_combos), 10))
    with col_r2:
        if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ ΟΛΩΝ"):
            st.session_state.my_bet = []
            st.session_state.last_random_combos = []
            st.rerun()

    if st.session_state.last_random_combos:
        st.write("🎰 **Τυχαίες Στήλες:**")
        for combo in st.session_state.last_random_combos:
            txt = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="random-box">{txt}</div>', unsafe_allow_html=True)

    with st.expander("🔍 Δες όλη την Ανάπτυξη"):
        for combo in all_combos:
            txt = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="column-box">{txt}</div>', unsafe_allow_html=True)
