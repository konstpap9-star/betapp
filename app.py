import streamlit as st
import math

# 1. Η ΑΚΡΙΒΗΣ ΛΙΣΤΑ ΣΗΜΕΙΩΝ ΠΟΥ ΖΗΤΗΣΕΣ
FINAL_OPTIONS = [
    "1", "X", "2", 
    "1X", "X2", "12",
    "G/G", "N/G", 
    "Over 1.5", "Under 1.5",
    "Over 2.5", "Under 2.5", 
    "Over 3.5", "Under 3.5",
    "Γηπεδούχος Over 0.5", "Γηπεδούχος Over 1.5", "Γηπεδούχος Over 2.5", "Γηπεδούχος Over 3.5",
    "Γηπεδούχος Under 0.5", "Γηπεδούχος Under 1.5", "Γηπεδούχος Under 2.5", "Γηπεδούχος Under 3.5",
    "Φιλοξενούμενος Over 0.5", "Φιλοξενούμενος Over 1.5", "Φιλοξενούμενος Over 2.5", "Φιλοξενούμενος Over 3.5",
    "Φιλοξενούμενος Under 0.5", "Φιλοξενούμενος Under 1.5", "Φιλοξενούμενος Under 2.5", "Φιλοξενούμενος Under 3.5"
]

st.set_page_config(page_title="BigBet Precise Markets", layout="wide")

# 2. CSS για Mobile & Compact Εμφάνιση
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    .white-container {
        background-color: #FFFFFF; padding: 10px; border-radius: 10px;
        margin-bottom: 5px; border: 1px solid #BBDEFB;
    }
    input {
        background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important;
        font-weight: bold !important; height: 40px !important;
    }
    /* Selectbox - Κίτρινο και ευανάγνωστο */
    div[data-baseweb="select"] > div {
        background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important;
        min-height: 40px !important; font-size: 13px !important;
    }
    div[data-baseweb="select"] div[role="button"] + div { display: none !important; }
    
    .counter-box {
        background-color: #FFD700; color: #0D47A1; font-size: 20px;
        font-weight: bold; text-align: center; padding: 10px; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

st.title("🏆 BigBet Printer Pro")

# --- ΕΙΣΑΓΩΓΗ ---
st.markdown('<div class="white-container">', unsafe_allow_html=True)
c_in1, c_in2, c_in3 = st.columns([1, 1, 1.2])
with c_in1: s_range = st.text_input("ΑΠΟ", key="start", max_chars=3, placeholder="Από")
with c_in2: e_range = st.text_input("ΕΩΣ", key="end", max_chars=3, placeholder="Έως")
with c_in3:
    st.write(" ")
    if st.button("ΠΡΟΣΘΗΚΗ"):
        if s_range.isdigit() and e_range.isdigit():
            for code in range(int(s_range), int(e_range) + 1):
                fmt = str(code).zfill(3)
                if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
                    st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})
            st.rerun()

u_input = st.text_input("📍 ΚΩΔΙΚΟΣ", key=f"in_{st.session_state.input_counter}", max_chars=3, placeholder="Κωδικός")
st.markdown('</div>', unsafe_allow_html=True)

if len(u_input) == 3 and u_input.isdigit():
    st.session_state.my_bet.append({"Κ": u_input, "Σ": "1"})
    st.session_state.input_counter += 1
    st.rerun()

st.markdown(f'<div class="counter-box">ΣΥΝΟΛΟ ΑΓΩΝΩΝ: {len(st.session_state.my_bet)}</div>', unsafe_allow_html=True)

# --- ΛΙΣΤΑ ΑΓΩΝΩΝ ---
if st.session_state.my_bet:
    st.markdown('<div class="white-container">', unsafe_allow_html=True)
    
    for i in range(len(st.session_state.my_bet)-1, -1, -1):
        item = st.session_state.my_bet[i]
        # Στήλες: Κωδικός (0.5), Σημείο (2.2), Διαγραφή (0.4)
        cl1, cl2, cl3 = st.columns([0.5, 2.2, 0.4])
        
        with cl1:
            st.write(f"**{item['Κ']}**")
            
        with cl2:
            choice = st.selectbox(
                f"sel_{i}", 
                FINAL_OPTIONS, 
                index=FINAL_OPTIONS.index(item['Σ']) if item['Σ'] in FINAL_OPTIONS else 0,
                key=f"sb_{item['Κ']}_{i}",
                label_visibility="collapsed"
            )
            st.session_state.my_bet[i]['Σ'] = choice
            
        with cl3:
            if st.button("✕", key=f"del_{i}"):
                st.session_state.my_bet.pop(i)
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ΣΥΣΤΗΜΑ ---
    st.markdown('<div class="white-container">', unsafe_allow_html=True)
    n = len(st.session_state.my_bet)
    k = st.number_input("Ζητούμενα:", 1, max(1, n), min(n, 3) if n>=3 else 1)
    st.write(f"Στήλες: **{math.comb(n, k):,}**")
    if st.button("🖨️ ΕΚΤΥΠΩΣΗ"):
        st.success("Έτοιμο!")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ"):
        st.session_state.my_bet = []
        st.rerun()
