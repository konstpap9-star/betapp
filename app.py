import streamlit as st
import random
from itertools import combinations
from fpdf import FPDF
import io

# 1. ΑΡΧΙΚΟΠΟΙΗΣΗ
if 'options' not in st.session_state:
    st.session_state.options = ["1", "X", "2"] # Ξεκινάμε με τα βασικά όπως είπες
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'last_random_combos' not in st.session_state: st.session_state.last_random_combos = []

st.set_page_config(page_title="BigBet Printer Pro", layout="wide")

# 2. CSS 
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    .random-box { background-color: #FFF9C4; padding: 10px; border-radius: 5px; border-left: 5px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. ΣΥΝΑΡΤΗΣΗ PDF
def create_pdf(combos):
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)
    
    # ΡΥΘΜΙΣΕΙΣ ΑΚΡΙΒΕΙΑΣ (mm)
    start_x_code = 20    # Απόσταση Α (Κωδικός)
    start_y = 24         # Απόσταση Β (Πρώτη σειρά)
    row_height = 4       # Απόσταση μεταξύ σειρών
    digit_spacing = 4.0  # Απόσταση ανάμεσα στα ψηφία του κωδικού
    
    # ΣΥΝΤΕΤΑΓΜΕΝΕΣ ΣΗΜΕΙΩΝ (Απόσταση από αριστερή άκρη)
    points_map = {
        "1": 83.0,
        "X": 89.0,
        "2": 95.0
    }

    for combo in combos:
        pdf.add_page()
        # Μεγαλύτερη και Έντονη γραμματοσειρά για τα Χ
        pdf.set_font("Courier", style='B', size=14) 
        
        for i, match in enumerate(combo):
            current_y = start_y + (i * row_height)
            
            # 1. Εκτύπωση Κωδικού
            code = str(match['Κ']).zfill(3)
            for j, digit in enumerate(code):
                # Αν το ψηφίο είναι '0' ή κενό, το χειριζόμαστε ανάλογα. 
                # Εδώ τυπώνουμε Χ στη θέση του κάθε ψηφίου που αντιστοιχεί στον κωδικό
                pdf.text(start_x_code + (j * digit_spacing), current_y, "X")
            
            # 2. Εκτύπωση Σημείου (1, Χ ή 2)
            point = match['Σ']
            if point in points_map:
                target_x = points_map[point]
                pdf.text(target_x, current_y, "X")

    return pdf.output(dest='S').encode('latin-1')

# --- ΤΟ ΥΠΟΛΟΙΠΟ INTERFACE (ΣΥΝΤΟΜΕΥΜΕΝΟ) ---
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

# Λίστα αγώνων και επιλογή σημείου
for i, item in enumerate(st.session_state.my_bet):
    col_k, col_s = st.columns([1, 2])
    col_k.write(f"Κωδ: **{item['Κ']}**")
    st.session_state.my_bet[i]['Σ'] = col_s.selectbox(f"Σημείο {i}", ["1", "X", "2"], 
                                                     index=["1", "X", "2"].index(item['Σ']),
                                                     key=f"sel_{i}", label_visibility="collapsed")

if st.session_state.my_bet:
    st.divider()
    n = len(st.session_state.my_bet)
    k = st.number_input("Ζητούμενα", 1, n, min(n, 3) if n>=3 else 1)
    all_combos = list(combinations(st.session_state.my_bet, k))
    
    with st.form("gen"):
        num = st.number_input("Τυχαίες στήλες", 1, len(all_combos), 1)
        if st.form_submit_button("🎰 ΠΑΡΑΓΩΓΗ"):
            st.session_state.last_random_combos = random.sample(all_combos, int(num))

    if st.session_state.last_random_combos:
        pdf_bytes = create_pdf(st.session_state.last_random_combos)
        st.download_button("🖨️ ΚΑΤΕΒΑΣΜΑ PDF", data=pdf_bytes, file_name="bet.pdf", mime="application/pdf")
