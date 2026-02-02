import streamlit as st
import math
import random
from itertools import combinations
import streamlit.components.v1 as components

st.set_page_config(page_title="BigBet Pro Clean", layout="wide")

# --- CSS ΓΙΑ ΜΕΓΙΣΤΗ ΕΥΚΡΙΝΕΙΑ (High Contrast) ---
st.markdown("""
    <style>
    /* Φόντο σε βαθύ σκοτεινό μπλε-γκρι */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Κάρτες για τα περιεχόμενα με απαλό περίγραμμα */
    div[data-testid="stVerticalBlock"] > div {
        background-color: #1A1C24;
        border-radius: 12px;
        padding: 5px;
    }

    /* Πλαίσιο εισαγωγής κωδικού */
    div.stTextInput > div > div > input {
        font-size: 28px !important; 
        text-align: center !important; 
        font-weight: bold !important; 
        color: #FFFFFF !important;
        background-color: #262730 !important;
        border: 2px solid #FFD700 !important;
        height: 60px !important;
    }

    /* Ο ΧΡΥΣΟΣ ΜΕΤΡΗΤΗΣ (ΣΥΝΟΛΟ ΑΓΩΝΩΝ) */
    .total-matches-label {
        font-size: 32px !important; 
        font-weight: 900 !important; 
        color: #001F3F !important; /* Πολύ σκούρο μπλε για αντίθεση στο χρυσό */
        text-align: center; 
        margin: 15px 0px; 
        padding: 20px;
        background-color: #FFD700 !important; 
        border: 2px solid #FFFFFF;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    }
    
    /* Τίτλοι και κείμενα */
    h1, h2, h3, p, span, label {
        color: #FFFFFF !important;
    }

    /* Στυλ για τις στήλες στην ανάλυση */
    .stText {
        background-color: #262730;
        padding: 8px;
        border-radius: 5px;
        color: #FFD700 !important;
        font-family: monospace;
        font-size: 14px;
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
            if (activeInput.tagName === 'INPUT' && activeInput.value.length === 3) {
                activeInput.dispatchEvent(new KeyboardEvent('keydown', {'key': 'Enter', 'bubbles': true}));
                activeInput.dispatchEvent(new Event('change', {'bubbles': true}));
            }
        });
    }
    setTimeout(setup, 1000);
    </script>
    """, height=0,
)

if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

st.title("🏆 BigBet Pro Tool")

# --- 1. ΕΙΣΑΓΩΓΗ ---
current_key = f"in_{st.session_state.input_counter}"
user_input = st.text_input("ΕΙΣΑΓΩΓΗ 3ΨΗΦΙΟΥ", key=current_key, max_chars=3)

# --- 2. ΧΡΥΣΟΣ ΜΕΤΡΗΤΗΣ ---
num_matches = len(st.session_state.my_bet)
st.markdown(f'<div class="total-matches-label">ΣΥΝΟΛΟ ΑΓΩΝΩΝ: {num_matches}</div>', unsafe_allow_html=True)

if len(user_input) == 3 and user_input.isdigit():
    st.session_state.my_bet.append({"Κ": user_input, "Σ": "1"})
    st.session_state.input_counter += 1
    st.rerun()

# --- 3. ΔΙΑΧΕΙΡΙΣΗ & ΑΝΑΠΤΥΞΗ ---
if st.session_state.my_bet:
    st.markdown("---")
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        st.subheader("📋 Λίστα Αγώνων")
        m_opts = ["1", "X", "2", "G/G", "N/G", "Over 2.5", "Under 2.5", "1X", "X2"]
        for i in range(len(st.session_state.my_bet)-1, -1, -1):
            item = st.session_state.my_bet[i]
            c1, c2, c3 = st.columns([1, 1.8, 0.6])
            with c1: st.write(f"**{item['Κ']}**")
            with c2: st.session_state.my_bet[i]['Σ'] = st.selectbox(f"s_{i}", m_opts, key=f"sel_{i}", index=m_opts.index(item['Σ']), label_visibility="collapsed")
            with c3:
                if st.button("❌", key=f"d_{i}"):
                    st.session_state.my_bet.pop(i)
                    st.rerun()

    with col_r:
        st.subheader("🔢 Σύστημα")
        n = len(st.session_state.my_bet)
        k = st.number_input("Ζητούμενα:", 1, max(1, n), min(n, 3))
        
        total = math.comb(n, k)
        st.metric("Συνολικές Στήλες", f"{total:,}")
        
        if total > 0:
            mode = st.radio("Εμφάνιση:", ["Όλες", "Τυχαίες"], horizontal=True)
            if mode == "Τυχαίες":
                num = st.number_input("Πόσες στήλες;", 1, total, min(total, 5))
                if st.button("Παραγωγή ✨"):
                    all_c = list(combinations(st.session_state.my_bet, k))
                    for idx, c in enumerate(random.sample(all_c, num), 1):
                        st.text(f"{idx}. {' · '.join([f'{x['Κ']}[{x['Σ']}]' for x in c])}")
            else:
                if total <= 1000:
                    if st.checkbox("Εμφάνιση Αναλυτικά"):
                        for idx, c in enumerate(combinations(st.session_state.my_bet, k), 1):
                            st.text(f"{idx}. {' · '.join([f'{x['Κ']}[{x['Σ']}]' for x in c])}")
                else:
                    st.warning("⚠️ Πολλές στήλες. Χρησιμοποίησε το 'Τυχαίες'.")

    if st.button("Καθαρισμός Όλων 🗑️"):
        st.session_state.my_bet = []
        st.rerun()
