import streamlit as st
import math
from itertools import combinations
import streamlit.components.v1 as components

st.set_page_config(page_title="BigBet No-Enter", layout="wide")

# --- ΑΥΤΟΜΑΤΟΣ ΚΩΔΙΚΑΣ JAVASCRIPT ---
# Αυτό το κομμάτι "πιάνει" τα 3 ψηφία και πατάει το Enter για σένα
components.html(
    """
    <script>
    const doc = window.parent.document;
    const inputs = doc.querySelectorAll('input');
    
    // Βρίσκουμε το πεδίο εισαγωγής
    doc.addEventListener('keyup', function(e) {
        const activeInput = doc.activeElement;
        if (activeInput.tagName === 'INPUT' && activeInput.value.length === 3) {
            // Δημιουργούμε ένα εικονικό πάτημα Enter
            const event = new KeyboardEvent('keydown', {
                key: 'Enter',
                code: 'Enter',
                which: 13,
                keyCode: 13,
                bubbles: True
            });
            activeInput.dispatchEvent(event);
        }
    });
    </script>
    """,
    height=0,
)

st.title("⚡ BigBet Real-Time Entry")

if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'last_val' not in st.session_state: st.session_state.last_val = ""

# --- ΠΕΔΙΟ ΕΙΣΑΓΩΓΗΣ ---
st.write("Γράψε 3 ψηφία (θα προστεθούν ακαριαία χωρίς Enter):")
user_input = st.text_input("ΚΩΔΙΚΟΣ", key="auto_input", max_chars=3)

# Επεξεργασία εισαγωγής
if len(user_input) == 3 and user_input != st.session_state.last_val:
    if user_input.isdigit():
        st.session_state.my_bet.append({"Κ": user_input, "Σ": "1"})
        st.session_state.last_val = user_input
        # Καθαρισμός για την επόμενη φορά μέσω rerun
        st.rerun()

# --- ΠΡΟΒΟΛΗ ΚΑΙ ΔΙΑΧΕΙΡΙΣΗ ---
if st.session_state.my_bet:
    st.markdown("---")
    st.subheader(f"📋 Αγώνες: {len(st.session_state.my_bet)}")
    
    market_options = ["1", "X", "2", "G/G", "N/G", "Over 2.5", "Under 2.5", "1X", "X2"]

    for i, item in enumerate(st.session_state.my_bet):
        col1, col2, col3 = st.columns([1, 2, 0.5])
        with col1: st.write(f"**{item['Κ']}**")
        with col2: 
            st.session_state.my_bet[i]['Σ'] = st.selectbox(f"m_{i}", market_options, key=f"sel_{i}", label_visibility="collapsed")
        with col3:
            if st.button("❌", key=f"d_{i}"):
                st.session_state.my_bet.pop(i)
                st.rerun()

    # --- ΣΥΣΤΗΜΑ ---
    n = len(st.session_state.my_bet)
    k_sys = st.number_input("Σύστημα (Ζητούμενα):", min_value=1, max_value=n, value=min(n, 3))
    total_possible = math.comb(n, k_sys)
    st.metric("Σύνολο Στηλών", f"{total_possible:,}")

    if st.button("Καθαρισμός Όλων 🗑️"):
        st.session_state.my_bet = []
        st.rerun()
