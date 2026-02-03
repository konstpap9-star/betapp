import streamlit as st
import random
import math
from itertools import combinations
import io

# 1. ΒΑΣΙΚΕΣ ΡΥΘΜΙΣΕΙΣ
if 'options' not in st.session_state:
    st.session_state.options = ["1", "X", "2", "1X", "X2", "12", "G/G", "N/G", "Over 2.5", "Under 2.5"]
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'last_random_combos' not in st.session_state: st.session_state.last_random_combos = []

st.set_page_config(page_title="BigBet Unlimited Pro", layout="wide")

# 2. CSS 
st.markdown("""
<style>
.stApp { background-color: #F0F2F6; }
.random-box { background-color: #FFF; padding: 5px; border-left: 5px solid #0D47A1; margin-bottom: 2px; font-family: monospace; font-size: 12px; }
.total-columns { font-size: 28px; color: #0D47A1; font-weight: bold; text-align: center; padding: 10px; background: #FFFF00; border-radius: 12px; border: 2px solid #FBC02D; width: 66%; margin: auto; }
</style>
""", unsafe_allow_html=True)

# 3. UI
st.title("🚀 BigBet Unlimited (High Capacity)")

c1, c2 = st.columns(2)
s_range = c1.text_input("ΑΠΟ", key="s", max_chars=3)
e_range = c2.text_input("ΕΩΣ", key="e", max_chars=3)

if st.button("ΠΡΟΣΘΗΚΗ ΕΥΡΟΥΣ ➕"):
    if s_range.isdigit() and e_range.isdigit():
        for code in range(int(s_range), int(e_range) + 1):
            fmt = str(code).zfill(3)
            if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
                st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})
        st.rerun()

if st.session_state.my_bet:
    st.divider()
    for i, item in enumerate(st.session_state.my_bet):
        col_k, col_s, col_d = st.columns([0.6, 2, 0.5])
        col_k.write(f"**{item['Κ']}**")
        st.session_state.my_bet[i]['Σ'] = col_s.selectbox(f"Σ {i}", st.session_state.options, index=0, key=f"sel_{i}", label_visibility="collapsed")
        if col_d.button("✕", key=f"del_{i}"):
            st.session_state.my_bet.pop(i)
            st.rerun()

    st.divider()
    n = len(st.session_state.my_bet)
    k = st.number_input("Σύστημα", 1, n, 3)
    
    total_c = math.comb(n, k)
    st.markdown(f'<div style="text-align:center; color:#0D47A1">Συνολικές Στήλες</div><div class="total-columns">{total_c}</div>', unsafe_allow_html=True)
    
    with st.form("unlimited_form"):
        num_to_gen = st.number_input("Πόσες τυχαίες στήλες να παραχθούν;", 1, total_c, 100)
        submitted = st.form_submit_button("🎰 ΠΑΡΑΓΩΓΗ & ΠΡΟΕΤΟΙΜΑΣΙΑ")

    if submitted:
        # Χρήση δειγματοληψίας χωρίς φόρτωμα όλης της λίστας στη μνήμη αν είναι εφικτό
        # Για πολύ μεγάλα νούμερα χρησιμοποιούμε random.sample απευθείας στους συνδυασμούς
        all_combos_gen = list(combinations(st.session_state.my_bet, k))
        st.session_state.last_random_combos = random.sample(all_combos_gen, int(num_to_gen))
        st.success(f"Επιτυχής παραγωγή {num_to_gen} στηλών!")

    if st.session_state.last_random_combos:
        # 1. ΕΜΦΑΝΙΣΗ ΔΕΙΓΜΑΤΟΣ (ΜΟΝΟ 10 ΓΙΑ ΤΑΧΥΤΗΤΑ)
        st.write("### Δείγμα πρώτων 10 στηλών:")
        for idx, combo in enumerate(st.session_state.last_random_combos[:10]):
            txt = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="random-box">Στήλη {idx+1}: {txt}</div>', unsafe_allow_html=True)
        
        # 2. ΕΞΑΓΩΓΗ ΣΕ TXT (ΑΠΕΡΙΟΡΙΣΤΗ ΧΩΡΗΤΙΚΟΤΗΤΑ)
        buffer = io.StringIO()
        for idx, combo in enumerate(st.session_state.last_random_combos):
            txt = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            buffer.write(f"Στήλη {idx+1}: {txt}\n")
        
        st.download_button(
            label="📄 ΚΑΤΕΒΑΣΜΑ ΟΛΩΝ ΤΩΝ ΣΤΗΛΩΝ (.TXT)",
            data=buffer.getvalue(),
            file_name="my_bets_unlimited.txt",
            mime="text/plain",
            use_container_width=True
        )

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ"):
        st.session_state.my_bet = []
        st.session_state.last_random_combos = []
        st.rerun()
