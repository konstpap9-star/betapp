# 1. ΝΕΑ ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΤΥΧΑΙΑ ΣΥΜΠΛΗΡΩΣΗ ΜΕ ΦΙΛΤΡΟ
def randomize_selections():
    # Αν ο χρήστης έχει επιλέξει συγκεκριμένα σημεία στο multiselect, χρησιμοποιούμε αυτά.
    # Αλλιώς, χρησιμοποιούμε όλη τη λίστα options.
    pool = st.session_state.allowed_points if st.session_state.allowed_points else st.session_state.options
    
    for i in range(len(st.session_state.my_bet)):
        rnd = random.choice(pool)
        st.session_state[f"sel_{i}"] = rnd
        st.session_state.my_bet[i]['Σ'] = rnd

# --- ΕΙΣΑΓΩΓΗ ---
with st.container():
    c1, c2 = st.columns(2)
    with c1: s_range = st.text_input("ΑΠΟ", key="s", max_chars=3)
    with c2: e_range = st.text_input("ΕΩΣ", key="e", max_chars=3)
    
    # ΝΕΟ ΠΕΔΙΟ: Επιλογή επιτρεπόμενων σημείων για την τύχη
    allowed = st.multiselect(
        "🎯 Επιλογή σημείων για την Τυχαία Παραγωγή (π.χ. μόνο 1, Χ, 2)",
        options=st.session_state.options,
        key="allowed_points",
        help="Αν το αφήσετε κενό, η τυχαία επιλογή θα γίνει από όλα τα διαθέσιμα σημεία."
    )

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("ΠΡΟΣΘΗΚΗ ΕΥΡΟΥΣ ➕", use_container_width=True):
            if s_range.isdigit() and e_range.isdigit():
                for code in range(int(s_range), int(e_range) + 1):
                    fmt = str(code).zfill(3)
                    if not any(x['Κ'] == fmt for x in st.session_state.my_bet):
                        st.session_state.my_bet.append({"Κ": fmt, "Σ": "1"})
                st.rerun()
    with col_b:
        if st.session_state.my_bet:
            st.button("🎲 ΤΥΧΑΙΑ ΣΗΜΕΙΑ (Στα επιλεγμένα)", on_click=randomize_selections, use_container_width=True)

    u_input = st.text_input("📍 ΚΩΔΙΚΟΣ", key="manual", max_chars=3)
    if len(u_input) == 3 and u_input.isdigit():
        if not any(x['Κ'] == u_input for x in st.session_state.my_bet):
            st.session_state.my_bet.append({"Κ": u_input, "Σ": "1"})
            st.rerun()
