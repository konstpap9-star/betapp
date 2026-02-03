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

# 2. ΠΛΗΡΕΣ CSS ΓΙΑ ΧΡΩΜΑΤΑ ΚΑΙ MOBILE FIX
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    /* Κίτρινα πλαίσια εισαγωγής */
    input { background-color: #FFF9C4 !important; border: 2px solid #FBC02D !important; font-weight: bold !important; color: black !important; }
    /* Κίτρινα πλαίσια selectbox */
    div[data-baseweb="select"] > div { background-color: #FFF9C4 !important; border: 2px solid #FBC02D !important; }
    /* Στυλ για τις τυχαίες στήλες (Κίτρινο κουτί) */
    .random-box { background-color: #FFF9C4; padding: 12px; border-radius: 8px; border-left: 6px solid #FBC02D; color: #0D47A1; font-weight: bold; margin-bottom: 8px; font-size: 16px; }
    /* Στυλ για την πλήρη ανάπτυξη */
    .column-box { background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 5px solid #0D47A1; margin-bottom: 5px; font-family: monospace; }
    /* Διόρθωση για το selectbox σε mobile */
    div[data-baseweb="select"] input { inputmode: none !important; caret-color: transparent !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. ΣΥΝΑΡΤΗΣΗ ΔΗΜΙΟΥΡΓΙΑΣ PDF (ΕΚΤΥΠΩΣΗ)
def create_pdf(combos):
    # Landscape προσανατολισμός (Οριζόντιο δελτίο)
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(
