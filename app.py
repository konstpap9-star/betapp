import streamlit as st
import math
from itertools import combinations

# 1. Βασικές Ρυθμίσεις
st.set_page_config(page_title="BigBet Mobile Pro", layout="wide")

# 2. CSS για Mobile & Vertical Optimization
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    
    .white-container {
        background-color: #FFFFFF;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 8px;
        border: 1px solid #BBDEFB;
    }
    
    /* Κίτρινα Πεδία */
    input {
        background-color: #FFF9C4 !important;
        border: 1px solid #FBC02D !important;
        font-weight: bold !important;
        height: 35px !important;
    }
    
    /* Πολύ στενό Selectbox χωρίς περιττά στοιχεία */
    div[data-baseweb="select"] > div {
        background-color: #FFF9C4 !important;
        border: 1px solid #FBC02D !important;
        min-height: 35px !important;
        padding: 0px 2px !important;
    }
    
    /* Αφαίρεση της κάθετης γραμμής και του βέλους για εξοικονόμηση χώρου */
    div[data-baseweb="select"] div[role="button"] + div {
        display: none !important;
    }

    /* Μικρό και κομψό κουμπί διαγραφής ✕ */
    .stButton > button {
        background-color: #FFEBEE !important;
        color: #C62828 !important;
        border: 1px solid #EF9A9A !important;
        padding: 0px !important;
        width: 30px !important;
        height: 35px !important;
        font-weight: bold !important;
    }

    .counter-box {
        background-color: #FFD700;
        color: #0D47A1;
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        padding: 8px;
        border-radius: 10px;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

st.title("🏆 BigBet Mobile")

# --- ΕΙΣΑΓΩΓΗ (Σε μία γραμμή για κάθετη οθόνη) ---
st.markdown('<div class="white-container">', unsafe_allow_html=True)
c_in1, c_in2, c_in3 = st.columns([1, 1, 1.2])
with c_in1: s_range = st.text_input("ΑΠΟ", key="start", max_chars=3, label_visibility="collapsed", placeholder="Από")
with c_in2: e_range = st.text_input("ΕΩΣ", key="end", max_chars=3, label_visibility="collapsed", placeholder="Έως")
with c_in3:
    if st.button("ΠΡΟΣΘΗΚΗ"):
        if s_range.isdigit() and e_range.isdigit():
            for code in range(int(s_range), int(e_range) + 1):
                fmt = str(code).zfill(3)
                if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
                    st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})
            st.rerun()

curr_key = f"in_{st.session_state.input_counter}"
u_input = st.text_input("📍 ΚΩΔΙΚΟΣ", key=curr_key, max_chars=3, placeholder="Κωδικός")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f'<div class="counter-box">ΑΓΩΝΕΣ: {len(st.session_state.my_bet)}</div>', unsafe_allow_html=True)

if len(u_input) == 3 and u_input.isdigit():
    st.session_state.my_bet.append({"Κ": u_input, "Σ": "1"})
    st.session_state.input_counter += 1
    st.rerun()

# --- ΛΙΣΤΑ (Εξαιρετικά Compact για Κάθετη Θέση) ---
if st.session_state.my_bet:
    # Στο κινητό οι στήλες l, r θα μπουν η μία κάτω από την άλλη αυτόματα
    st.markdown('<div class="white-container">', unsafe_allow_html=True)
    opts = ["1", "X", "2", "G/G", "N/G", "Ov", "Un", "1X", "X2"]
    
    for i in range(len(st.session_state.my_bet)-1, -1, -1):
        item = st.session_state.my_bet[i]
        # Χρήση πολύ στενών αναλογιών για να μείνουν στην ίδια γραμμή
        cl1, cl2, cl3 = st.columns([0.6, 1.4, 0.4])
        with cl1: 
            st.write(f"**{item['Κ']}**")
        with cl2: 
            st.session_state.my_bet[i]['Σ'] = st.selectbox(f"s_{i}", opts, key=f"sel_{i}", index=opts.index(item['Σ']), label_visibility="collapsed")
        with cl3:
            if st.button("✕", key=f"d_{i}"):
                st.session_state.my_bet.pop(i)
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ΣΥΣΤΗΜΑ ---
    st.markdown('<div class="white-container">', unsafe_allow_html=True)
    n = len(st.session_state.my_bet)
    k = st.number_input("Ζητούμενα:", 1, max(1, n), min(n, 3) if n>=3 else 1)
    st.write(f"Στήλες: **{math.comb(n, k):,}**")
    if st.button("🖨️ ΕΚΤΥΠΩΣΗ"):
        st.info("Δημιουργία...")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ"):
        st.session_state.my_bet = []
        st.rerun()
