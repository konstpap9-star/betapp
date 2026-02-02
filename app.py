import streamlit as st
import math
from itertools import combinations
import streamlit.components.v1 as components

st.set_page_config(page_title="BigBet No-Enter", layout="wide")

# --- CSS ΓΙΑ ΜΕΓΑΛΟ ΚΑΙ ΚΕΝΤΡΑΡΙΣΜΕΝΟ ΚΟΥΤΙ ---
st.markdown("""
    <style>
    div.stTextInput > div > div > input {
        font-size: 45px !important;
        text-align: center !important;
        font-weight: bold !important;
        height: 70px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- JAVASCRIPT ΓΙΑ ΑΥΤΟΜΑΤΟ ENTER & FOCUS ---
components.html(
    """
    <script>
    function setup() {
        const doc = window.parent.document;
        // Βρίσκουμε το input και του δίνουμε focus
        const inputs = doc.querySelectorAll('input');
        const mainInput = inputs[inputs.length - 1]; 
        if (mainInput) mainInput.focus();

        doc.addEventListener('keyup', function(e) {
            const activeInput = doc.activeElement;
            if (activeInput.tagName === 'INPUT' && activeInput.value.length === 3) {
                // Προσομοίωση Enter
                activeInput.dispatchEvent(new KeyboardEvent('keydown', {'key': 'Enter', 'bubbles': true}));
                activeInput.dispatchEvent(new Event('change', {'bubbles': true}));
            }
        });
    }
    // Εκτέλεση μετά από λίγο για να προλάβει να φορτώσει το DOM
    setTimeout(setup, 500);
    </script>
    """,
    height=0,
)

st.title("⚡ BigBet Fast Entry")

if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

# Χρησιμοποιούμε το input_counter στο key για να "πεθαίνει" το παλιό κουτάκι και να γεννιέται νέο άδειο
current_key = f"input_field_{st.session_state.input_counter}"

st.write("Γράψε 3 ψηφία:")
user_input = st.text_input("ΚΩΔΙΚΟΣ", key=current_key, max_chars=3, label_visibility="collapsed")

# Μόλις το Streamlit δει 3 ψηφία (από το JS Enter)
if len(user_input) == 3:
    if user_input.isdigit():
        st.session_state.my_bet.append({"Κ": user_input, "Σ": "1"})
        st.session_state.input_counter += 1 # Αυτό "καθαρίζει" το κουτάκι
        st.rerun()

# --- ΠΡΟΒΟΛΗ ΛΙΣΤΑΣ ---
if st.session_state.my_bet:
    st.markdown("---")
    st.subheader(f"📋 Αγώνες: {len(st.session_state.my_bet)}")
    
    market_options = ["1", "X", "2", "G/G", "N/G", "Over 2.5", "Under 2.5", "1X", "X2"]

    for i, item in enumerate(reversed(st.session_state.my_bet)): # reversed για να βλέπεις τον τελευταίο πάνω-πάνω
        idx = len(st.session_state.my_bet) - 1 - i
        col1, col2, col3 = st.columns([1, 2, 0.5])
        with col1: st.write(f"**{item['Κ']}**")
        with col2: 
            st.session_state.my_bet[idx]['Σ'] = st.selectbox(f"m_{idx}", market_options, key=f"sel_{idx}", index=market_options.index(item['Σ']), label_visibility="collapsed")
        with col3:
            if st.button("❌", key=f"d_{idx}"):
                st.session_state.my_bet.pop(idx)
                st.rerun()

    st.markdown("---")
    n = len(st.session_state.my_bet)
    k_sys = st.number_input("Σύστημα (Ζητούμενα):", min_value=1, max_value=n, value=min(n, 3))
    total_possible = math.comb(n, k_sys)
    st.metric("Σύνολο Στηλών", f"{total_possible:,}")

    if st.button("Καθαρισμός Όλων 🗑️"):
        st.session_state.my_bet = []
        st.session_state.input_counter = 0
        st.rerun()
