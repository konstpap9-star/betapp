import streamlit as st
import math
import random
from itertools import combinations

# 1. Βασικές Ρυθμίσεις
st.set_page_config(page_title="BigBet Pro Stable", layout="wide")

# 2. CSS - Μόνο τα απαραίτητα για ταχύτητα
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    .white-box {
        background-color: #FFFFFF; 
        padding: 15px; 
        border-radius: 10px; 
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    .total-matches-label {
        font-size: 26px !important; font-weight: bold; color: #0D47A1;
        text-align: center; padding: 10px; background-color: #FFD700;
        border-radius: 10px; border: 2px solid #DAA520;
    }
    /* Μικρά inputs για το Από/Έως */
    div[data-testid="stHorizontalBlock"] input {
        height: 40px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Αρχικοποίηση
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

st.title("🏆 BigBet Pro Tool")

# --- ΜΑΖΙΚΗ ΕΙΣΑΓΩΓΗ (Compact & Side-by-Side) ---
st.markdown('<div class="white-box"><b>🔗 Μαζική Εισαγωγή</b>', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 1, 1.5])
with c1:
    s_val = st.text_input("ΑΠΟ", key="s_range", max_chars=3, placeholder="Από", label_visibility="collapsed")
with c2:
    e_val = st.text_input("ΕΩΣ", key="e_range", max_chars=3, placeholder="Έως", label_visibility="collapsed")
with c3:
    if st.button("Προσθήκη Εύρους ➕"):
        if s_val.isdigit() and e_val.isdigit():
            s, e = int(s_val), int(e_val)
            if s <= e:
                for code in range(s, e + 1):
                    fmt_code = str(code).zfill(3)
                    if not any(x['Κ'] == fmt_code for x in st.session_state.my_bet):
                        st.session_state.my_bet.append({"Κ": fmt_code, "Σ": "1"})
                st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- ΚΕΝΤΡΙΚΗ ΕΙΣΑΓΩΓΗ ---
st.markdown('<div class="white-box">', unsafe_allow_html=True)
current_key = f"in_{st.session_state.input_counter}"
u_input = st.text_input("📍 ΕΙΣΑΓΩΓΗ ΚΩΔΙΚΟΥ", key=current_key, max_chars=3)
st.markdown('</div>', unsafe_allow_html=True)

# --- ΧΡΥΣΟΣ ΜΕΤΡΗΤΗΣ ---
st.markdown(f'<div class="total-matches-label">ΣΥΝΟΛΟ ΑΓΩΝΩΝ: {len(st.session_state.my_bet)}</div>', unsafe_allow_html=True)

if len(u_input) == 3 and u_input.isdigit():
    st.session_state.my_bet.append({"Κ": u_input, "Σ": "1"})
    st.session_state.input_counter += 1
    st.rerun()

# --- ΛΙΣΤΑ ΚΑΙ ΑΝΑΠΤΥΞΗ ---
if st.session_state.my_bet:
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("📋 Λίστα")
        opts = ["1", "X", "2", "G/G", "N/G", "Over 2.5", "Under 2.5", "1X", "X2"]
        for i in range(len(st.session_state.my_bet)-1, -1, -1):
            item = st.session_state.my_bet[i]
            cl1, cl2, cl3 = st.columns([1, 2, 0.8])
            with cl1: st.write(f"**{item['Κ']}**")
            with cl2: st.session_state.my_bet[i]['Σ'] = st.selectbox(f"sel_{i}", opts, key=f"s_{i}", index=opts.index(item['Σ']), label_visibility="collapsed")
            with cl3:
                if st.button("❌", key=f"d_{i}"):
                    st.session_state.my_bet.pop(i)
                    st.rerun()

    with col_r:
        st.subheader("🔢 Σύστημα")
        n = len(st.session_state.my_bet)
        k = st.number_input("Ζητούμενα:", 1, max(1, n), min(n, 3))
        total = math.comb(n, k)
        st.metric("Σύνολο Στηλών", f"{total:,}")
        
        if total > 0:
            if total <= 300: # Χαμηλό όριο για ασφάλεια
                if st.checkbox("Εμφάνιση Όλων"):
                    for combo in combinations(st.session_state.my_bet, k):
                        st.text(" · ".join([f"{x['Κ']}[{x['Σ']}]" for x in combo]))
            else:
                st.info("💡 Πολλές στήλες. Χρησιμοποίησε το 'Τυχαίες'.")
                num_r = st.number_input("Πόσες τυχαίες;", 1, total, 10)
                if st.button("✨ Παραγωγή"):
                    all_c = list(combinations(st.session_state.my_bet, k))
                    for c in random.sample(all_c, num_r):
                        st.text(" · ".join([f"{x['Κ']}[{x['Σ']}]" for x in c]))

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ ΟΛΩΝ"):
        st.session_state.my_bet = []
        st.rerun()
