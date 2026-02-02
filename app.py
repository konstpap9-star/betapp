import streamlit as st
import math
import random
from itertools import combinations
import streamlit.components.v1 as components

st.set_page_config(page_title="BigBet Boca Edition", layout="wide")

# --- CSS ΓΙΑ ΦΟΝΤΟ BOCA & ΕΥΔΙΑΚΡΙΤΑ ΣΤΟΙΧΕΙΑ ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                    url("https://images.unsplash.com/photo-1540741272439-58b2011b952a?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Λευκό ημιδιαφανές πλαίσιο για να φαίνονται τα γράμματα */
    .stMarkdown, .stSelectbox, .stNumberInput, .stButton, .stMetric, .stTextInput {
        background-color: rgba(255, 255, 255, 0.9) !important;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
    }

    div.stTextInput > div > div > input {
        font-size: 25px !important; text-align: center !important; font-weight: bold !important; color: #000 !important;
    }

    .total-matches-label {
        font-size: 30px !important; font-weight: bold !important; color: #0000FF !important;
        text-align: center; margin: 15px 0px; padding: 20px;
        background-color: #FFD700 !important; border: 4px solid #DAA520; border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    
    h1, h2, h3 { color: #FFD700 !important; text-shadow: 2px 2px 4px #000; }
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

st.title("🏆 BigBet Pro: La Bombonera Edition")

# --- 1. ΕΙΣΑΓΩΓΗ ---
current_key = f"in_{st.session_state.input_counter}"
user_input = st.text_input("ΕΙΣΑΓΩΓΗ ΚΩΔΙΚΟΥ", key=current_key, max_chars=3)

# --- 2. ΧΡΥΣΟΣ ΜΕΤΡΗΤΗΣ ---
num_matches = len(st.session_state.my_bet)
st.markdown(f'<div class="total-matches-label">ΣΥΝΟΛΟ ΑΓΩΝΩΝ: {num_matches}</div>', unsafe_allow_html=True)

if len(user_input) == 3 and user_input.isdigit():
    st.session_state.my_bet.append({"Κ": user_input, "Σ": "1"})
    st.session_state.input_counter += 1
    st.rerun()

# --- 3. ΔΙΑΧΕΙΡΙΣΗ & ΑΝΑΠΤΥΞΗ ---
if st.session_state.my_bet:
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        st.subheader("📋 Λίστα Αγώνων")
        m_opts = ["1", "X", "2", "G/G", "N/G", "Over 2.5", "Under 2.5", "1X", "X2"]
        for i in range(len(st.session_state.my_bet)-1, -1, -1):
            item = st.session_state.my_bet[i]
            c1, c2, c3 = st.columns([1, 1.5, 0.6])
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
            mode = st.radio("Τρόπος:", ["Όλες", "Τυχαίες"], horizontal=True)
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
                    st.warning("⚠️ Πολλές στήλες. Βάλε 'Τυχαίες'.")

    if st.button("Καθαρισμός Όλων 🗑️"):
        st.session_state.my_bet = []
        st.rerun()
