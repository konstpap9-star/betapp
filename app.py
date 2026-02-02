import streamlit as st
import math
import random
from itertools import combinations

# Ρυθμίσεις σελίδας
st.set_page_config(page_title="BigBet Turbo", layout="wide")

# --- CSS ΓΙΑ ΣΤΑΘΕΡΟΤΗΤΑ ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp {background-color: #f0f2f6;}
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 BigBet Turbo - 100K Limit")

# Αρχικοποίηση μνήμης (Session State)
if 'my_bet' not in st.session_state:
    st.session_state.my_bet = []

# --- 1. ΕΙΣΑΓΩΓΗ ΑΓΩΝΩΝ ---
st.subheader("📝 Εισαγωγή Αγώνων")
raw_input = st.text_input("Κωδικοί (π.χ. 101102103):", key="input_field")

if st.button("Προσθήκη Αγώνων"):
    if raw_input:
        # Σπάσιμο ανά 3 ψηφία
        new_codes = [raw_input[i:i+3] for i in range(0, len(raw_input), 3)]
        for c in new_codes:
            if len(c) == 3:
                st.session_state.my_bet.append({"Κ": c, "Σ": "1"})
        st.rerun()

# --- 2. ΔΙΑΧΕΙΡΙΣΗ ΚΑΙ ΑΝΑΠΤΥΞΗ ---
if st.session_state.my_bet:
    n = len(st.session_state.my_bet)
    st.info(f"Αγώνες στο δελτίο: {n} | Επιλεγμένοι: {', '.join([x['Κ'] for x in st.session_state.my_bet])}")
    
    # Επιλογή Συστήματος
    k_sys = st.number_input("Ζητούμενα (Σύστημα):", min_value=1, max_value=n if n > 0 else 1, value=min(n, 3) if n > 0 else 1)
    
    # Μαθηματικός Υπολογισμός
    total_possible = math.comb(n, k_sys)
    st.metric("Πιθανές Στήλες", f"{total_possible:,}")

    st.markdown("---")

    # ΕΛΕΓΧΟΣ ΟΡΙΟΥ 100.000
    if total_possible > 100000:
        st.error(f"⚠️ Το σύστημα έχει {total_possible:,} στήλες. Το όριο είναι 100.000!")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Ανάπτυξη Όλων"):
                st.write("### Λίστα Στηλών:")
                # Χρήση generator για ταχύτητα
                combos = combinations(st.session_state.my_bet, k_sys)
                for idx, c in enumerate(combos, 1):
                    res = " - ".join([f"{item['Κ']}[{item['Σ']}]" for item in c])
                    st.text(f"{idx}. {res}")

        with col2:
            num_random = st.number_input("Τυχαίες στήλες:", min_value=1, max_value=total_possible, value=min(total_possible, 10))
            if st.button("Τυχαία Επιλογή 🎲"):
                # Μετατροπή σε λίστα μόνο όταν είναι απαραίτητο για το sampling
                all_combos = list(combinations(st.session_state.my_bet, k_sys))
                sampled = random.sample(all_combos, num_random)
                st.write(f"### {num_random} Τυχαίες Επιλογές:")
                for idx, s in enumerate(sampled, 1):
                    res = " - ".join([f"{item['Κ']}[{item['Σ']}]" for item in s])
                    st.text(f"{idx}. {res}")

    if st.button("Καθαρισμός Όλων 🗑️"):
        st.session_state.my_bet = []
        st.rerun()
else:
    st.write("Δεν υπάρχουν αγώνες. Ξεκίνα γράφοντας κωδικούς στο πλαίσιο!")
