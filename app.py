import streamlit as st
import math
import random
from itertools import combinations
import streamlit.components.v1 as components

st.set_page_config(page_title="BigBet Pro", layout="wide")

# --- CSS ΓΙΑ ΜΙΚΡΟΤΕΡΑ ΚΑΙ ΚΑΘΑΡΑ ΝΟΥΜΕΡΑ ---
st.markdown("""
    <style>
    div.stTextInput > div > div > input {
        font-size: 25px !important; 
        text-align: center !important; 
        font-weight: bold !important; 
        height: 50px !important;
        border-radius: 10px !important;
    }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- JAVASCRIPT (Auto-Enter & Focus) ---
components.html(
    """
    <script>
    function setup() {
        const doc = window.parent.document;
        const inputs = doc.querySelectorAll('input');
        const mainInput = inputs[inputs.length - 1]; 
        if (mainInput) mainInput.focus();

        doc.addEventListener('keyup', function(e) {
            const activeInput = doc.activeElement;
            if (activeInput.tagName === 'INPUT' && activeInput.value.length === 3) {
                activeInput.dispatchEvent(new KeyboardEvent('keydown', {'key': 'Enter', 'bubbles': true}));
                activeInput.dispatchEvent(new Event('change', {'bubbles': true}));
            }
        });
    }
    setTimeout(setup, 500);
    </script>
    """, height=0,
)

if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

st.title("🏆 BigBet Pro Tool")

# --- ΕΙΣΑΓΩΓΗ ---
st.write("Εισαγωγή 3ψήφιου κωδικού:")
current_key = f"input_field_{st.session_state.input_counter}"
user_input = st.text_input("ΚΩΔΙΚΟΣ", key=current_key, max_chars=3, label_visibility="collapsed")

if len(user_input) == 3 and user_input.isdigit():
    st.session_state.my_bet.append({"Κ": user_input, "Σ": "1"})
    st.session_state.input_counter += 1
    st.rerun()

# --- ΔΙΑΧΕΙΡΙΣΗ ΑΓΩΝΩΝ ---
if st.session_state.my_bet:
    st.markdown("---")
    col_l, col_r = st.columns([1, 1.2])
    
    with col_l:
        st.subheader("📋 Οι Αγώνες σου")
        market_options = ["1", "X", "2", "G/G", "N/G", "Over 2.5", "Under 2.5", "1X", "X2"]
        
        for i in range(len(st.session_state.my_bet)-1, -1, -1):
            item = st.session_state.my_bet[i]
            c1, c2, c3 = st.columns([1, 2, 0.5])
            with c1: st.write(f"**{item['Κ']}**")
            with c2: 
                st.session_state.my_bet[i]['Σ'] = st.selectbox(f"m_{i}", market_options, key=f"sel_{i}", index=market_options.index(item['Σ']), label_visibility="collapsed")
            with c3:
                if st.button("❌", key=f"d_{i}"):
                    st.session_state.my_bet.pop(i)
                    st.rerun()

    with col_r:
        st.subheader("🔢 Ανάπτυξη & Φίλτρα")
        n = len(st.session_state.my_bet)
        k_sys = st.number_input("Σύστημα (Ζητούμενα):", min_value=1, max_value=n, value=min(n, 3))
        
        total_cols = math.comb(n, k_sys)
        st.metric("Συνολικές Στήλες", f"{total_cols:,}")
        
        if total_cols > 0:
            st.markdown("---")
            # Επιλογή αν θέλει όλες ή τυχαίες
            filter_mode = st.radio("Επιλογή στηλών:", ["Όλες οι στήλες", "Τυχαία επιλογή (Random)"], horizontal=True)
            
            all_combos = list(combinations(st.session_state.my_bet, k_sys))
            
            if filter_mode == "Τυχαία επιλογή (Random)":
                num_to_keep = st.number_input("Πόσες στήλες να κρατήσω;", min_value=1, max_value=total_cols, value=min(total_cols, 10))
                if st.button("Παραγωγή Τυχαίων ✨"):
                    selected_combos = random.sample(all_combos, num_to_keep)
                    st.write(f"### {num_to_keep} Τυχαίες Στήλες:")
                    for idx, c in enumerate(selected_combos, 1):
                        res = " · ".join([f"{item['Κ']}[{item['Σ']}]" for item in c])
                        st.text(f"Στ. {idx}: {res}")
            
            else: # Όλες οι στήλες
                if total_cols <= 100000:
                    if st.checkbox("🔍 Εμφάνιση Αναλυτικών Στηλών"):
                        for idx, c in enumerate(all_combos, 1):
                            res = " · ".join([f"{item['Κ']}[{item['Σ']}]" for item in c])
                            st.text(f"Στ. {idx}: {res}")
                else:
                    st.warning("⚠️ Πολλές στήλες (>100.000). Χρησιμοποίησε το Random.")

    if st.button("Καθαρισμός Όλων 🗑️"):
        st.session_state.my_bet = []
        st.session_state.input_counter = 0
        st.rerun()
