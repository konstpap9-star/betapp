import streamlit as st
import random
import math
from itertools import combinations
from fpdf import FPDF

# 1. SESSION STATE
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'last_random_combos' not in st.session_state: st.session_state.last_random_combos = []
# Όλες οι επιλογές σημείων
options = ["1", "X", "2", "Over 1.5", "Over 2.5", "Over 3.5", "Γ Over 0.5", "Φ Over 0.5"]

st.set_page_config(page_title="BigBet Printer Pro", layout="wide")

# 2. CSS - Κίτρινο πλαίσιο και στυλ
st.markdown("""
<style>
.stApp { background-color: #E3F2FD; }
.total-columns { width: 66%; font-size: 32px; color: #0D47A1; font-weight: bold; text-align: center; padding: 10px; background: #FFFF00; border-radius: 12px; border: 3px solid #FBC02D; margin: 20px auto; }
.random-box { background-color: #FFF9C4; padding: 10px; border-radius: 5px; border-left: 5px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# 3. ΣΥΝΑΡΤΗΣΗ PDF (ΒΑΣΙΚΗ - LANDSCAPE ΟΠΩΣ ΤΟ ΑΡΧΙΚΟ)
def create_pdf(combos):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)
    for combo in combos:
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0)
        for i, match in enumerate(combo):
            y = 24 + (i * 4.0)
            # Κωδικός
            for j in range(3): pdf.ellipse(20 + (j * 4.0), y - 1.8, 3.6, 3.6, style='F')
            # Σημείο (Ενδεικτική θέση για το βασικό Ευαγγέλιο)
            pdf.ellipse(83.0, y - 1.8, 3.6, 3.6, style='F')
    return pdf.output(dest='S').encode('latin-1')

# --- UI ---
st.title("🏆 BigBet Printer Pro - Ευαγγέλιο")

c1, c2 = st.columns(2)
s_range = c1.text_input("ΑΠΟ", value="100")
e_range = c2.text_input("ΕΩΣ", value="105")

col_btn1, col_btn2 = st.columns(2)
if col_btn1.button("➕ ΠΡΟΣΘΗΚΗ ΑΓΩΝΩΝ", use_container_width=True):
    for code in range(int(s_range), int(e_range) + 1):
        fmt = str(code).zfill(3)
        if not any(d['Κ'] == fmt for d in st.session_state.my_bet):
            st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})
    st.rerun()

if col_btn2.button("🎲 ΤΥΧΑΙΑ ΣΗΜΕΙΑ", use_container_width=True):
    for i in range(len(st.session_state.my_bet)):
        st.session_state.my_bet[i]['Σ'] = random.choice(options)
    st.rerun()

if st.session_state.my_bet:
    st.divider()
    for i, item in enumerate(st.session_state.my_bet):
        cols = st.columns([1, 4, 1])
        cols[0].write(f"**{item['Κ']}**")
        st.session_state.my_bet[i]['Σ'] = cols[1].selectbox(f"Σημείο {i}", options, index=options.index(item['Σ']), key=f"sel_{i}", label_visibility="collapsed")
        if cols[2].button("✕", key=f"del_{i}"):
            st.session_state.my_bet.pop(i)
            st.rerun()

    st.divider()
    n = len(st.session_state.my_bet)
    k = st.number_input("Σύστημα", 1, n, min(n, 3) if n>=3 else 1)
    st.markdown(f'<div class="total-columns">{math.comb(n, k)} στήλες</div>', unsafe_allow_html=True)

    if st.button("🎰 ΠΑΡΑΓΩΓΗ & ΕΚΤΥΠΩΣΗ", use_container_width=True):
        all_c = list(combinations(st.session_state.my_bet, k))
        st.session_state.last_random_combos = random.sample(all_c, min(len(all_c), 20))
        pdf_data = create_pdf(st.session_state.last_random_combos)
        st.download_button("🖨️ ΛΗΨΗ PDF", pdf_data, "bet.pdf", "application/pdf", use_container_width=True)

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ", use_container_width=True):
        st.session_state.my_bet = []
        st.session_state.last_random_combos = []
        st.rerun()
