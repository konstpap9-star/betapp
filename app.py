import streamlit as st
import math
from itertools import combinations

# 1. Βασικές Ρυθμίσεις
st.set_page_config(page_title="BigBet Slim Edition", layout="wide")

# 2. CSS για Compact Εμφάνιση
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    
    .white-container {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid #BBDEFB;
    }
    
    /* Κίτρινα Πεδία */
    input {
        background-color: #FFF9C4 !important;
        border: 2px solid #FBC02D !important;
        font-weight: bold !important;
    }
    
    /* Compact Selectbox (Σημεία) */
    div[data-baseweb="select"] > div {
        background-color: #FFF9C4 !important;
        border: 2px solid #FBC02D !important;
        min-height: 30px !important;
    }
    
    /* Αφαίρεση κάθετης γραμμής (separator) στο selectbox */
    div[data-baseweb="select"] div[role="button"] + div {
        display: none !important;
    }

    /* Μίκρυμα του κουμπιού διαγραφής */
    .stButton > button {
        padding: 2px 10px !important;
        height: auto !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
    }

    .counter-box {
        background-color: #FFD700;
        color: #0D47A1;
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border-radius: 12px;
        border: 2px solid #DAA520;
    }
    </style>
    """, unsafe_allow_html=True)

if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

st.title("🏆 BigBet Printer Pro")

# --- ΕΙΣΑΓΩΓΗ ---
st.markdown('<div class="white-container">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 1, 2])
with c1: s_range = st.text_input("ΑΠΟ", key="start", max_chars=3)
with c2: e_range = st.text_input("ΕΩΣ", key="end", max_chars=3)
with c3:
    st.write("")
    if st.button("Προσθήκη Εύρους ➕"):
        if s_range.isdigit() and e_range.isdigit():
            for code in range(int(s_range), int(e_range) + 1):
                fmt = str(code).zfill(3)
                if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
                    st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})
            st.rerun()

curr_key = f"in_{st.session_state.input_counter}"
u_input = st.text_input("📍 ΕΙΣΑΓΩΓΗ ΚΩΔΙΚΟΥ", key=curr_key, max_chars=3)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div class="counter-box">ΣΥΝΟΛΟ ΑΓΩΝΩΝ: {len(st.session_state.my_bet)}</div>', unsafe_allow_html=True)

if len(u_input) == 3 and u_input.isdigit():
    st.session_state.my_bet.append({"Κ": u_input, "Σ": "1"})
    st.session_state.input_counter += 1
    st.rerun()

# --- ΛΙΣΤΑ (Compact Mode) ---
if st.session_state.my_bet:
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.markdown('<div class="white-container"><b>📋 Λίστα</b>', unsafe_allow_html=True)
        opts = ["1", "X", "2", "G/G", "N/G", "Over", "Under", "1X", "X2"]
        for i in range(len(st.session_state.my_bet)-1, -1, -1):
            item = st.session_state.my_bet[i]
            # Χρήση 4 στηλών για να "στριμώξουμε" τα στοιχεία
            cl1, cl2, cl3 = st.columns([0.8, 1.2, 0.4])
            with cl1: st.write(f"**{item['Κ']}**")
            with cl2: 
                st.session_state.my_bet[i]['Σ'] = st.selectbox(f"s_{i}", opts, key=f"sel_{i}", index=opts.index(item['Σ']), label_visibility="collapsed")
            with cl3:
                if st.button("✕", key=f"d_{i}"):
                    st.session_state.my_bet.pop(i)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="white-container"><b>🔢 Σύστημα</b>', unsafe_allow_html=True)
        n = len(st.session_state.my_bet)
        k = st.number_input("Ζητούμενα:", 1, max(1, n), min(n, 3) if n>=3 else 1)
        st.metric("Στήλες", f"{math.comb(n, k):,}")
        if st.button("🖨️ Εκτύπωση"):
            st.info("Δημιουργία εκτύπωσης...")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🗑️ Καθαρισμός Όλων"):
        st.session_state.my_bet = []
        st.rerun()
