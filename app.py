import streamlit as st
import math
import random
from itertools import combinations
import streamlit.components.v1 as components

# Ρυθμίσεις σελίδας
st.set_page_config(page_title="BigBet Pro", layout="wide")

# --- CSS ΓΙΑ ΜΠΛΕ/ΧΡΥΣΟ ΜΕΤΡΗΤΗ ΚΑΙ ΣΤΑΘΕΡΟΤΗΤΑ ---
st.markdown("""
    <style>
    div.stTextInput > div > div > input {
        font-size: 25px !important; text-align: center !important; font-weight: bold !important; height: 50px !important;
    }
    .total-matches-label {
        font-size: 30px !important; font-weight: bold !important; color: #0000FF !important;
        text-align: center; margin: 10px 0px; padding: 15px;
        background-color: #FFD700 !important; border: 3px solid #DAA520; border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- JAVASCRIPT ΓΙΑ AUTO-ENTER (Πιο "ελαφρύ" για να μην κολλάει) ---
components.html(
    """
    <script>
    function setup() {
        const doc = window.parent.document;
        doc.addEventListener('keyup', function(e) {
            const activeInput = doc.activeElement;
            if (activeInput.tagName === 'INPUT' && activeInput.value.length === 3) {
                activeInput.dispatchEvent(new KeyboardEvent('keydown', {'key': 'Enter', 'bubbles': true}));
                activeInput.dispatchEvent(new Event('change', {'bubbles': true}));
            }
        });
    }
    setTimeout(setup, 1000);
    </script>
    """, height=0,
)

# Αρχικοποίηση session state
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

st.title("🏆 BigBet Pro Tool")

# --- 1. ΕΙΣΑΓΩΓΗ ---
current_key = f"in_{st.session_state.input_counter}"
user_input = st.text_input("ΕΙΣΑΓΩΓΗ ΚΩΔΙΚΟΥ", key=current_key, max_chars=3)

# --- 2. ΧΡΥΣΟΣ ΜΕΤΡΗΤΗΣ ---
num_matches = len(st.session_state.my_bet)
st.markdown(f'<div class="total-matches-label">ΣΥΝΟΛΟ ΑΓΩΝΩΝ: {num_matches}</div>', unsafe_allow_html=True)

# Έλεγχος εισαγωγής
if len(user_input) == 3:
    if user_input.isdigit():
        st.session_state.my_bet.append({"Κ": user_input, "Σ": "1"})
        st.session_state.input_counter += 1
        st.rerun()

# --- 3. ΔΙΑΧΕΙΡΙΣΗ & ΑΝΑΠΤΥΞΗ ---
if st.session_state.my_bet:
    st.markdown("---")
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        st.subheader("📋 Λίστα")
        m_opts = ["1", "X", "2", "G/G", "N/G", "Over 2.5", "Under 2.5", "1X", "X2"]
        for i in range(len(st.session_state.my_bet)-1, -1, -1):
            item = st.session_state.my_bet[i]
            c1, c2, c3 = st.columns([1, 1.5, 0.5])
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
        st.metric("Στήλες", f"{total:,}")
        
        if total > 0:
            mode = st.radio("Εμφάνιση:", ["Όλες", "Τυχαίες"], horizontal=True)
            if mode == "Τυχαίες":
                num = st.number_input("Πόσες;", 1, total, min(total, 5))
                if st.button("Παραγωγή ✨"):
                    all_c = list(combinations(st.session_state.my_bet, k))
                    for idx, c in enumerate(random.sample(all_c, num), 1):
                        st.text(f"{idx}. {' · '.join([f'{x['Κ']}[{x['Σ']}]' for x in c])}")
            else:
                if total <= 1000: # Όριο για να μην κολλάει η οθόνη
                    if st.checkbox("Εμφάνιση Αναλυτικά"):
                        for idx, c in enumerate(combinations(st.session_state.my_bet, k), 1):
                            st.text(f"{idx}. {' · '.join([f'{x['Κ']}[{x['Σ']}]' for x in c])}")
                else:
                    st.warning("Πολλές στήλες. Βάλε 'Τυχαίες'.")

    if st.button("Καθαρισμός Όλων 🗑️"):
        st.session_state.my_bet = []
        st.rerun()
