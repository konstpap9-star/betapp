import streamlit as st
import math
import random
from itertools import combinations

st.set_page_config(page_title="BigBet Turbo", layout="wide")

st.title("🚀 BigBet Turbo - 100K Limit")

if 'my_bet' not in st.session_state: 
    st.session_state.my_bet = []

# --- ΕΙΣΑΓΩΓΗ ---
raw_input = st.text_input("Κωδικοί (π.χ. 101102103...):")
if st.button("Προσθήκη Αγώνων"):
    if raw_input:
        new = [raw_input[i:i+3] for i in range(0, len(raw_input), 3)]
        for c in new:
            if len(c) == 3: st.session_state.my_bet.append({"Κ": c, "Σ": "1"})
        st.rerun()

if st.session_state.my_bet:
    n = len(st.session_state.my_bet)
    st.info(f"Αγώνες στο δελτίο: {n}")
    
    k_sys = st.number_input("Ζητούμενα (Σύστημα):", min_value=1, max_value=n, value=min(n, 3))
    
    # Υπολογισμός συνολικών στηλών
    total_possible = math.comb(n, k_sys)
    st.metric("Πιθανοί συνδυασμοί", f"{total_possible:,}")

    st.markdown("---")

    # ΕΛΕΓΧΟΣ ΟΡΙΟΥ
    if total_possible > 100000:
        st.error(f"⚠️ Το σύστημα παράγει {total_possible:,} στήλες. Το όριο είναι 100.000.")
        st.write("Δοκίμασε να μειώσεις τους αγώνες ή να αλλάξεις τα ζητούμενα.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Ανάπτυξη Όλων"):
                st.write("### Λίστα Στηλών:")
                # Χρήση iterator για εξοικονόμηση μνήμης
                combos = combinations(st.session_state.my_bet, k_sys)
                for idx, c in enumerate(combos, 1):
                    res = " - ".join([f"{item['Κ']}({item['Σ']})" for item in c])
                    st.text(f"{idx}. {res}")
        
        with col2:
            num_random = st.number_input("Τυχαίες στήλες για κράτημα:", min_value=1, max_value=total_possible, value=min(total_possible, 10
