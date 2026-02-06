import streamlit as st
import random
import math
from itertools import combinations
from fpdf import FPDF
import io

# 1. SESSION STATE (ΕΥΑΓΓΕΛΙΟ)
if 'options' not in st.session_state:
    st.session_state.options = [
        "1", "X", "2", "Over 1.5", "Over 2.5", "Over 3.5", 
        "Γ Over 0.5", "Φ Over 0.5"
    ]
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'last_random_combos' not in st.session_state: st.session_state.last_random_combos = []

st.set_page_config(page_title="BigBet Printer Pro", layout="wide")

# 2. CSS - Κίτρινο πλαίσιο 2/3 και στυλ
st.markdown("""
<style>
.stApp { background-color: #E3F2FD; }
input { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; font-weight: bold !important; }
.total-columns { width: 66%; font-size: 32px; color: #0D47A1; font-weight: bold; text-align: center; padding: 10px; background: #FFFF00; border-radius: 12px; border: 3px solid #FBC02D; margin: 20px auto; }
.random-box { background-color: #FFF9C4; padding: 10px; border-radius: 5px; border-left: 5px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# 3. ΣΥΝΑΡΤΗΣΗ PDF (PORTRAIT ΒΑΣΕΙ ΦΩΤΟΓΡΑΦΙΩΝ)
def create_pdf(combos):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)
    
    # Συντεταγμένες X (Πλάτος)
    X_CODE = 20.0   # Κωδικός αγώνα
    X_BASE_1 = 83.0  # Σημείο 1
    X_BASE_X = 89.0  # Σημείο X
    X_BASE_2 = 95.0  # Σημείο 2
    
    # Χάρτης Ειδικών (Βάσει των πεδίων που μου έδειξες)
    X_MAP = {
        "Φ Over 0.5": 101.0, # Πεδίο 1
        "Γ Over 0.5": 109.0, # Πεδίο 3
        "Over 3.5": 117.0,   # Πεδίο 5
        "Over 1.5": 125.0,   # Πεδίο 7
        "Over 2.5": 133.0    # Πεδίο 9
    }

    radius = 1.8
    for combo in combos:
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0)
        for i, match in enumerate(combo):
            y = 24 + (i * 4) # Κάθε αγώνας 4mm πιο κάτω
            
            # Κωδικός (3 κουκίδες)
            for j in range(3):
                pdf.ellipse(X_CODE + (j * 4.0), y - radius, radius*2, radius*2, style='F')
            
            # Σημείο
            s = match['Σ']
            if s == "1": pdf.ellipse(X_BASE_1, y - radius, radius*2, radius*2, style='F')
            elif s == "X": pdf.ellipse(X_BASE_X, y - radius, radius*2, radius*2, style='F')
            elif s == "2": pdf.ellipse(X_BASE_2, y - radius, radius*2, radius*2, style='F')
            elif s in X_MAP:
                pdf.ellipse(X_MAP[s], y - radius, radius*2, radius*2, style='F')
                
    return pdf.output(dest='S').encode('latin-1')

# --- UI LOGIC ---
st.title("🏆 BigBet Printer Pro")

c1, c2 = st.columns(2)
s_range = c1.text_input("ΑΠΟ", key="s", max_chars=3)
e_range = c2.text_input("ΕΩΣ", key="e", max_chars=3)

if st.button("ΠΡΟΣΘΗΚΗ ΕΥΡΟΥΣ ➕", use_container_width=True):
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
        st.session_state.my_bet[i]['Σ'] = col_s.selectbox(
            f"Σ {i}", st.session_state.options, 
            index=st.session_state.options.index(item['Σ']) if item['Σ'] in st.session_state.options else 0,
            key=f"sel_{i}", label_visibility="collapsed"
        )
        if col_d.button("✕", key=f"del_{i}"):
            st.session_state.my_bet.pop(i)
            st.rerun()

    st.divider()
    n = len(st.session_state.my_bet)
    k = st.number_input("Σύστημα", 1, n, min(n, 3) if n>=3 else 1)
    
    total_c = math.comb(n, k)
    st.markdown(f'<div class="total-columns">{total_c} στήλες</div>', unsafe_allow_html=True)
    
    with st.form("gen_form"):
        num_to_gen = st.number_input("Πόσες τυχαίες στήλες;", 1, total_c, min(total_c, 10))
        if st.form_submit_button("🎰 ΠΑΡΑΓΩΓΗ", use_container_width=True):
            all_combos = list(combinations(st.session_state.my_bet, k))
            st.session_state.last_random_combos = random.sample(all_combos, int(num_to_gen))

    if st.session_state.last_random_combos:
        for idx, combo in enumerate(st.session_state.last_random_combos):
            txt = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="random-box">Στήλη {idx+1}: {txt}</div>', unsafe_allow_html=True)
        
        pdf_bytes = create_pdf(st.session_state.last_random_combos)
        st.download_button("🖨️ ΚΑΤΕΒΑΣΜΑ PDF", data=pdf_bytes, file_name="bet_print.pdf", mime="application/pdf", use_container_width=True)

    # ΤΟ ΚΟΥΜΠΙ ΚΑΘΑΡΙΣΜΟΥ ΠΟΥ ΕΛΕΙΠΕ
    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ", use_container_width=True):
        st.session_state.my_bet = []
        st.session_state.last_random_combos = []
        st.rerun()
