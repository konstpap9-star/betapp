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
if 'last_random_combos' not in st.session_state: st.session_state.last_random_combos = []

st.set_page_config(page_title="BigBet Printer Pro", layout="wide")

# 2. CSS ΓΙΑ MOBILE FIX & ΧΡΩΜΑΤΑ
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    div[data-baseweb="select"] input { inputmode: none !important; caret-color: transparent !important; }
    input { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; font-weight: bold !important; }
    div[data-baseweb="select"] > div { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; }
    .column-box { background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 5px solid #0D47A1; margin-bottom: 5px; font-family: monospace; }
    .random-box { background-color: #FFF9C4; padding: 10px; border-radius: 5px; border-left: 5px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. ΣΥΝΑΡΤΗΣΕΙΣ ΛΕΙΤΟΥΡΓΙΑΣ
def randomize_points():
    pool = st.session_state.filter_points if st.session_state.filter_points else st.session_state.options
    for i in range(len(st.session_state.my_bet)):
        new_val = random.choice(pool)
        st.session_state.my_bet[i]['Σ'] = new_val
        st.session_state[f"sel_{i}"] = new_val

def create_pdf(combos):
    # Δημιουργία PDF σε οριζόντια διάταξη (Landscape)
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)
    
    # Οι μετρήσεις σου σε mm
    start_x = 20  # Απόσταση Α
    start_y = 24  # Απόσταση Β
    row_height = 4  # Απόσταση σειρών
    
    # Εκτιμώμενα διαστήματα (θα ρυθμιστούν μετά τη δοκιμή)
    digit_spacing = 3.5 
    points_offset = 60 # Πόσο δεξιά είναι τα σημεία 1-X-2

    for combo in combos:
        pdf.add_page()
        pdf.set_font("Courier", style='B', size=10) # Courier για σταθερό πλάτος
        
        for i, match in enumerate(combo):
            current_y = start_y + (i * row_height)
            
            # Εκτύπωση Κωδικού (π.χ. 123)
            code = str(match['Κ']).zfill(3)
            for j, digit in enumerate(code):
                pdf.text(start_x + (j * digit_spacing), current_y, "X")
            
            # Προσωρινή τοποθέτηση σημείου (θα το φτιάξουμε μόλις μετρήσεις)
            pdf.text(start_x + points_offset, current_y, "X")

    return pdf.output(dest='S').encode('latin-1')

st.title("🏆 BigBet Printer Pro")

# --- ΕΝΟΤΗΤΑ ΕΙΣΑΓΩΓΗΣ ---
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

u_input = st.text_input("📍 ΚΩΔΙΚΟΣ", key="manual", max_chars=3)
if len(u_input) == 3 and u_input.isdigit():
    if not any(x['Κ'] == u_input for x in st.session_state.my_bet):
        st.session_state.my_bet.append({"Κ": u_input, "Σ": "1"})
        st.rerun()

# --- ΤΥΧΑΙΑ ΣΥΜΠΛΗΡΩΣΗ ---
if st.session_state.my_bet:
    st.divider()
    st.multiselect("🎯 Φίλτρο Τυχαίων Σημείων:", st.session_state.options, key="filter_points")
    st.button("🎲 ΤΥΧΑΙΑ ΣΥΜΠΛΗΡΩΣΗ ΑΓΩΝΩΝ", on_click=randomize_points, use_container_width=True)

# --- ΛΙΣΤΑ ΑΓΩΝΩΝ ---
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
        
        # ΚΟΥΜΠΙ PDF
        pdf_bytes = create_pdf(st.session_state.last_random_combos)
        st.download_button(
            label="🖨️ ΚΑΤΕΒΑΣΜΑ PDF ΓΙΑ ΕΚΤΥΠΩΣΗ",
            data=pdf_bytes,
            file_name="bet_print.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    with st.expander("🔍 Προβολή Πλήρους Ανάπτυξης"):
        for idx, combo in enumerate(all_combos):
            txt = " | ".join([f"{c['Κ']}({c['Σ']})" for c in combo])
            st.markdown(f'<div class="column-box">Στήλη {idx+1}: {txt}</div>', unsafe_allow_html=True)

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ"):
        st.session_state.my_bet = []
        st.session_state.last_random_combos = []
        st.rerun()
