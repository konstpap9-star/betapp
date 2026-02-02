import streamlit as st
import math
import random
from itertools import combinations

# 1. Βασικές Ρυθμίσεις
st.set_page_config(page_title="BigBet Pro Auto-Fill", layout="wide")

# 2. CSS για Λευκά Πλαίσια και Γαλάζιο Φόντο
st.markdown("""
    <style>
    .stApp { background-color: #E3F2FD; }
    
    div[data-testid="stVerticalBlock"] > div {
        background-color: #FFFFFF !important; 
        border-radius: 12px; 
        padding: 15px; 
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }

    div.stTextInput > div > div > input {
        font-size: 20px !important; text-align: center; font-weight: bold;
        color: #0D47A1; border: 2px solid #1976D2; height: 45px;
    }

    .total-matches-label {
        font-size: 30px !important; font-weight: bold; color: #0D47A1;
        text-align: center; padding: 15px; background-color: #FFD700;
        border-radius: 12px; border: 2px solid #DAA520; margin: 10px 0;
    }
    
    .stButton > button {
        width: 100%;
        background-color: #1976D2 !important;
        color: white !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Αρχικοποίηση Μνήμης
if 'my_bet' not in st.session_state: st.session_state.my_bet = []
if 'input_counter' not in st.session_state: st.session_state.input_counter = 0

st.title("🏆 BigBet Pro Tool")

# --- ΝΕΟ: ΜΑΖΙΚΗ ΕΙΣΑΓΩΓΗ (ΑΠΟ - ΕΩΣ) ---
st.subheader("🔗 Μαζική Εισαγωγή Κωδικών")
c_start, c_end, c_btn = st.columns([1, 1, 1.2])

with c_start:
    start_num = st.text_input("ΑΠΟ", key="start_range", max_chars=3, placeholder="π.χ. 100")
with c_end:
    end_num = st.text_input("ΕΩΣ", key="end_range", max_chars=3, placeholder="π.χ. 115")
with c_btn:
    st.write(" ") # Για στοίχιση
    if st.button("Προσθήκη Εύρους ➕"):
        if start_num.isdigit() and end_num.isdigit():
            s = int(start_num)
            e = int(end_num)
            if s <= e:
                for code in range(s, e + 1):
                    # Μετατροπή σε string 3 ψηφίων (π.χ. 001, 010, 100)
                    formatted_code = str(code).zfill(3)
                    # Έλεγχος αν υπάρχει ήδη για να μην μπαίνει διπλός
                    if not any(item['Κ'] == formatted_code for item in st.session_state.my_bet):
                        st.session_state.my_bet.append({"Κ": formatted_code, "Σ": "1"})
                st.rerun()
            else:
                st.error("Το 'ΑΠΟ' πρέπει να είναι μικρότερο.")

st.markdown("---")

# --- ΚΛΑΣΙΚΗ ΕΙΣΑΓΩΓΗ ---
st.subheader("📍 Μεμονωμένη Εισαγωγή")
current_key = f"in_{st.session_state.input_counter}"
user_input = st.text_input("ΚΩΔΙΚΟΣ", key=current_key, max_chars=3)

# Μετρητής Αγώνων
st.markdown(f'<div class="total-matches-label">ΣΥΝΟΛΟ ΑΓΩΝΩΝ: {len(st.session_state.my_bet)}</div>', unsafe_allow_html=True)

if len(user_input) == 3 and user_input.isdigit():
    st.session_state.my_bet.append({"Κ": user_input, "Σ": "1"})
    st.session_state.input_counter += 1
    st.rerun()

# 5. Προβολή και Ανάπτυξη
if st.session_state.my_bet:
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("📋 Λίστα Αγώνων")
        opts = ["1", "X", "2", "G/G", "N/G", "Over 2.5", "Under 2.5", "1X", "X2"]
        for i in range(len(st.session_state.my_bet)-1, -1, -1):
            item = st.session_state.my_bet[i]
            c1, c2, c3 = st.columns([1, 2, 0.8])
            with c1: st.write(f"**{item['Κ']}**")
            with c2: 
                st.session_state.my_bet[i]['Σ'] = st.selectbox(
                    f"sel_{i}", opts, key=f"s_{i}", 
                    index=opts.index(item['Σ']), label_visibility="collapsed"
                )
            with c3:
                if st.button("❌", key=f"del_{i}"):
                    st.session_state.my_bet.pop(i)
                    st.rerun()

    with col_r:
        st.subheader("🔢 Ανάπτυξη")
        n = len(st.session_state.my_bet)
        k = st.number_input("Ζητούμενα:", 1, max(1, n), min(n, 3))
        total = math.comb(n, k)
        st.metric("Σύνολο Στηλών", f"{total:,}")
        
        if total > 0:
            if total <= 500:
                if st.checkbox("Εμφάνιση Όλων"):
                    for combo in combinations(st.session_state.my_bet, k):
                        st.text(" · ".join([f"{x['Κ']}[{x['Σ']}]" for x in combo]))
            else:
                num_rand = st.number_input("Τυχαίες στήλες:", 1, total, 10)
                if st.button("Δείξε Τυχαίες ✨"):
                    all_combos = list(combinations(st.session_state.my_bet, k))
                    for c in random.sample(all_combos, num_rand):
                        st.text(" · ".join([f"{x['Κ']}[{x['Σ']}]" for x in c]))

    if st.button("🗑️ ΚΑΘΑΡΙΣΜΟΣ ΟΛΩΝ"):
        st.session_state.my_bet = []
        st.session_state.input_counter = 0
        st.rerun()
