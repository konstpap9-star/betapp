import streamlit as st
import math

# 1. Η ΝΕΑ ΛΙΣΤΑ ΣΗΜΕΙΩΝ ΜΕ ΣΥΝΤΟΜΟΓΡΑΦΙΕΣ (Γ & Φ)
FINAL_OPTIONS = [
    "1", "X", "2", 
    "1X", "X2", "12",
    "G/G", "N/G", 
    "Over 1.5", "Under 1.5",
    "Over 2.5", "Under 2.5", 
    "Over 3.5", "Under 3.5",
    # ΓΗΠΕΔΟΥΧΟΣ & ΦΙΛΟΞΕΝΟΥΜΕΝΟΣ ΜΑΖΙ (OVER)
    "Γ Over 0.5", "Φ Over 0.5",
    "Γ Over 1.5", "Φ Over 1.5",
    "Γ Over 2.5", "Φ Over 2.5",
    "Γ Over 3.5", "Φ Over 3.5",
    # ΓΗΠΕΔΟΥΧΟΣ & ΦΙΛΟΞΕΝΟΥΜΕΝΟΣ ΜΑΖΙ (UNDER)
    "Γ Under 0.5", "Φ Under 0.5",
    "Γ Under 1.5", "Φ Under 1.5",
    "Γ Under 2.5", "Φ Under 2.5",
    "Γ Under 3.5", "Φ Under 3.5"
]

st.set_page_config(page_title="BigBet Precise Mobile", layout="wide")

# 2. CSS για Mobile Optimization
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
    /* Selectbox - Κίτρινο και Compact */
    div[data-baseweb="select"] > div {
        background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important;
        min-height: 40px !important; font-size: 15px !important;
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

u_input =
