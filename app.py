
import streamlit as st
import itertools

# --- ΚΩΔΙΚΟΣ ΕΙΣΟΔΟΥ ---
PASSWORD = "1234" 

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 Είσοδος")
    user_pw = st.text_input("Βάλε τον κωδικό σου", type="password")
    if st.button("Είσοδος"):
        if user_pw == PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Λάθος κωδικός!")
    st.stop()

# --- ΚΥΡΙΩΣ ΕΦΑΡΜΟΓΗ ---
st.title("⚽ Bet Analyzer")

# 1. Εισαγωγή αγώνων
txt = st.text_area("Γράψε τους αγώνες (έναν σε κάθε γραμμή)", "Αγώνας 1\nΑγώνας 2\nΑγώνας 3\nΑγώνας 4")
matches = [line.strip() for line in txt.split('\n') if line.strip()]

# 2. Επιλογή Συστήματος
if len(matches) > 1:
    k = st.number_input(f"Τι σύστημα θέλεις; (Από 1 έως {len(matches)})", 1, len(matches), 3)
    
    if st.button("Υπολόγισε Στήλες"):
        combos = list(itertools.combinations(matches, k))
        st.success(f"Βρέθηκαν {len(combos)} συνδυασμοί!")
        
        for i, c in enumerate(combos, 1):
            st.write(f"**Στήλη {i}:** {' + '.join(c)}")
