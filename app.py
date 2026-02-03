import streamlit as st
import random
from itertools import combinations

# 1. ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ
st.set_page_config(page_title="BigBet Pro", layout="wide")

# 2. ΑΡΧΙΚΟΠΟΙΗΣΗ SESSION STATE (Για να μην χάνονται τα δεδομένα)
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

# 3. CSS ΓΙΑ ΚΙΤΡΙΝΑ ΠΕΔΙΑ & DISABLE KEYBOARD
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    div[data-baseweb="select"] input { inputmode: none !important; caret-color: transparent !important; }
    input { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; font-weight: bold !important; }
    div[data-baseweb="select"] > div { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; }
    .column-box { background-color: #f0f2f6; padding: 10px; border-radius: 5px; font-family: monospace; border-left: 5px solid #0D47A1; margin-bottom: 5px; }
    .random-box { background-color: #FFF9C4; padding: 10px; border-radius: 5px; font-family: monospace; border-left: 5px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 4. ΣΥΝΑΡΤΗΣΕΙΣ
def add_range():
    s = st.session_state.s
    e = st.session_state.e
    if s.isdigit() and e.isdigit():
        for code in range(int(s), int(e) + 1):
            fmt = str(code).zfill(3)
            if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
                st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})

def randomize_selections():
    # Παίρνει τα επιλεγμένα από το multiselect ή όλη τη λίστα
    pool = st.session_state.allowed_points if st.session_state.get('allowed_points') else st.session_state.options
    for i in range(len(st.session_state.my_bet)):
        rnd = random.choice(pool)
        st.session_state[f"sel_{i}"] = rnd
        st.session_state.my_bet[i]['Σ'] = rnd

# 5. UI - ΤΙΤΛΟΣ
st.title("🏆 BigBet Printer Pro")

# --- ΕΙΣΑΓΩΓΗ ---
with st.container():
    c1, c2 = st.columns(2)
    s_range = c1.text_input("ΑΠΟ", key="s", max_chars=3)
    e_range = c2.text_input("ΕΩΣ", key="e", max_chars=3)
    
    st.button("ΠΡΟΣΘΗΚΗ ΕΥΡΟΥΣ ➕", on_click=add_range, use_container_width=True)

    # ΦΙΛΤΡΟ ΤΥΧΑΙΑΣ ΕΠΙΛΟΓΗΣ
    st.multiselect(
        "🎯 Φίλτρο Τυχαίων (π.χ. διάλεξε 1, Χ, 2)",
        options=st.session_state.options,
        key="allowed_points"
    )
    
    if st.session_state.my_bet:
        st.button("🎲 ΤΥΧΑΙΑ ΣΥΜΠΛΗΡΩΣΗ", on_click=randomize_selections, use_container_width=True)

    u_input = st.text_input("📍 ΚΩΔΙΚΟΣ", key="manual", max_chars=3)
    if len(u_input) == 3 and u_input.isdigit():
        if not any(x['Κ'] == u_input for x in st.session_state.my_bet):
            st.session_state.my_bet.append({"Κ": u_input, "Σ": "1"})
            st.rerun()

# --- ΛΙΣΤΑ ΑΓΩΝΩΝ ---
st.subheader(f"Αγώνες: {len(st.session_state.my_bet)}")
for i, item in enumerate(st.session_state.my_bet):
    col_k, col_s, col_d = st.columns([0.6, 2, 0.5])
    col_k.write(f"**{item['Κ']}**")
