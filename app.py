import streamlit as st
import math
import random
from itertools import combinations
import streamlit.components.v1 as components

st.set_page_config(page_title="BigBet Sky Edition", layout="wide")

# --- CSS ΓΙΑ ΑΝΟΙΧΤΟ ΓΑΛΑΖΙΟ ΦΟΝΤΟ & ΕΥΔΙΑΚΡΙΤΑ ΣΤΟΙΧΕΙΑ ---
st.markdown("""
    <style>
    /* Φόντο σε ανοιχτό γαλάζιο */
    .stApp {
        background-color: #E3F2FD;
    }
    
    /* Λευκές κάρτες για τα περιεχόμενα */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #FFFFFF;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    }

    /* Πλαίσιο εισαγωγής κωδικού */
    div.stTextInput > div > div > input {
        font-size: 28px !important; 
        text-align: center !important; 
        font-weight: bold !important; 
        color: #0D47A1 !important; /* Σκούρο μπλε γράμματα */
        background-color: #FFFFFF !important;
        border: 3px solid #1976D2 !important;
        height: 60px !important;
    }

    /* Ο ΧΡΥΣΟΣ ΜΕΤΡΗΤΗΣ (ΣΥΝΟΛΟ ΑΓΩΝΩΝ) */
    .total-matches-label {
        font-size: 32px !important; 
        font-weight: 900 !important; 
        color: #0D47A1
