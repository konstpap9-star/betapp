import streamlit as st
import random
import math
from itertools import combinations
from fpdf import FPDF
import io

# 1. SESSION STATE (ΕΥΑΓΓΕΛΙΟ)
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'last_random_combos' not in st.session_state: st.session_state.last_random_combos = []

st.set_page_config(page_title="BigBet Printer Pro", layout="wide")

# 2. CSS - Κίτρινο πλαίσιο 2/3
st.markdown("""
<style>
.stApp { background-color: #E3F2FD; }
.total-columns { width: 66%; font-size: 32px; color: #0D47A1; font-weight: bold; text-align: center; padding: 10px; background: #FFFF00; border-radius: 12px; border: 3px solid #FBC02D; margin: auto; }
.random-box { background-color: #FFF9C4; padding: 10px; border-radius: 5px; border-left: 5px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# 3. ΧΑΡΤΗΣ ΕΚΤΥΠΩΣΗΣ (ΒΑΣΕΙ ΦΩΤΟΓΡΑΦΙΑΣ)
def create_pdf(combos):
    # Orientation P (Portrait) για τον HP σου
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)
    
    # Αποστάσεις από την αριστερή άκρη (X)
    X_CODE = 20.0  # Κωδικός
    X_BASE_1 = 83.0 # Σημείο 1
    X_BASE_X = 89.0 # Σημείο X
    X_BASE_2 = 95.0 # Σημείο 2
    
    # Ειδικά Στοιχήματα (Ανά 4mm βάσει της φωτό σου)
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
            y = 24 + (i * 4) # Κάθε αγώνας σε νέα γραμμή
            
            # Εκτύπωση Κωδικού (3 κουκίδες)
            for j in range(3):
                pdf.ellipse(X_CODE + (j * 4.0), y - radius, radius*2, radius*2, style='F')
            
            # Εκτύπωση Σημείου
            s = match['Σ']
            if s == "1": pdf.ellipse(X_BASE_1, y - radius, radius*2, radius*2, style='F')
            elif s == "X": pdf.ellipse(X_BASE_X, y - radius, radius*2, radius*2, style='F')
            elif s == "2": pdf.ellipse(X_BASE_2, y - radius, radius*2, radius*2, style='F')
            elif s in X_MAP:
                pdf.ellipse(X_MAP[s], y - radius, radius*2, radius*2, style='F')
                
    return pdf.output(dest='S').encode('latin-1')

# --- UI ---
st.title("🏆 BigBet Printer Pro (Back Up 1.1)")

c1, c2 = st.columns(2)
s_range = c1.text_input("ΑΠΟ", key="s")
e_range = c2.text_input("ΕΩΣ", key="e")

if st.button("ΠΡΟΣΘΗΚΗ ΑΓΩΝΩΝ"):
    for code in range(int(s_range), int(e_range) + 1):
        st.session_state.my_bet.append({"Κ": str(code).zfill(3), "Σ": "1"})
    st.rerun()

if st.session_state.my_bet:
    for i, item in enumerate(st.session_state.my_bet):
        cols = st.columns([1, 3, 1])
        cols[0].write(item['Κ'])
        st.session_state.my_bet[i]['Σ'] = cols[1].selectbox(f"Σημείο {i}", ["1", "X", "2", "Over 1.5", "Over 2.5", "Over 3.5", "Γ Over 0.5", "Φ Over 0.5"], key=f"s_{i}")

    n = len(st.session_state.my_bet)
    k = st.number_input("Σύστημα", 1, n, 3)
    st.markdown(f'<div class="total-columns">{math.comb(n, k)} στήλες</div>', unsafe_allow_html=True)

    if st.button("🎰 ΠΑΡΑΓΩΓΗ ΣΤΗΛΩΝ"):
        all_c = list(combinations(st.session_state.my_bet, k))
        st.session_state.last_random_combos = random.sample(all_c, min(len(all_c), 500))

    if st.session_state.last_random_combos:
        st.download_button("🖨️ ΕΚΤΥΠΩΣΗ PDF", create_pdf(st.session_state.last_random_combos), "bet.pdf", "application/pdf")
