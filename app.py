import streamlit as st
import math
import random
from itertools import combinations
import streamlit.components.v1 as components

# Ρυθμίσεις σελίδας
st.set_page_config(page_title="BigBet White Edition", layout="wide")

# --- CSS ΓΙΑ ΓΑΛΑΖΙΟ ΦΟΝΤΟ ΚΑΙ ΛΕΥΚΑ ΠΛΑΙΣΙΑ ---
st.markdown("""
    <style>
    /* Φόντο σελίδας ανοιχτό γαλάζιο */
    .stApp { 
        background-color: #E3F2FD; 
    }
    
    /* ΟΛΑ ΤΑ ΠΛΑΙΣΙΑ ΛΕΥΚΑ */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #FFFFFF !important; 
        border-radius: 15px; 
        padding: 15px; 
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }
    
    /* Λευκό φόντο και στα εσωτερικά widgets */
    .stSelectbox, .stNumberInput, .stTextInput, .stMetric {
        background-color: #FFFFFF !important;
    }

    /* Πλαίσιο εισαγωγής κωδικού */
    div.stTextInput > div > div > input {
        font-size: 28px !important; text-align: center !important; font-weight: bold !important; 
        color: #0D47A1 !important; background-color: #FFFFFF !important; 
        border: 3px solid #1976D2 !important; height: 60px !important;
    }

    /* Ο ΧΡΥΣΟΣ ΜΕΤΡΗΤΗΣ */
    .total-matches-label {
        font-size: 32px !important; font-weight: 900 !important; color: #0D47A1 !important; 
        text-align: center; margin: 15px 0px; padding: 20px;
        background-color: #FFD700 !important; border: 3px solid #DAA520; border-radius: 15px;
    }

    /* Λευκό φόντο στις αναλυτικές στήλες */
    .stText { 
        background-color: #FFFFFF !important; 
        padding: 10px; border-radius: 8px; 
        color: #1A1A1A !important; font-weight: bold; 
        border-left: 6px solid #FFD700; 
        border: 1px solid #E0E0E0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- JAVASCRIPT ΓΙΑ AUTO-ENTER ---
components.html(
    """
    <script>
    function setup() {
        const doc = window.parent.document;
        doc.addEventListener('keyup', function(e) {
            const activeInput = doc.activeElement;
            if (activeInput && activeInput.tagName === 'INPUT' && activeInput.value.length === 3) {
                activeInput.dispatchEvent(new KeyboardEvent('keydown', {'key': 'Enter', 'bubbles': true}));
                activeInput.dispatchEvent(new Event('change', {'bubbles': true}));
            }
        });
    }
    setTimeout(setup, 1000);
    </script>
    """, height=0,
)

# Αρχικοποίηση
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

st.title("🏆 BigBet Pro Tool")

# --- 1. ΕΙΣΑΓΩΓΗ ---
current_key = f"in_{st.session_state.input_counter}"
user_input = st.text_input("ΕΙΣΑΓΩΓΗ 3ΨΗΦΙΟΥ", key=current_key, max_chars=3)

# --- 2. ΜΕΤΡΗΤΗΣ ---
num_matches = len(st.session_state.my_bet)
st.markdown(f'<div class="total-matches-label">ΣΥΝΟΛΟ ΑΓΩΝΩΝ: {num_matches}</div>', unsafe_allow_html=True)

if len(user_input) == 3 and user_input.isdigit():
    st.session_state.my_bet.append({"Κ": user_input, "Σ": "1"})
    st.session_state.input_counter += 1
    st.rerun()

# --- 3. ΔΙΑΧΕΙΡΙΣΗ ---
if st.session_state.my_bet:
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        st.subheader("📋 Λίστα")
        m_opts = ["1", "X", "2", "G/G", "N/G", "Over 2.5", "Under 2.5", "1X", "X2"]
        for i in range(len(st.session_state.my_bet)-1, -1, -1):
            item = st.session_state.my_bet[i]
            c1, c2, c3 = st.columns([1, 2, 0.5])
            with c1: st.write(f"**{item['Κ']}**")
            with c2: st.session_state.my_bet[i]['Σ'] = st.selectbox(f"s_{i}", m_opts, key=f"sel_{i}", index=m_opts.index(item['Σ']), label_visibility="collapsed")
            with c3:
                if st.button("❌", key=f"d_{i}"):
                    st.session_state.my_bet.pop(i)
                    st.rerun()

    with col_r:
        st.subheader("🔢 Σύστημα")
        n = len(st.session_state.my_bet)
        k = st.number_input("Ζητούμενα:", 1, max(1, n), min(n, 3))
        
        total = math.comb(n, k)
        st.metric("Συνολικές Στήλες", f"{total:,}")
        
        if total > 0:
            mode = st.radio("Εμφάνιση:", ["Όλες", "Τυχαίες"], horizontal=True)
            if mode == "Τυχαίες":
                num = st.number_input("Πόσες στήλες;", 1, total, min(total, 10))
                if st.button("Παραγωγή ✨"):
                    all_c = list(combinations(st.session_state.my_bet, k))
                    selected = random.sample(all_c, num)
                    for idx, c in enumerate(selected, 1):
                        st.text(f"{idx}. {' · '.join([f'{x['Κ']}[{x['Σ']}]' for x in c])}")
            else:
                if total <= 500:
                    if st.checkbox("🔍 Εμφάνιση Αναλυτικά"):
                        for idx, c in enumerate(combinations(st.session_state.my_bet, k), 1):
                            st.text(f"{idx}. {' · '.join([f'{x['Κ']}[{x['Σ']}]' for x in c])}")
                else:
                    st.warning("⚠️ Πολλές στήλες (>500).")

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ ΟΛΩΝ"):
        st.session_state.my_bet = []
        st.session_state.input_counter = 0
        st.rerun()
