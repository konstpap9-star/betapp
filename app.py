import streamlit as st
import math
import random
from itertools import combinations

# 1. Βασικές Ρυθμίσεις
st.set_page_config(page_title="BigBet Pro Compact", layout="wide")

# 2. CSS για Λευκά Πλαίσια, Γαλάζιο Φόντο και Compact Στοιχεία
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    
    /* Λευκά Πλαίσια */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #FFFFFF !important; 
        border-radius: 12px; 
        padding: 10px; 
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 8px;
    }

    /* Μικρότερα Inputs για το Από/Έως */
    .compact-input input {
        height: 35px !important;
        font-size: 16px !important;
        padding: 5px !important;
        text-align: center !important;
    }

    /* Κεντρικό Input Κωδικού */
    div.stTextInput > div > div > input {
        font-size: 24px !important; text-align: center; font-weight: bold;
        color: #0D47A1; border: 2px solid #1976D2; height: 50px;
    }

    /* Χρυσός Μετρητής */
    .total-matches-label {
        font-size: 28px !important; font-weight: bold; color: #0D47A1;
        text-align: center; padding: 12px; background-color: #FFD700;
        border-radius: 12px; border: 2px solid #DAA520; margin: 5px 0;
    }
    
    .stButton > button {
        width: 100%;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Αρχικοποίηση Μνήμης
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

st.title("🏆 BigBet Pro Tool")

# --- ΜΑΖΙΚΗ ΕΙΣΑΓΩΓΗ ΣΕ ΜΙΑ ΓΡΑΜΜΗ (Compact) ---
with st.container():
    st.write("🔗 **Μαζική Εισαγωγή**")
    # Χρησιμοποιούμε περισσότερες στήλες για να γίνουν μικρά τα πλαίσια
    c1, c2, c3, c4, c5 = st.columns([0.5, 0.8, 0.8, 1.2, 2])
    
    with c1:
        st.write(" ") # Padding
    with c2:
        start_num = st.text_input("ΑΠΟ", key="start_range", max_chars=3, label_visibility="collapsed", placeholder="Από")
    with c3:
        end_num = st.text_input("ΕΩΣ", key="end_range", max_chars=3, label_visibility="collapsed", placeholder="Έως")
    with c4:
        if st.button("Προσθήκη ➕"):
            if start_num.isdigit() and end_num.isdigit():
                s, e = int(start_num), int(end_num)
                if s <= e:
                    for code in range(s, e + 1):
                        formatted_code = str(code).zfill(3)
                        if not any(item['Κ'] == formatted_code for item in st.session_state.my_bet):
                            st.session_state.my_bet.append({"Κ": formatted_code, "Σ": "1"})
                    st.rerun()
    with c5:
        st.write(" ") # Κενό για να μείνουν αριστερά τα υπόλοιπα

st.markdown("---")

# --- ΚΛΑΣΙΚΗ ΕΙΣΑΓΩΓΗ ---
current_key = f"in_{st.session_state.input_counter}"
user_input = st.text_input("📍 ΕΙΣΑΓΩΓΗ ΚΩΔΙΚΟΥ", key=current_key, max_chars=3)

# Μετρητής Αγώνων
st.markdown(f'<div class="total-matches-label">ΣΥΝΟΛΟ ΑΓΩΝΩΝ: {len(st.session_state.my_bet)}</div>', unsafe_allow_html=True)

if len(user_input) == 3 and user_input.isdigit():
    st.session_state.my_bet.append({"Κ": user_input, "Σ": "1"})
    st.session_state.input_counter += 1
    st.rerun()

# 5. Προβολή και Ανάπτυξη
if st.session_state.my_bet:
