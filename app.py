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

# 3. CSS ΓΙΑ STYLING & ΚΡΥΦΟ ΠΛΗΚΤΡΟΛΟΓΙΟ
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    /* Mobile Keyboard Fix */
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
    e = st.session_state.e
    if s.isdigit() and e.isdigit():
        for code in range(int(s), int(e) + 1):
            fmt = str(code).zfill(3)
            if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
                st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})

def randomize_callback():
    pool = st.session_state.allowed_points if st.session_state.get('allowed_points') else st.session_state.options
    for i in range(len(st.session_state.my_bet)):
        rnd = random.choice(pool)
        # Ενημερώνουμε απευθείας το session state των selectboxes
        st.session_state[f"sel_{i}"] = rnd
        st.session_state.my_bet[i]['Σ'] = rnd

# 5. ΚΥΡΙΟ UI
st.title("🏆 BigBet Printer Pro")

with st.expander("🛠️ Ρυθμίσεις Εισαγωγής", expanded=True):
    c1, c2 = st.columns(2)
    c1.text_input("ΑΠΟ (Κωδικός)", key="s", max_chars=3)
    c2.text_input("ΕΩΣ (Κωδικός)", key="e", max_chars=3)
    st.button("ΠΡΟΣΘΗΚΗ ΕΥΡΟΥΣ ➕", on_click=add_range_callback, use_container_width=True)

    st.multiselect("🎯 Φίλτρο Τυχαίων Σημείων", options=st.session_state.options, key="allowed_points")
    
    if st.session_state.my_bet:
        st.button("🎲 ΤΥΧΑΙΑ ΣΥΜΠΛΗΡΩΣΗ ΣΕ ΟΛΑ", on_click=randomize_callback, use_container_width=True)

# --- ΛΙΣΤΑ ΑΓΩΝΩΝ ---
if st.session_state.my_bet:
    st.subheader(f"📍 Επιλεγμένοι Αγώνες ({len(st.session_state.my_bet)})")
    for i, item in enumerate(st.session_state.my_bet):
        col_k, col_s, col_d = st.columns([0.6, 2, 0.5])
        col_k.write(f"**{item['Κ']}**")
        
        # Το selectbox συνδέεται με το sel_i κλειδί
        choice = col_s.selectbox(
            f"Σημείο {i}", 
            st.session_state.options, 
            key=f"sel_{i}",
            label_visibility="collapsed"
        )
        # Ενημέρωση της λίστας my_bet για την ανάπτυξη
        st.session_state.my_bet[i]['Σ'] = choice
        
        if col_d.button("✕", key=f"del_{i}"):
            st.session_state.my_bet.pop(i)
            st.rerun()

# --- ΑΝΑΠΤΥΞΗ ΣΥΣΤΗΜΑΤΟΣ ---
if st.session_state.my_bet:
    st.divider()
    n = len(st.session_state.my_bet)
    k_sys = st.number_input("Ζητούμενα (Σύστημα)", 1, n, value=min(n, 3))
    
    # Παραγωγή συνδυασμών
    all_combos = list(combinations(st.session_state.my_bet, k_sys))
    st.info(f"Σύνολο: **{len(all_combos)} στήλες**")

    # Τυχαίες Στήλες
    if st.button("ΠΑΡΑΓΩΓΗ ΤΥΧΑΙΩΝ ΣΤΗΛΩΝ 🎰"):
        st.session_state.last_random_combos = random.sample(all_combos, min(len(all_combos), 10))

    if st.session_state.last_random_combos:
        st.write("🎰 **Τυχαίες Στήλες:**")
        for idx, combo in enumerate(st.session_state.last_random_combos):
            txt = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="random-box">Στήλη {idx+1}: {txt}</div>', unsafe_allow_html=True)

    # Πλήρης Ανάπτυξη
    with st.expander("🔍 Προβολή Πλήρους Ανάπτυξης"):
        for idx, combo in enumerate(all_combos):
            txt = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="column-box">Στήλη {idx+1}: {txt}</div>', unsafe_allow_html=True)

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ ΟΛΩΝ"):
        st.session_state.my_bet = []
        st.session_state.last_random_combos = []
        st.rerun()
