import streamlit as st
import random
from itertools import combinations
from fpdf import FPDF
import io

# 1. ΑΡΧΙΚΟΠΟΙΗΣΗ SESSION STATE
if 'options' not in st.session_state:
    st.session_state.options = [
        "1", "X", "2", "1X", "X2", "12", "G/G", "N/G", 
        "Over 1.5", "Under 1.5", "Over 2.5", "Under 2.5", "Over 3.5", "Under 3.5",
        "Γ Over 0.5", "Φ Over 0.5", "Γ Over 1.5", "Φ Over 1.5", 
        "Γ Over 2.5", "Φ Over 2.5", "Γ Over 3.5", "Φ Over 3.5"
    ]
if 'my_bet' not in st.session_state: st.session_state.my_bet = []

st.set_page_config(page_title="BigBet Printer Pro", layout="wide")

# 2. CSS (ΕΥΑΓΓΕΛΙΟ)
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    input { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; font-weight: bold !important; }
    .column-box { background-color: #ffffff; padding: 8px; border-radius: 5px; border-left: 5px solid #0D47A1; margin-bottom: 5px; font-family: monospace; border: 1px solid #ddd; }
    .random-box { background-color: #FFF9C4; padding: 10px; border-radius: 5px; border-left: 5px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. ΣΥΝΑΡΤΗΣΕΙΣ (ΕΥΑΓΓΕΛΙΟ)
def create_pdf(combos):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)
    start_x_code = 20  
    start_y = 24       
    row_height = 4     
    digit_spacing = 4.0 
    radius = 1.8 # ΤΟ ΜΕΓΕΘΟΣ ΕΥΑΓΓΕΛΙΟ
    points_map = {"1": 83.0, "X": 89.0, "2": 95.0}

    for combo in combos:
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0)
        for i, match in enumerate(combo):
            current_y = start_y + (i * row_height)
            for j in range(3):
                pdf.ellipse(start_x_code + (j * digit_spacing), current_y - radius, radius*2, radius*2, style='F')
            point = match['Σ']
            if point in points_map:
                pdf.ellipse(points_map[point], current_y - radius, radius*2, radius*2, style='F')
    return pdf.output(dest='S').encode('latin-1')

st.title("🏆 BigBet Printer Pro")

# --- ΕΙΣΑΓΩΓΗ ΑΓΩΝΩΝ ---
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

# --- ΛΙΣΤΑ ΑΓΩΝΩΝ ---
if st.session_state.my_bet:
    st.divider()
    for i, item in enumerate(st.session_state.my_bet):
        col1, col2, col3 = st.columns([0.5, 2, 0.5])
        col1.write(f"**{item['Κ']}**")
        choice = col2.selectbox(f"Σ {i}", st.session_state.options, index=st.session_state.options.index(item['Σ']), key=f"sel_{i}", label_visibility="collapsed")
        st.session_state.my_bet[i]['Σ'] = choice
        if col3.button("✕", key=f"del_{i}"):
            st.session_state.my_bet.pop(i)
            st.rerun()

    # --- ΕΝΟΤΗΤΑ ΑΝΑΠΤΥΞΗΣ (ΜΟΝΟ ΜΕ ΕΝΤΟΛΗ) ---
    st.divider()
    st.subheader("📊 Ρυθμίσεις Ανάπτυξης")
    
    with st.form("analysis_form"):
        n = len(st.session_state.my_bet)
        k = st.number_input("Ζητούμενα (Σύστημα)", 1, n, min(n, 3) if n>=3 else 1)
        submit_button = st.form_submit_button("🚀 ΕΚΤΕΛΕΣΗ ΑΝΑΠΤΥΞΗΣ", use_container_width=True)

    if submit_button:
        all_combos = list(combinations(st.session_state.my_bet, k))
        st.success(f"Ολοκληρώθηκε! Δημιουργήθηκαν **{len(all_combos)}** στήλες.")
        
        # Λήψη PDF
        pdf_all = create_pdf(all_combos)
        st.download_button("🖨️ ΚΑΤΕΒΑΣΜΑ PDF ΟΛΩΝ ΤΩΝ ΣΤΗΛΩΝ", pdf_all, "bet_full.pdf", use_container_width=True)
        
        # Προβολή Στηλών
        for idx, combo in enumerate(all_combos):
            txt = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="column-box">Στήλη {idx+1}: {txt}</div>', unsafe_allow_html=True)

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ ΟΛΩΝ"):
        st.session_state.my_bet = []
        st.rerun()
