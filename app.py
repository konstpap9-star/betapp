import streamlit as st
import random
import math
from itertools import combinations
from fpdf import FPDF
import io

# 1. SESSION STATE (ΕΥΑΓΓΕΛΙΟ)
if 'my_bet' not in st.session_state:
    st.session_state.my_bet = []
if 'last_random_combos' not in st.session_state:
    st.session_state.last_random_combos = []

st.set_page_config(page_title="BigBet Printer Pro", layout="wide")

# 2. CSS - Κίτρινο πλαίσιο 2/3 και στυλ
st.markdown("""
<style>
.stApp { background-color: #E3F2FD; }
input { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; font-weight: bold !important; }
.total-columns {
    width: 66%;
    font-size: 32px;
    color: #0D47A1;
    font-weight: bold;
    text-align: center;
    padding: 10px;
    background: #FFFF00;
    border-radius: 12px;
    border: 3px solid #FBC02D;
    margin: 20px auto;
}
.random-box {
    background-color: #FFF9C4;
    padding: 10px;
    border-radius: 5px;
    border-left: 5px solid #FBC02D;
    color: #0D47A1;
    font-weight: bold;
    margin-bottom: 5px;
}
</style>
""", unsafe_allow_html=True)

# 3. ΣΥΝΑΡΤΗΣΗ PDF (ΒΑΣΙΚΗ ΕΚΔΟΣΗ)
def create_pdf(combos):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)
    
    start_y = 24
    x_digits = 20
    x_point_1 = 83.0
    x_point_x = 89.0
    x_point_2 = 95.0
    radius = 1.8

    for combo in combos:
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0)
        for i, match in enumerate(combo):
            y = start_y + (i * 4.0)
            # Κωδικός (3 κουκίδες)
            for j in range(3):
                pdf.ellipse(x_digits + (j * 4.0), y - radius, radius*2, radius*2, style='F')
            
            # Σημείο
            s = match['Σ']
            if s == "1":
                pdf.ellipse(x_point_1, y - radius, radius*2, radius*2, style='F')
            elif s == "X":
                pdf.ellipse(x_point_x, y - radius, radius*2, radius*2, style='F')
            elif s == "2":
                pdf.ellipse(x_point_2, y - radius, radius*2, radius*2, style='F')
                
    return pdf.output(dest='S').encode('latin-1')

# --- UI LOGIC ---
st.title("🏆 BigBet Printer Pro")

# Εισαγωγή εύρους
c1, c2 = st.columns(2)
s_range = c1.text_input("ΑΠΟ (π.χ. 100)", key="s", max_chars=3)
e_range = c2.text_input("ΕΩΣ (π.χ. 110)", key="e", max_chars=3)

if st.button("ΠΡΟΣΘΗΚΗ ΕΥΡΟΥΣ ➕", use_container_width=True):
    if s_range.isdigit() and e_range.isdigit():
        for code in range(int(s_range), int(e_range) + 1):
            fmt_code = str(code).zfill(3)
            if not any(d['Κ'] == fmt_code for d in st.session_state.my_bet):
                st.session_state.my_bet.append({"Κ": fmt_code, "Σ": "1"})
        st.rerun()

# Λίστα αγώνων
if st.session_state.my_bet:
    st.divider()
    for i, item in enumerate(st.session_state.my_bet):
        col_k, col_s, col_d = st.columns([0.6, 2, 0.5])
        col_k.write(f"**{item['Κ']}**")
        st.session_state.my_bet[i]['Σ'] = col_s.selectbox(
            f"Σημείο {i}", ["1", "X", "2"], 
            index=["1", "X", "2"].index(item['Σ']),
            key=f"sel_{i}", label_visibility="collapsed"
        )
        if col_d.button("✕", key=f"del_{i}"):
            st.session_state.my_bet.pop(i)
            st.rerun()

    st.divider()
    
    # Σύστημα
    n = len(st.session_state.my_bet)
    k = st.number_input("Επιλέξτε Σύστημα (π.χ. 3 από 5)", 1, n, min(n, 3) if n >= 3 else 1)
    
    total_combos = math.comb(n, k)
    st.markdown(f'<div class="total-columns">{total_combos} στήλες</div>', unsafe_allow_html=True)
    
    # Παραγωγή τυχαίων
    with st.form("gen_form"):
        num_to_gen = st.number_input("Πόσες τυχαίες στήλες να παραχθούν;", 1, total_combos, min(total_combos, 10))
        if st.form_submit_button("🎰 ΠΑΡΑΓΩΓΗ ΤΥΧΑΙΩΝ ΣΤΗΛΩΝ", use_container_width=True):
            all_combos = list(combinations(st.session_state.my_bet, k))
            st.session_state.last_random_combos = random.sample(all_combos, int(num_to_gen))

    # Προβολή και Εκτύπωση
    if st.session_state.last_random_combos:
        for idx, combo in enumerate(st.session_state.last_random_combos):
            combo_text = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="random-box">Στήλη {idx+1}: {combo_text}</div>', unsafe_allow_html=True)
        
        pdf_bytes = create_pdf(st.session_state.last_random_combos)
        st.download_button(
            label="🖨️ ΕΚΤΥΠΩΣΗ ΣΕ PDF",
            data=pdf_bytes,
            file_name="bet_pro.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    # Καθαρισμός
    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ ΟΛΩΝ", use_container_width=True):
        st.session_state.my_bet = []
        st.session_state.last_random_combos = []
        st.rerun()
