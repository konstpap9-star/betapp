import streamlit as st
import random
import math
from itertools import combinations
from fpdf import FPDF

# --- SESSION STATE (ΕΥΑΓΓΕΛΙΟ) ---
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'last_random_combos' not in st.session_state: st.session_state.last_random_combos = []

st.set_page_config(page_title="BigBet Printer", layout="wide")

# --- CSS (Κίτρινο Πλαίσιο) ---
st.markdown("""
<style>
.stApp { background-color: #E3F2FD; }
.total-columns { width: 66%; font-size: 32px; color: #0D47A1; font-weight: bold; text-align: center; padding: 10px; background: #FFFF00; border-radius: 12px; border: 3px solid #FBC02D; margin: 20px auto; }
</style>
""", unsafe_allow_html=True)

# --- ΣΥΝΑΡΤΗΣΗ ΕΚΤΥΠΩΣΗΣ (ΜΕ ΤΙΣ ΝΕΕΣ ΣΥΝΤΕΤΑΓΜΕΝΕΣ) ---
def create_pdf(combos):
    # Ορίζουμε το μέγεθος ακριβώς όσο το δελτίο για να μη μπερδεύεται ο HP
    pdf = FPDF(orientation='P', unit='mm', format=(105, 230))
    pdf.set_auto_page_break(auto=False)
    
    # ΡΥΘΜΙΣΕΙΣ ΒΑΣΕΙ ΤΩΝ ΦΩΤΟΓΡΑΦΙΩΝ ΣΟΥ (IMG_20260206_231033)
    # Χ_START: Μετακίνηση τέρμα αριστερά για να βρει τους κωδικούς
    X_START = 6.0  
    Y_START = 18.0 
    
    # Χάρτης Σημείων (Μετατοπισμένος αριστερά για να μη βγαίνει εκτός)
    X_MAP = {
        "1": 65.0, "X": 71.0, "2": 77.0,
        "Φ Over 0.5": 83.0, "Γ Over 0.5": 87.0, 
        "Over 3.5": 91.0, "Over 1.5": 95.0, "Over 2.5": 99.0
    }

    radius = 1.7
    for combo in combos:
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0)
        for i, match in enumerate(combo):
            y = Y_START + (i * 4.45)
            
            # Κωδικός (3 κουκίδες)
            for j in range(3):
                pdf.ellipse(X_START + (j * 4.0), y - radius, radius*2, radius*2, style='F')
            
            # Σημείο
            s = match['Σ']
            if s in X_MAP:
                pdf.ellipse(X_MAP[s], y - radius, radius*2, radius*2, style='F')
                
    return pdf.output(dest='S').encode('latin-1')

# --- UI ---
st.title("🏆 BigBet Printer - Back Up 1.3")

c1, c2 = st.columns(2)
s_range = c1.text_input("ΑΠΟ (π.χ. 345)", value="345")
e_range = c2.text_input("ΕΩΣ (π.k. 348)", value="345")

if st.button("➕ ΠΡΟΣΘΗΚΗ ΑΓΩΝΩΝ"):
    for code in range(int(s_range), int(e_range) + 1):
        st.session_state.my_bet.append({"Κ": str(code).zfill(3), "Σ": "Over 2.5"})
    st.rerun()

if st.session_state.my_bet:
    for i, item in enumerate(st.session_state.my_bet):
        cols = st.columns([1, 4, 1])
        cols[0].write(f"**{item['Κ']}**")
        st.session_state.my_bet[i]['Σ'] = cols[1].selectbox(f"Σημείο {i}", ["1", "X", "2", "Over 1.5", "Over 2.5", "Over 3.5", "Γ Over 0.5", "Φ Over 0.5"], index=4, key=f"s_{i}")
        if cols[2].button("✕", key=f"del_{i}"):
            st.session_state.my_bet.pop(i)
