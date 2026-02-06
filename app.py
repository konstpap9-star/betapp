import streamlit as st
import random
import math
from itertools import combinations
from fpdf import FPDF
import io

# 1. ΒΑΣΙΚΕΣ ΡΥΘΜΙΣΕΙΣ (ΕΥΑΓΓΕΛΙΟ)
if 'options' not in st.session_state:
    st.session_state.options = [
        "1", "X", "2", "1X", "X2", "12", "G/G", "N/G", 
        "Over 1.5", "Under 1.5", "Over 2.5", "Under 2.5", "Over 3.5", "Under 3.5",
        "Γ Over 0.5", "Φ Over 0.5", "Γ Over 1.5", "Φ Over 1.5", 
        "Γ Over 2.5", "Φ Over 2.5", "Γ Over 3.5", "Φ Over 3.5"
    ]
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'last_random_combos' not in st.session_state: st.session_state.last_random_combos = []

st.set_page_config(page_title="BigBet Printer Pro", layout="wide")

# 2. CSS (ΕΥΑΓΓΕΛΙΟ - ΚΙΤΡΙΝΟ ΠΛΑΙΣΙΟ 2/3)
st.markdown("""
<style>
.stApp { background-color: #E3F2FD; }
div[data-baseweb="select"] input { inputmode: none !important; caret-color: transparent !important; }
input { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; font-weight: bold !important; }
div[data-baseweb="select"] > div { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; }
.column-box { background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 5px solid #0D47A1; margin-bottom: 5px; font-family: monospace; }
.random-box { background-color: #FFF9C4; padding: 10px; border-radius: 5px; border-left: 5px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 5px; }
.total-wrapper { display: flex; flex-direction: column; align-items: center; width: 100%; margin: 15px 0; }
.total-label { font-size: 14px; color: #0D47A1; font-weight: normal; margin-bottom: 2px; }
.total-columns { width: 66%; font-size: 32px; color: #0D47A1; font-weight: bold; text-align: center; padding: 10px; background: #FFFF00; border-radius: 12px; border: 3px solid #FBC02D; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# 3. ΣΥΝΑΡΤΗΣΗ PDF (ΕΥΑΓΓΕΛΙΟ - 1.8mm)
def create_pdf(combos):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)
    radius = 1.8 
    points_map = {"1": 83.0, "X": 89.0, "2": 95.0}
    for combo in combos:
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0)
        for i, match in enumerate(combo):
            current_y = 24 + (i * 4)
            for j in range(3):
                pdf.ellipse(20 + (j * 4.0), current_y - radius, radius*2, radius*2, style='F')
            point = match['Σ']
            if point in points_map:
                pdf.ellipse(points_map[point], current_y - radius, radius*2, radius*2, style='F')
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
    st.subheader(f"Αγώνες: {len(st.session_state.my_bet)}")
    for i, item in enumerate(st.session_state.my_bet):
        col_k, col_s, col_d = st.columns([0.6, 2, 0.5])
        col_k.write(f"**{item['Κ']}**")
        st.session_state.my_bet[i]['Σ'] = col_s.selectbox(f"Σ {i}", st.session_state.options, index=st.session_state.options.index(item['Σ']), key=f"sel_{i}", label_visibility="collapsed")
        if col_d.button("✕", key=f"del_{i}"):
            st.session_state.my_bet.pop(i)
            st.rerun()

    st.divider()
    n = len(st.session_state.my_bet)
    k = st.number_input("Σύστημα", 1, n, min(n, 3) if n>=3 else 1)
    
    total_c = math.comb(n, k)
    st.markdown(f'<div class="total-wrapper"><div class="total-label">στήλες</div><div class="total-columns">{total_c}</div></div>', unsafe_allow_html=True)
    
    with st.form("gen_form"):
        num_to_gen = st.number_input("Πόσες τυχαίες;", 1, total_c, min(total_c, 10))
        submitted = st.form_submit_button("🎰 ΠΑΡΑΓΩΓΗ", use_container_width=True)
        
    if submitted:
        all_combos = list(combinations(st.session_state.my_bet, k))
        st.session_state.last_random_combos = random.sample(all_combos, int(num_to_gen))

    if st.session_state.last_random_combos:
        # Εμφάνιση των πρώτων 50 στηλών στην οθόνη
        display_list = st.session_state.last_random_combos[:50]
        for idx, combo in enumerate(display_list):
            txt = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="random-box">Στήλη {idx+1}: {txt}</div>', unsafe_allow_html=True)
        
        if len(st.session_state.last_random_combos) > 50:
            st.warning("Εμφανίζονται οι πρώτες 50 στήλες. Όλες περιλαμβάνονται στο PDF.")

        st.download_button(
            "🖨️ ΚΑΤΕΒΑΣΜΑ PDF", 
            data=create_pdf(st.session_state.last_random_combos), 
            file_name="bet_print.pdf", 
            mime="application/pdf", 
            use_container_width=True
        )

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ"):
        st.session_state.my_bet = []
        st.session_state.last_random_combos = []
        st.rerun()
