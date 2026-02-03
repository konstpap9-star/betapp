import streamlit as st
import math
import random
from itertools import combinations

# --- 1. ΑΡΧΙΚΟΠΟΙΗΣΗ ---
if 'options' not in st.session_state:
    st.session_state.options = [
        "1", "X", "2", "1X", "X2", "12", "G/G", "N/G", 
        "Over 1.5", "Under 1.5", "Over 2.5", "Under 2.5", "Over 3.5", "Under 3.5",
        "Γ Over 0.5", "Φ Over 0.5", "Γ Over 1.5", "Φ Over 1.5", 
        "Γ Over 2.5", "Φ Over 2.5", "Γ Over 3.5", "Φ Over 3.5",
        "Γ Under 0.5", "Φ Under 0.5", "Γ Under 1.5", "Φ Under 1.5", 
        "Γ Under 2.5", "Φ Under 2.5", "Γ Under 3.5", "Φ Under 3.5"
    ]

if 'last_random_combos' not in st.session_state:
    st.session_state.last_random_combos = []

if 'my_bet' not in st.session_state: 
    st.session_state.my_bet = []

# ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΤΥΧΑΙΑ ΣΥΜΠΛΗΡΩΣΗ ΣΗΜΕΙΩΝ
def randomize_all_selections():
    for i in range(len(st.session_state.my_bet)):
        random_choice = random.choice(st.session_state.options)
        st.session_state[f"sel_{i}"] = random_choice
        st.session_state.my_bet[i]['Σ'] = random_choice

st.set_page_config(page_title="Dinos Bet Pro", layout="wide")

# --- 2. CSS ΓΙΑ MOBILE & STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    /* Απενεργοποίηση πληκτρολογίου σε κινητά για τα Selectboxes */
    div[data-baseweb="select"] input { inputmode: none !important; caret-color: transparent !important; }
    
    input { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; font-weight: bold !important; }
    div[data-baseweb="select"] > div { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; }
    
    .column-box { 
        background-color: #f0f2f6; padding: 10px; border-radius: 5px; 
        font-family: monospace; font-size: 14px; margin-bottom: 5px; border-left: 5px solid #0D47A1;
    }
    .random-box { 
        background-color: #FFF9C4; padding: 10px; border-radius: 5px; 
        font-family: monospace; font-size: 14px; margin-bottom: 5px; border-left: 5px solid #FBC02D;
        color: #0D47A1; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ΛΟΓΟΤΥΠΟ ---
# Χρησιμοποιούμε το URL της εικόνας που δημιουργήσαμε
st.image("https://raw.githubusercontent.com/Google/gemini-assets/main/dinos_bet_logo.png", width=250) 
# Σημείωση: Αν την έχεις κατεβάσει τοπικά, άλλαξε το URL σε "dinos_logo.png"

# --- 4. ΕΙΣΑΓΩΓΗ ---
with st.container():
    c1, c2 = st.columns(2)
    with c1: s_range = st.text_input("ΑΠΟ", key="s", max_chars=3)
    with c2: e_range = st.text_input("ΕΩΣ", key="e", max_chars=3)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("ΠΡΟΣΘΗΚΗ ΕΥΡΟΥΣ ➕", use_container_width=True):
            if s_range.isdigit() and e_range.isdigit():
                for code in range(int(s_range), int(e_range) + 1):
                    fmt = str(code).zfill(3)
                    if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
                        st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})
                st.rerun()
    
    with col_btn2:
        if st.session_state.my_bet:
            if st.button("🎲 ΤΥΧΑΙΑ ΣΗΜΕΙΑ ΣΕ ΟΛΑ", on_click=randomize_all_selections, use_container_width=True):
                pass

    u_input = st.text_input("📍 ΚΩΔΙΚΟΣ", key="manual", max_chars=3)
    if len(u_input) == 3 and u_input.isdigit():
        if not any(x['Κ'] == u_input for x in st.session_state.my_bet):
            st.session_state.my_bet.append({"Κ": u_input, "Σ": "1"})
            st.rerun()

# --- 5. ΛΙΣΤΑ ΑΓΩΝΩΝ ---
st.subheader(f"Αγώνες: {len(st.session_state.my_bet)}")
for i, item in enumerate(st.session_state.my_bet):
    col_k, col_s, col_d = st.columns([0.6, 2, 0.5])
    with col_k: st.write(f"**{item['Κ']}**")
    with col_s:
        # Χρησιμοποιούμε το key για να επιτρέψουμε την αυτόματη ενημέρωση
        choice = st.selectbox("Σημείο", st.session_state.options, 
            key=f"sel_{i}", label_visibility="collapsed")
        st.session_state.my_bet[i]['Σ'] = choice
    with col_d:
        if st.button("✕", key=f"del_{i}"):
            st.session_state.my_bet.pop(i)
            st.rerun()

# --- 6. ΣΥΣΤΗΜΑ, ΤΥΧΑΙΑ & ΑΝΑΠΤΥΞΗ ---
if st.session_state.my_bet:
    st.divider()
    n = len(st.session_state.my_bet)
    k = st.number_input("Ζητούμενα (Σύστημα)", 1, n, min(n, 3) if n>=3 else 1)
    
    all_combos = list(combinations(st.session_state.my_bet, k))
    total_cols = len(all_combos)
    st.write(f"Σύνολο Πλήρους Ανάπτυξης: **{total_cols} στήλες**")

    # ΤΥΧΑΙΑ ΕΠΙΛΟΓΗ (ΜΟΝΙΜΑ ΟΡΑΤΗ)
    st.markdown("---")
    st.subheader("🎲 Παραγωγή Τυχαίων Στηλών")
    num_random = st.number_input("Πόσες τυχαίες στήλες θέλεις;", 1, total_cols, min(total_cols, 5))
    
    if st.button("ΠΑΡΑΓΩΓΗ ΤΥΧΑΙΩΝ ΣΤΗΛΩΝ 🎰"):
        st.session_state.last_random_combos = random.sample(all_combos, int(num_random))

    # Εμφάνιση των τυχαίων αν υπάρχουν
    if st.session_state.last_random_combos:
        st.write("**Οι Τυχαίες Στήλες σου:**")
        for idx, combo in enumerate(st.session_state.last_random_combos):
            txt = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="random-box">Στήλη {idx+1}: {txt}</div>', unsafe_allow_html=True)

    st.markdown("---")
    # ΠΛΗΡΗΣ ΑΝΑΠΤΥΞΗ
    with st.expander("🔍 Δες την Πλήρη Ανάπτυξη"):
        for idx, combo in enumerate(all_combos):
            txt = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="column-box">Στήλη {idx+1}: {txt}</div>', unsafe_allow_html=True)

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ ΟΛΩΝ"):
        st.session_state.my_bet = []
        st.session_state.last_random_combos = []
        st.rerun()
