import streamlit as st
import math
import random
from itertools import combinations

st.set_page_config(page_title="BigBet Auto-View", layout="wide")

# --- CSS ΓΙΑ ΕΜΦΑΝΙΣΗ ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp {background-color: #f0f2f6;}
    /* Μεγάλο πεδίο εισαγωγής */
    div.stTextInput > div > div > input {
        font-size: 40px;
        text-align: center;
        font-weight: bold;
        background-color: #ffffff;
        border: 2px solid #1E88E5;
    }
    /* Στυλ για τη λίστα αγώνων */
    .match-row {
        background-color: #ffffff;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 5px;
        border-left: 5px solid #1E88E5;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ BigBet Auto-Entry & View")

# Αρχικοποίηση
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

# --- 1. ΑΥΤΟΜΑΤΟ ΠΕΔΙΟ ΕΙΣΑΓΩΓΗΣ ---
st.write("Γράψε 3 ψηφία και θα προστεθεί αυτόματα:")
current_key = f"input_{st.session_state.input_counter}"
user_input = st.text_input("ΚΩΔΙΚΟΣ", key=current_key, placeholder="---", max_chars=3)

# Αυτόματη προσθήκη μόλις φτάσει τα 3 ψηφία
if len(user_input) == 3:
    if user_input.isdigit():
        # Προσθήκη στη λίστα (αποφυγή διπλών αν θέλεις)
        st.session_state.my_bet.append({"Κ": user_input, "Σ": "1"})
        st.session_state.input_counter += 1
        st.rerun()
    else:
        st.error("Μόνο νούμερα!")

# --- 2. ΠΡΟΒΟΛΗ ΟΛΩΝ ΤΩΝ ΚΩΔΙΚΩΝ ---
if st.session_state.my_bet:
    st.markdown("---")
    st.subheader(f"📋 Επιλεγμένοι Αγώνες ({len(st.session_state.my_bet)})")
    
    # Λίστα σημείων για το selectbox
    market_options = ["1", "X", "2", "G/G", "N/G", "Over 0.5", "Under 0.5", "Over 1.5", "Under 1.5", "Over 2.5", "Under 2.5", "Over 3.5", "Under 3.5", "1X", "X2", "12"]

    # Εμφάνιση κάθε αγώνα σε γραμμή
    for i, item in enumerate(st.session_state.my_bet):
        col1, col2, col3 = st.columns([1, 2, 0.5])
        with col1:
            st.markdown(f"**#{i+1} | Κωδ: {item['Κ']}**")
        with col2:
            st.session_state.my_bet[i]['Σ'] = st.selectbox(
                f"Σημείο για {item['Κ']}", 
                market_options, 
                index=market_options.index(item['Σ']),
                key=f"m_{i}",
                label_visibility="collapsed"
            )
        with col3:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.my_bet.pop(i)
                st.rerun()

    # --- 3. ΑΝΑΠΤΥΞΗ ΣΥΣΤΗΜΑΤΟΣ ---
    st.markdown("---")
    n = len(st.session_state.my_bet)
    k_sys = st.number_input("Ζητούμενα (Σύστημα):", min_value=1, max_value=n, value=min(n, 3))
    
    total_possible = math.comb(n, k_sys)
    st.metric("Πιθανές Στήλες", f"{total_possible:,}")

    if total_possible <= 100000:
        if st.checkbox("Εμφάνιση Ανάλυσης Στηλών"):
            combos = combinations(st.session_state.my_bet, k_sys)
            for idx, c in enumerate(combos, 1):
                res = " - ".join([f"{item['Κ']}[{item['Σ']}]" for item in c])
                st.text(f"Στήλη {idx}: {res}")
    else:
        st.warning("Πολύ μεγάλο σύστημα για πλήρη ανάλυση (>100.000).")

    if st.button("Καθαρισμός Όλων 🗑️"):
        st.session_state.my_bet = []
        st.session_state.input_counter = 0
        st.rerun()
