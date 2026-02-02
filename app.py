import streamlit as st
import math
import random
from itertools import combinations

# 1. Βασικές Ρυθμίσεις
st.set_page_config(page_title="BigBet Stable Pro", layout="wide")

# 2. CSS για Λευκά Πλαίσια και Γαλάζιο Φόντο
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    
    /* Λευκά Πλαίσια */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #FFFFFF !important; 
        border-radius: 12px; 
        padding: 20px; 
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }

    /* Πλαίσιο Εισαγωγής */
    div.stTextInput > div > div > input {
        font-size: 26px !important; text-align: center; font-weight: bold;
        color: #0D47A1; border: 2px solid #1976D2; height: 55px;
    }

    /* Χρυσός Μετρητής */
    .total-matches-label {
        font-size: 30px !important; font-weight: bold; color: #0D47A1;
        text-align: center; padding: 15px; background-color: #FFD700;
        border-radius: 12px; border: 2px solid #DAA520; margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Αρχικοποίηση Μνήμης
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

st.title("🏆 BigBet Pro Tool")

# 4. Εισαγωγή Κωδικού
# Το key αλλάζει κάθε φορά για να καθαρίζει το input αυτόματα
current_key = f"in_{st.session_state.input_counter}"
user_input = st.text_input("ΚΩΔΙΚΟΣ", key=current_key, max_chars=3)

# Μετρητής Αγώνων
st.markdown(f'<div class="total-matches-label">ΣΥΝΟΛΟ ΑΓΩΝΩΝ: {len(st.session_state.my_bet)}</div>', unsafe_allow_html=True)

# Αν ο κωδικός είναι 3 ψηφία, πρόσθεσέ τον
if len(user_input) == 3 and user_input.isdigit():
    st.session_state.my_bet.append({"Κ": user_input, "Σ": "1"})
    st.session_state.input_counter += 1
    st.rerun()

# 5. Προβολή και Ανάπτυξη
if st.session_state.my_bet:
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("📋 Λίστα Αγώνων")
        opts = ["1", "X", "2", "G/G", "N/G", "Over 2.5", "Under 2.5", "1X", "X2"]
        # Εμφάνιση από τον πιο πρόσφατο στον παλιότερο
        for i in range(len(st.session_state.my_bet)-1, -1, -1):
            item = st.session_state.my_bet[i]
            c1, c2, c3 = st.columns([1, 2, 1])
            with c1: st.write(f"**{item['Κ']}**")
            with c2: 
                st.session_state.my_bet[i]['Σ'] = st.selectbox(
                    f"sel_{i}", opts, key=f"s_{i}", 
                    index=opts.index(item['Σ']), label_visibility="collapsed"
                )
            with c3:
                if st.button("❌", key=f"del_{i}"):
                    st.session_state.my_bet.pop(i)
                    st.rerun()

    with col_r:
        st.subheader("🔢 Ανάπτυξη Συστήματος")
        n = len(st.session_state.my_bet)
        k = st.number_input("Ζητούμενα:", 1, max(1, n), min(n, 3))
        total = math.comb(n, k)
        st.metric("Σύνολο Στηλών", f"{total:,}")
        
        if total > 0:
            if total <= 500:
                if st.checkbox("Εμφάνιση Όλων"):
                    for combo in combinations(st.session_state.my_bet, k):
                        st.text(" · ".join([f"{x['Κ']}[{x['Σ']}]" for x in combo]))
            else:
                num_rand = st.number_input("Τυχαίες στήλες για προβολή:", 1, total, 10)
                if st.button("Δείξε Τυχαίες ✨"):
                    all_combos = list(combinations(st.session_state.my_bet, k))
                    for c in random.sample(all_combos, num_rand):
                        st.text(" · ".join([f"{x['Κ']}[{x['Σ']}]" for x in c]))

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ"):
        st.session_state.my_bet = []
        st.session_state.input_counter = 0
        st.rerun()
