import streamlit as st
import random
from itertools import combinations

# 1. ΑΡΧΙΚΟΠΟΙΗΣΗ
if 'options' not in st.session_state:
    st.session_state.options = ["1", "X", "2", "1X", "X2", "12", "G/G", "N/G", "Over 2.5", "Under 2.5"] # Συντομευμένη για δοκιμή
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'last_random_combos' not in st.session_state: st.session_state.last_random_combos = []

st.set_page_config(page_title="BigBet Pro", layout="wide")

# 2. CSS (Keyboard Fix & Style)
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    div[data-baseweb="select"] input { inputmode: none !important; }
    input { background-color: #FFF9C4 !important; font-weight: bold !important; }
    .column-box { background-color: #f0f2f6; padding: 8px; border-radius: 5px; border-left: 5px solid #0D47A1; margin-bottom: 4px; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# 3. ΛΕΙΤΟΥΡΓΙΕΣ
def add_new_code(code_str):
    fmt = code_str.zfill(3)
    if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
        st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})

def randomize_now():
    pool = st.session_state.get('allowed_points', [])
    if not pool: pool = st.session_state.options
    for i in range(len(st.session_state.my_bet)):
        st.session_state.my_bet[i]['Σ'] = random.choice(pool)

# 4. UI
st.title("🏆 BigBet Printer Pro")

# Είσοδος Κωδικών
u_input = st.text_input("📍 ΔΩΣΕ ΚΩΔΙΚΟ (π.χ. 101)", max_chars=3)
if len(u_input) == 3 and u_input.isdigit():
    add_new_code(u_input)
    # Καθαρισμός του input μετά την προσθήκη δεν γίνεται εύκολα στο streamlit χωρίς key, 
    # οπότε απλά συνεχίζουμε.

# Τυχαία Συμπλήρωση
if st.session_state.my_bet:
    st.multiselect("🎯 Διάλεξε σημεία για την τύχη:", st.session_state.options, key="allowed_points")
    if st.button("🎲 ΤΥΧΑΙΑ ΣΥΜΠΛΗΡΩΣΗ ΑΓΩΝΩΝ"):
        randomize_now()
        st.rerun()

st.divider()

# Λίστα Αγώνων
for i in range(len(st.session_state.my_bet)):
    item = st.session_state.my_bet[i]
    c1, c2, c3 = st.columns([1, 3, 1])
    c1.write(f"**{item['Κ']}**")
    
    # Εδώ είναι το μυστικό: Χρησιμοποιούμε το index βασισμένο στην τρέχουσα τιμή της λίστας
    current_index = st.session_state.options.index(item['Σ']) if item['Σ'] in st.session_state.options else 0
    
    new_selection = c2.selectbox(
        f"Σημείο για {item['Κ']}", 
        st.session_state.options, 
        index=current_index,
        key=f"box_{item['Κ']}_{i}", # Δυναμικό key που αλλάζει αν χρειαστεί
        label_visibility="collapsed"
    )
    st.session_state.my_bet[i]['Σ'] = new_selection
    
    if c3.button("✕", key=f"del_{i}"):
        st.session_state.my_bet.pop(i)
        st.rerun()

# Ανάπτυξη
if st.session_state.my_bet:
    st.divider()
    all_combos = list(combinations(st.session_state.my_bet, 3)) # Παράδειγμα για 3άδες
    st.write(f"Σύνολο 3άδων: {len(all_combos)}")
    
    with st.expander("🔍 Δες τις στήλες"):
        for combo in all_combos:
            txt = " - ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="column-box">{txt}</div>', unsafe_allow_html=True)
    
    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ"):
        st.session_state.my_bet = []
        st.rerun()
