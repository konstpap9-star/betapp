def randomize_all():
    # Παίρνει τα επιλεγμένα σημεία ή όλα
    pool = st.session_state.allowed_points if st.session_state.get('allowed_points') else st.session_state.options
    for i in range(len(st.session_state.my_bet)):
        new_val = random.choice(pool)
        # ΕΝΗΜΕΡΩΣΗ 1: Η κεντρική λίστα (για την ανάπτυξη στηλών)
        st.session_state.my_bet[i]['Σ'] = new_val
        # ΕΝΗΜΕΡΩΣΗ 2: Το key του selectbox (για να αλλάξει στην οθόνη)
        st.session_state[f"sel_{i}"] = new_val
