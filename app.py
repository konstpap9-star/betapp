import streamlit as st
import math
import random
from itertools import combinations

# 1. Ρυθμίσεις Σελίδας
st.set_page_config(page_title="BigBet Yellow Edition", layout="wide")

# 2. CSS για Γαλάζιο Φόντο και Ελαφρύ Κίτρινο στα Πλαίσια
st.markdown("""
    <style>
    /* Φόντο Σελίδας */
    .stApp { 
        background-color: #E3F2FD; 
    }
    
    /* ΤΑ ΠΛΑΙΣΙΑ ΣΕ ΕΛΑΦΡΥ ΚΙΤΡΙΝΟ */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #FFF9C4 !important; /* Απαλό κίτρινο */
        border-radius: 15px; 
        padding: 20px; 
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        border: 1px solid #FBC02D; /* Διακριτικό περίγραμμα */
    }
    
    /* Λευκά εσωτερικά κουτάκια για να ξεχωρίζουν μέσα στο κίτρινο */
    .stTextInput input, .stSelectbox div, .stNumberInput input {
        background-color: #FFFFFF !important;
    }

    /* Ο Χρυσός Μετρητής παραμένει έντονος */
    .total-matches-label {
        font-size: 32px !important; font-weight: bold; color: #0D47A1;
        text-align: center; padding: 20px;
        background-color: #FFD700 !important; 
        border: 3px solid #DAA520; border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# Αρχικοποίηση
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

st.title("🏆 BigBet Printer Pro")

# --- ΜΑΖΙΚΗ ΕΙΣΑΓΩΓΗ ---
st.markdown("### 🔗 Μαζική Εισαγωγή")
c1, c2, c3 = st.columns([1, 1, 1.5])
with c1:
    s_range = st.text_input("ΑΠΟ", key="s_r", max_chars=3)
with c2:
    e_range = st.text_input("ΕΩΣ", key="e_r", max_chars=3)
with c3:
    st.write(" ")
    if st.button("Προσθήκη Εύρους ➕"):
        if s_range.isdigit() and e_range.isdigit():
            for code in range(int(s_range), int(e_range) + 1):
                fmt = str(code).zfill(3)
                if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
                    st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})
            st.rerun()

# --- ΜΕΜΟΝΩΜΕΝΗ ΕΙΣΑΓΩΓΗ ---
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
        st.subheader("📋 Λίστα Αγώνων")
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
        k = st.number_input("Ζητούμενα:", 1, max(1, n), min(n, 3) if n>=3 else 1)
        st.metric("Σύνολο Στηλών", f"{math.comb(n, k):,}")
        
        if st.button("🖨️ Εκτύπωση σε Δελτίο"):
            st.info("Εδώ θα ενεργοποιηθεί η εκτύπωση με τις συντεταγμένες που θα βρούμε.")

    if st.button("🗑️ Καθαρισμός Όλων"):
        st.session_state.my_bet = []
        st.rerun()
