import streamlit as st
import math
import random
from itertools import combinations

# 1. Ρυθμίσεις Σελίδας
st.set_page_config(page_title="BigBet Precise Edition", layout="wide")

# 2. CSS για Λευκά Πλαίσια και Κίτρινα Πεδία Εισαγωγής
st.markdown("""
    <style>
    /* Φόντο Σελίδας Γαλάζιο */
    .stApp { background-color: #E3F2FD; }
    
    /* ΤΑ ΜΕΓΑΛΑ ΠΛΑΙΣΙΑ ΕΙΝΑΙ ΛΕΥΚΑ ΠΑΛΙ */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #FFFFFF !important; 
        border-radius: 12px; 
        padding: 15px; 
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    
    /* ΤΑ ΠΕΔΙΑ ΤΩΝ ΑΡΙΘΜΩΝ ΕΙΝΑΙ ΕΛΑΦΡΥ ΚΙΤΡΙΝΟ */
    div.stTextInput > div > div > input {
        background-color: #FFF9C4 !important; /* Το απαλό κίτρινο που ζήτησες */
        color: #0D47A1 !important;
        font-weight: bold !important;
        font-size: 20px !important;
        border: 2px solid #FBC02D !important;
    }

    /* Ο Χρυσός Μετρητής */
    .total-matches-label {
        font-size: 28px !important; font-weight: bold; color: #0D47A1;
        text-align: center; padding: 15px; background-color: #FFD700;
        border-radius: 12px; border: 2px solid #DAA520; margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Αρχικοποίηση
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

st.title("🏆 BigBet Printer Pro")

# --- ΜΑΖΙΚΗ ΕΙΣΑΓΩΓΗ ---
with st.container():
    st.write("🔗 **Μαζική Εισαγωγή**")
    c1, c2, c3, c4 = st.columns([1, 1, 1, 2])
    with c1:
        s_range = st.text_input("ΑΠΟ", key="s_r", max_chars=3, placeholder="Από")
    with c2:
        e_range = st.text_input("ΕΩΣ", key="e_r", max_chars=3, placeholder="Έως")
    with c3:
        st.write(" ") # Padding
        if st.button("Προσθήκη ➕"):
            if s_range.isdigit() and e_range.isdigit():
                for code in range(int(s_range), int(e_range) + 1):
                    fmt = str(code).zfill(3)
                    if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
                        st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})
                st.rerun()
    with c4: st.empty()

# --- ΜΕΜΟΝΩΜΕΝΗ ΕΙΣΑΓΩΓΗ ---
with st.container():
    curr_key = f"in_{st.session_state.input_counter}"
    u_input = st.text_input("📍 ΕΙΣΑΓΩΓΗ ΚΩΔΙΚΟΥ", key=curr_key, max_chars=3)

# Μετρητής
st.markdown(f'<div class="total-matches-label">ΣΥΝΟΛΟ ΑΓΩΝΩΝ: {len(st.session_state.my_bet)}</div>', unsafe_allow_html=True)

if len(u_input) == 3 and u_input.isdigit():
    st.session_state.my_bet.append({"Κ": u_input, "Σ": "1"})
    st.session_state.input_counter += 1
    st.rerun()

# --- ΛΙΣΤΑ ΚΑΙ ΣΥΣΤΗΜΑ ---
if st.session_state.my_bet:
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader("📋 Λίστα")
        opts = ["1", "X", "2", "G/G", "N/G", "Over 2.5", "Under 2.5", "1X", "X2"]
        for i in range(len(st.session_state.my_bet)-1, -1, -1):
            item = st.session_state.my_bet[i]
            cl1, cl2, cl3 = st.columns([1, 2, 0.8])
            with cl1: st.write(f"**{item['Κ']}**")
            with cl2: st.session_state.my_bet[i]['Σ'] = st.selectbox(f"s_{i}", opts, key=f"sel_{i}", index=opts.index(item['Σ']))
            with cl3:
                if st.button("❌", key=f"d_{i}"):
                    st.session_state.my_bet.pop(i)
                    st.rerun()
    with col_r:
        st.subheader("🔢 Σύστημα")
        n = len(st.session_state.my_bet)
        k = st.number_input("Ζητούμενα:", 1, max(1, n), min(n, 3) if n>=3 else 1
