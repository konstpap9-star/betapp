import streamlit as st
import math

# 1. ΟΡΙΣΤΙΚΗ ΛΙΣΤΑ - ΔΕΝ ΑΛΛΑΖΕΙ ΠΟΤΕ
if 'options' not in st.session_state:
    st.session_state.options = [
        "1", "X", "2", "1X", "X2", "12", "G/G", "N/G", 
        "Over 1.5", "Under 1.5", "Over 2.5", "Under 2.5", "Over 3.5", "Under 3.5",
        "Γ Over 0.5", "Φ Over 0.5", "Γ Over 1.5", "Φ Over 1.5", 
        "Γ Over 2.5", "Φ Over 2.5", "Γ Over 3.5", "Φ Over 3.5",
        "Γ Under 0.5", "Φ Under 0.5", "Γ Under 1.5", "Φ Under 1.5", 
        "Γ Under 2.5", "Φ Under 2.5", "Γ Under 3.5", "Φ Under 3.5"
    ]

st.set_page_config(page_title="BigBet Stable", layout="wide")

# 2. ΑΠΛΟ CSS (Μόνο τα απαραίτητα για να μην κολλάει)
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    .block-container { padding-top: 2rem; }
    input { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; }
    div[data-baseweb="select"] > div { background-color: #FFF9C4 !important; border: 1px solid #FBC02D !important; }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

if 'my_bet' not in st.session_state: st.session_state.my_bet = []

st.title("🏆 BigBet Printer")

# --- ΕΙΣΑΓΩΓΗ ---
with st.expander("➕ Προσθήκη Αγώνων", expanded=True):
    c1, c2 = st.columns(2)
    with c1: s_range = st.text_input("ΑΠΟ", key="s", max_chars=3)
    with c2: e_range = st.text_input("ΕΩΣ", key="e", max_chars=3)
    if st.button("ΠΡΟΣΘΗΚΗ ΕΥΡΟΥΣ"):
        if s_range.isdigit() and e_range.isdigit():
            for code in range(int(s_range), int(e_range) + 1):
                fmt = str(code).zfill(3)
                if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
                    st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})
            st.rerun()

    u_input = st.text_input("📍 ΜΕΜΟΝΩΜΕΝΟΣ ΚΩΔΙΚΟΣ", key="manual", max_chars=3)
    if len(u_input) == 3 and u_input.isdigit():
        st.session_state.my_bet.append({"Κ": u_input, "Σ": "1"})
        st.rerun()

# --- ΛΙΣΤΑ ---
st.subheader(f"Σύνολο: {len(st.session_state.my_bet)}")

for i, item in enumerate(reversed(st.session_state.my_bet)):
    idx = len(st.session_state.my_bet) - 1 - i
    col_k, col_s, col_d = st.columns([0.5, 2, 0.5])
    
    with col_k:
        st.write(f"**{item['Κ']}**")
    with col_s:
        # Χρήση του session_state για τη λίστα
        choice = st.selectbox(
            "Σημείο", 
            st.session_state.options, 
            index=st.session_state.options.index(item['Σ']) if item['Σ'] in st.session_state.options else 0,
            key=f"sel_{idx}",
            label_visibility="collapsed"
        )
        st.session_state.my_bet[idx]['Σ'] = choice
    with col_d:
        if st.button("✕", key=f"del_{idx}"):
            st.session_state.my_bet.pop(idx)
            st.rerun()

# --- ΣΥΣΤΗΜΑ ---
if st.session_state.my_bet:
    st.divider()
    n = len(st.session_state.my_bet)
    k = st.number_input("Ζητούμενα", 1, n, min(n, 3) if n>=3 else 1)
    st.write(f"Στήλες: **{math.comb(n, k)}**")
    
    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ ΟΛΩΝ"):
        st.session_state.my_bet = []
        st.rerun()
