import streamlit as st
import random
from itertools import combinations
from fpdf import FPDF
import io

# 1. ΑΡΧΙΚΟΠΟΙΗΣΗ SESSION STATE
if 'options' not in st.session_state:
    st.session_state.options = ["1", "X", "2", "G/G", "N/G", "Over 2.5", "Under 2.5"]
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'last_random_combos' not in st.session_state: st.session_state.last_random_combos = []

st.set_page_config(page_title="BigBet Printer Pro", layout="wide")

# 2. CSS ΓΙΑ MOBILE & ΧΡΩΜΑΤΑ
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    div[data-baseweb="select"] input { inputmode: none !important; }
    input { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; font-weight: bold !important; }
    .column-box { background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 5px solid #0D47A1; margin-bottom: 5px; font-family: monospace; }
    .random-box { background-color: #FFF9C4; padding: 10px; border-radius: 5px; border-left: 5px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. ΣΥΝΑΡΤΗΣΗ ΔΗΜΙΟΥΡΓΙΑΣ PDF (ΕΚΤΥΠΩΣΗ)
def create_pdf(combos):
    # Landscape προσανατολισμός
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)
    
    # ΡΥΘΜΙΣΕΙΣ ΑΠΟ ΤΙΣ ΜΕΤΡΗΣΕΙΣ ΣΟΥ (mm)
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
        # ΔΙΠΛΑΣΙΟ ΜΕΓΕΘΟΣ Χ (Μέγεθος 28, Bold)
        pdf.set_font("Courier", style='B', size=28) 
        
        for i, match in enumerate(combo):
            # Μικρή διόρθωση στο Y για να κεντράρει το μεγάλο Χ στη γραμμή
            current_y = start_y + (i * row_height)
            
            # 1. Εκτύπωση Κωδικού (3 Χ)
            for j in range(3):
                # Χρησιμοποιούμε pdf.text για ακρίβεια θέσης
                pdf.text(start_x_code + (j * digit_spacing), current_y, "X")
            
            # 2. Εκτύπωση Σημείου (1, Χ ή 2)
            point = match['Σ']
            if point in points_map:
                target_x = points_map[point]
                pdf.text(target_x, current_y, "X")

    return pdf.output(dest='S').encode('latin-1')

# 4. ΛΕΙΤΟΥΡΓΙΕΣ UI
def randomize_points():
    pool = st.session_state.filter_points if st.session_state.filter_points else st.session_state.options
    for i in range(len(st.session_state.my_bet)):
        new_val = random.choice(pool)
        st.session_state.my_bet[i]['Σ'] = new_val
        st.session_state[f"sel_{i}"] = new_val

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
    st.multiselect("🎯 Φίλτρο Τυχαίων Σημείων:", st.session_state.options, key="filter_points")
    st.button("🎲 ΤΥΧΑΙΑ ΣΥΜΠΛΗΡΩΣΗ ΑΓΩΝΩΝ", on_click=randomize_points, use_container_width=True)
    
    st.subheader(f"Αγώνες: {len(st.session_state.my_bet)}")
    for i, item in enumerate(st.session_state.my_bet):
        col_k, col_s, col_d = st.columns([0.6, 2, 0.5])
        col_k.write(f"**{item['Κ']}**")
        choice = col_s.selectbox(f"Σημείο {i}", st.session_state.options, 
                                index=st.session_state.options.index(item['Σ']) if item['Σ'] in st.session_state.options else 0,
                                key=f"sel_{i}", label_visibility="collapsed")
        st.session_state.my_bet[i]['Σ'] = choice
        if col_d.button("✕", key=f"del_{i}"):
            st.session_state.my_bet.pop(i)
            st.rerun()

# --- ΑΝΑΠΤΥΞΗ & ΕΚΤΥΠΩΣΗ ---
if st.session_state.my_bet:
    st.divider()
    n = len(st.session_state.my_bet)
    k = st.number_input("Ζητούμενα (Σύστημα)", 1, n, min(n, 3) if n>=3 else 1)
    
    all_combos = list(combinations(st.session_state.my_bet, k))
    total_columns = len(all_combos)
    st.info(f"Σύνολο Πλήρους Ανάπτυξης: **{total_columns} στήλες**")

    with st.form("random_gen_form"):
        num_to_gen = st.number_input("Πόσες τυχαίες στήλες θέλεις;", 1, total_columns, min(total_columns, 10))
        submit_btn = st.form_submit_button("🎰 ΠΑΡΑΓΩΓΗ ΤΥΧΑΙΩΝ ΣΤΗΛΩΝ", use_container_width=True)
        if submit_btn:
            st.session_state.last_random_combos = random.sample(all_combos, int(num_to_gen))

    if st.session_state.last_random_combos:
        st.write(f"🎰 **Τυχαίες Στήλες ({len(st.session_state.last_random_combos)}):**")
        for idx, combo in enumerate(st.session_state.last_random_combos):
            txt = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="random-box">Στήλη {idx+1}: {txt}</div>', unsafe_allow_html=True)
        
        # ΚΟΥΜΠΙ ΕΚΤΥΠΩΣΗΣ PDF
        pdf_bytes = create_pdf(st.session_state.last_random_combos)
        st.download_button(
            label="🖨️ ΚΑΤΕΒΑΣΜΑ PDF ΓΙΑ ΕΚΤΥΠΩΣΗ",
            data=pdf_bytes,
            file_name="bet_print.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ ΟΛΩΝ"):
        st.session_state.my_bet = []
        st.session_state.last_random_combos = []
        st.rerun()
