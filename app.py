import streamlit as st
import math
import random
from itertools import combinations
import streamlit.components.v1 as components

# Ρυθμίσεις σελίδας
st.set_page_config(page_title="BigBet Pro Stable", layout="wide")

# --- CSS ΓΙΑ ΓΑΛΑΖΙΟ ΦΟΝΤΟ & ΣΤΑΘΕΡΟΤΗΤΑ ---
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    div[data-testid="stVerticalBlock"] > div {
        background-color: #FFFFFF; border-radius: 15px; padding: 15px; box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    }
    div.stTextInput > div > div > input {
        font-size: 28px !important; text-align: center !important; font-weight: bold !important; 
        color: #0D47A1 !important; background-color: #FFFFFF !important; border: 3px solid #1976D2 !important; height: 60px !important;
    }
    .total-matches-label {
        font-size: 32px !important; font-weight: 900 !important; color: #0D47A1 !important; 
        text-align: center; margin: 15px 0px; padding: 20px;
        background-color: #FFD700 !important; border: 3px solid #DAA520; border-radius: 15px;
    }
    .stText { background-color: #F8F9FA; padding: 10px; border-radius: 8px; color: #1A1A1A !important; font-weight: bold; border-left: 6px solid #FFD700; }
    </style>
    """, unsafe_allow_html=True)

# --- JAVASCRIPT ΓΙΑ AUTO-ENTER (Πιο σταθερό) ---
components.html(
    """
    <script>
    function setup() {
        const doc = window.parent.document;
        doc.addEventListener('keyup', function(e) {
            const activeInput = doc.activeElement;
            if (activeInput && activeInput.tagName === 'INPUT' && activeInput.value.length === 3) {
                activeInput.dispatchEvent(new KeyboardEvent('keydown', {'key': 'Enter', 'bubbles': true}));
                activeInput.dispatchEvent(new Event('change', {'bubbles': true}));
            }
        });
    }
    setTimeout(setup, 1000);
    </script>
    """, height=0,
)

# Αρχικοποίηση Session State
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

st.title("🏆 BigBet Pro Tool")

# --- 1. ΕΙΣΑΓΩΓΗ ---
current_key = f"in_{st.session_state.input_counter}"
user_input = st.text_input("ΕΙΣΑΓΩΓΗ 3ΨΗΦΙΟΥ", key=current_key, max_chars=3)

# --- 2. ΜΕΤΡΗΤΗΣ ---
num_matches = len(st.session_state.my_bet)
st.markdown(f'<div class="total-matches-label">ΣΥΝΟΛΟ ΑΓΩΝΩΝ: {num_matches}</div>', unsafe_allow_html=True)

if len(user_input) == 3 and user_input.isdigit():
    st.session_state.my_bet.append({"Κ": user_input, "Σ": "1"})
    st.session_state.input_counter += 1
    st.rerun()

# --- 3. ΔΙΑΧΕΙΡΙΣΗ ---
if st.session_state.my_bet:
    col_l, col_r =
