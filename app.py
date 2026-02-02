import streamlit as st
import math
import random
from itertools import combinations

# Βασικές ρυθμίσεις για να μην κρασάρει
st.set_page_config(page_title="BigBet Stable", layout="wide")

# --- CSS (Απλό και Καθαρό) ---
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    .total-matches-label {
        font-size: 28px !important; font-weight: bold; color: #0D47A1;
        text-align: center; padding: 15px; background-color: #FFD700;
        border-radius: 10px; border: 2px solid #DAA520; margin: 10px 0;
    }
    div.stTextInput > div > div > input {
        font-size: 24px !important; text-align: center; font-weight: bold;
        border: 2px solid #1976D2; height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# Αρχικοποίηση
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

st.title("🏆 BigBet Pro")

# --- ΕΙΣΑΓΩΓΗ ---
# Χρησιμοποιούμε δυναμικό κλειδί για να καθαρίζει το κουτί
current_key = f"input_{st.session_state.input_counter}"
user_input = st.text_input("ΚΩΔΙΚΟΣ (3 ΨΗΦΙΑ)", key=current_key, max_chars=3)

# Εμφάνιση Μετρητή
st.markdown(f'<div class="total-matches-label">ΣΥΝΟΛΟ ΑΓΩΝΩΝ: {len(st.session_state.my_bet)}</div>', unsafe_allow_html=True)

# Αυτόματη καταχώρηση (Το Streamlit θα κάνει rerun μόλις δει 3 χαρακτήρες λόγω του key)
if len(user_input) == 3:
    if user_input.isdigit():
        st.session_state.my_bet.append({"Κ": user_input, "Σ": "1"})
        st.session_state.input_counter += 1
        st.rerun()

# --- ΛΙΣΤΑ ΚΑΙ ΣΥΣΤΗΜΑ ---
if st.session_state.my_bet:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Αγώνες")
        opts = ["1", "X", "2", "G/G", "Over 2.5", "Under 2.5"]
        for i in range(len(st.session_state.my_bet)-1, -1, -1):
            item = st.session_state.my_bet[i]
            c_a, c_b, c_c = st.columns([1, 2, 1])
            with c_a: st.write(f"**{item['Κ']}**")
            with c_b: st.session_state.my_bet[i]['Σ'] = st.selectbox(f"s_{i}", opts, key=f"sel_{i}", index=opts.index(item['Σ']), label_visibility="collapsed")
            with c_c:
                if st.button("❌", key=f"del_{i}"):
                    st.session_state.my_bet.pop(i)
                    st.rerun()

    with col2:
        st.subheader("🔢 Σύστημα")
        n = len(st.session_state.my_bet)
        k = st.number_input("Ζητούμενα:", 1, max(1, n), min(n, 3))
        total = math.comb(n, k)
        st.metric("Σύνολο Στηλών", f"{total:,}")
        
        if total > 0 and total < 500:
            if st.checkbox("Εμφάνιση Στηλών"):
                for combo in combinations(st.session_state.my_bet, k):
                    st.text(" · ".join([f"{x['Κ']}[{x['Σ']}]" for x in combo]))
        elif total >= 500:
            st.warning("Πολλές στήλες για εμφάνιση.")

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ ΟΛΩΝ"):
        st.session_state.my_bet = []
        st.session_state.input_counter = 0
        st.rerun()
