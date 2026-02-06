import streamlit as st
import random
import math
from itertools import combinations
from fpdf import FPDF

# 1. SESSION STATE
if 'options' not in st.session_state:
    st.session_state.options = ["1", "X", "2", "Over 1.5", "Over 2.5", "Over 3.5", "Γ Over 0.5", "Φ Over 0.5"]
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'last_random_combos' not in st.session_state: st.session_state.last_random_combos = []

st.set_page_config(page_title="BigBet Printer Pro", layout="wide")

# 2. CSS - Κίτρινο πλαίσιο
st.markdown("""
<style>
.stApp { background-color: #E3F2FD; }
.total-columns { width: 66%; font-size: 32px; color: #0D47A1; font-weight: bold; text-align: center; padding: 10px; background: #FFFF00; border-radius: 12px; border: 3px solid #FBC02D; margin: 20px auto; }
.random-box { background-color: #FFF9C4; padding: 10px; border-radius: 5px; border-left: 5px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

# 3. Η ΔΙΟΡΘΩΜΕΝΗ ΣΥΝΑΡΤΗΣΗ PDF (Portrait - Στόχευση Ακριβείας)
def create_pdf(combos):
    # Ορίζουμε το μέγεθος σελίδας ακριβώς όσο το δελτίο (περίπου 105x230mm) 
    # για να μην μπερδεύεται ο HP με το Α4
    pdf = FPDF(orientation='P', unit='mm', format=(105, 230))
    pdf.set_auto_page_break(auto=False)
    
    # ΝΕΕΣ ΣΥΝΤΕΤΑΓΜΕΝΕΣ (Μετατόπιση προς τα πάνω και αριστερά)
    X_CODE_START = 6.0   # Η πρώτη κουκίδα του κωδικού (αριστερά)
    Y_FIRST_ROW = 18.0   # Το ύψος της πρώτης γραμμής αγώνα
    
    X_BASE_1 = 65.0      # Σημείο 1
    X_BASE_X = 71.0      # Σημείο X
    X_BASE_2 = 77.0      # Σημείο 2
    
    # Χάρτης Ειδικών (αποστάσεις 4mm μεταξύ τους)
    X_MAP = {
        "Φ Over 0.5": 83.0, 
        "Γ Over 0.5": 87.0, 
        "Over 3.5": 91.0,   
        "Over 1.5": 95.0,   
        "Over 2.5": 99.0    
    }

    radius = 1.6 # Ελαφρώς μικρότερη κουκίδα για καλύτερη εφαρμογή
    for combo in combos:
        pdf.add_page()
        pdf.set_fill_color(0, 0, 0)
        for i, match in enumerate(combo):
            y = Y_FIRST_ROW + (i * 4.45) # Το 4.45 είναι το βήμα της γραμμής του ΟΠΑΠ
            
            # Κωδικός (π.χ. 345)
            code_str = match['Κ']
            for idx, digit in enumerate(code_str):
                # Εδώ απλώς εκτυπώνουμε τις θέσεις των 3 ψηφίων
                pdf.ellipse(X_CODE_START + (idx * 3.8), y - radius, radius*2, radius*2, style='F')
            
            # Σημείο
            s = match['Σ']
            if s == "1": pdf.ellipse(X_BASE_1, y - radius, radius*2, radius*2, style='F')
            elif s == "X": pdf.ellipse(X_BASE_X, y - radius, radius*2, radius*2, style='F')
            elif s == "2": pdf.ellipse(X_BASE_2, y - radius, radius*2, radius*2, style='F')
            elif s in X_MAP:
                pdf.ellipse(X_MAP[s], y - radius, radius*2, radius*2, style='F')
                
    return pdf.output(dest='S').encode('latin-1')

# --- UI ---
st.title("🏆 BigBet Printer Pro v1.2")

c1, c2 = st.columns(2)
s_range = c1.text_input("ΑΠΟ", value="345")
e_range = c2.text_input("ΕΩΣ", value="345")

if st.button("ΠΡΟΣΘΗΚΗ ΑΓΩΝΩΝ"):
    if s_range.isdigit() and e_range.isdigit():
        for code in range(int(s_range), int(e_range) + 1):
            st.session_state.my_bet.append({"Κ": str(code).zfill(3), "Σ": "Over 2.5"})
        st.rerun()

if st.session_state.my_bet:
    for i, item in enumerate(st.session_state.my_bet):
        col1, col2 = st.columns([1, 4])
        col1.write(f"**{item['Κ']}**")
        st.session_state.my_bet[i]['Σ'] = col2.selectbox(f"Σημείο {i}", st.session_state.options, index=st.session_state.options.index(item['Σ']), key=f"sel_{i}")

    n = len(st.session_state.my_bet)
    k = st.number_input("Σύστημα", 1, n, 1)
    
    if st.button("🎰 ΠΑΡΑΓΩΓΗ & ΕΚΤΥΠΩΣΗ"):
        all_c = list(combinations(st.session_state.my_bet, k))
        st.session_state.last_random_combos = random.sample(all_c, 1) # Δοκιμή με 1 στήλη
        pdf_bytes = create_pdf(st.session_state.last_random_combos)
        st.download_button("🖨️ ΚΑΤΕΒΑΣΜΑ PDF ΔΟΚΙΜΗΣ", data=pdf_bytes, file_name="test.pdf")

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ"):
        st.session_state.my_bet = []
        st.session_state.last_random_combos = []
        st.rerun()
