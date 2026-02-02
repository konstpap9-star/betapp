import streamlit as st
import math
import random
from itertools import combinations
import streamlit.components.v1 as components

# Ρυθμίσεις σελίδας
st.set_page_config(page_title="BigBet White Edition", layout="wide")

# --- CSS ΓΙΑ ΓΑΛΑΖΙΟ ΦΟΝΤΟ ΚΑΙ ΛΕΥΚΑ ΠΛΑΙΣΙΑ ---
st.markdown("""
    <style>
    /* Φόντο σελίδας ανοιχτό γαλάζιο */
    .stApp { 
        background-color: #E3F2FD; 
    }
    
    /* ΟΛΑ ΤΑ ΠΛΑΙΣΙΑ ΛΕΥΚΑ */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #FFFFFF !important; 
        border-radius: 15px; 
        padding: 15px; 
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 15px;
    }
    
    /* Λευκό φόντο και στα εσωτερικά widgets */
    .stSelectbox, .stNumberInput, .stTextInput, .stMetric {
        background-color: #FFFFFF !important;
    }

    /* Πλαίσιο εισαγωγής κωδικού */
    div.stTextInput > div > div > input {
        font-size: 28px !important; text-align: center !important; font-weight: bold !important; 
        color: #0D47A1 !important; background-color: #FFFFFF !important; 
        border: 3px solid #1976D2 !important; height: 60px !important;
    }

    /* Ο ΧΡΥΣΟΣ ΜΕΤΡΗΤΗΣ */
    .total-matches-label {
        font-size: 32px !important; font-weight: 900 !important; color: #0D47A1 !important; 
        text-align: center; margin: 15px 0px; padding: 20px;
        background-color: #FFD700 !important; border: 3px solid #DAA520; border-radius: 15px;
    }

    /* Λευκό φόντο στις αναλυτικές στήλες */
    .stText { 
        background-color: #FFFFFF !important; 
        padding: 10px; border-radius: 8px; 
        color: #1A1A1A !important; font-weight: bold; 
        border-left: 6px solid #FFD700; 
        border: 1px solid #E0E0E0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- JAVASCRIPT ΓΙΑ AUTO-ENTER ---
components.html(
    """
    <script>
    function setup() {
        const doc = window.parent.document;
        doc.addEventListener('keyup', function(e) {
            const activeInput = doc.activeElement;
            if (activeInput && activeInput.tagName === 'INPUT' && activeInput.value.length === 3
