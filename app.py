import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="BigBet Tool", layout="wide")

# --- CSS ΣΤΥΛ ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #f0f2f6;}
    .stRadio > div { flex-direction: row; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- ΚΕΝΤΡΙΚΟ ΜΕΝΟΥ ---
st.title("🏆 BigBet Tool")
choice = st.radio("Διάλεξε Εργαλείο:", 
                 ["Το Δελτίο μου", "Live Σκορ", "Value Bet", "Arbitrage"],
                 horizontal=True)

st.markdown("---")

if choice == "Το Δελτίο μου":
    st.subheader("📝 Γρήγορη Εισαγωγή Κωδικών")
    
    if 'my_bet' not in st.session_state:
        st.session_state.my_bet = []

    market_options = [
        "1", "X", "2", "G/G", "N/G",
        "Over 0.5", "Under 0.5", "Over 1.5", "Under 1.5",
        "Over 2.5", "Under 2.5", "Over 3.5", "Under 3.5",
        "1X", "X2", "12"
    ]

    # ΕΞΥΠΝΗ ΕΙΣΑΓΩΓΗ
    st.write("Γράψε τους κωδικούς συνεχόμενα (π.χ. 101102103):")
    raw_input = st.text_input("Εισαγωγή κωδικών:", key="bulk_input")
    
    if st.button("Προσθήκη στο Δελτίο ➕"):
        if raw_input:
            # Σπάμε το κείμενο ανά 3 χαρακτήρες
            new_codes = [raw_input[i:i+3] for i in range(0, len(raw_input), 3)]
            for c in new_codes:
                if len(c) == 3: # Προσθέτουμε μόνο αν είναι 3ψηφιος
                    st.session_state.my_bet.append({"Κωδικός": c, "Σημείο": "1", "Απόδοση": 1.80})
            st.rerun()

    # ΕΠΕΞΕΡΓΑΣΙΑ ΔΕΛΤΙΟΥ
    if st.session_state.my_bet:
        st.markdown("---")
        total_odds = 1.0
        
        for i, item in enumerate(st.session_state.my_bet):
            c1, c2, c3, c4 = st.columns([1, 2, 1, 0.5])
            with c1:
                st.session_state.my_bet[i]['Κωδικός'] = st.text_input(f"code_{i}", value=item['Κωδικός'], label_visibility="collapsed")
            with c2:
                st.session_state.my_bet[i]['Σημείο'] = st.selectbox(f"mkt_{i}", market_options, index=market_options.index(item['Σημείο']), label_visibility="collapsed")
            with c3:
                st.session_state.my_bet[i]['Απόδοση'] = st.number_input(f"odd_{i}", min_value=1.01, value=item['Απόδοση'], step=0.01, format="%.2f", label_visibility="collapsed")
            with c4:
                if st.button("❌", key=f"del_{i}"):
                    st.session_state.my_bet.pop(i)
                    st.rerun()
            total_odds *= st.session_state.my_bet[i]['Απόδοση']

        st.success(f"**Συνολική Απόδοση: {total_odds:.2f}**")
        
        col_stake, col_win = st.columns(2)
        with col_stake:
            stake = st.number_input("Ποντάρισμα (€)", min_value=0.0, value=10.0)
        with col_win:
            st.metric("Πιθανό Κέρδος", f"{stake * total_odds:.2f}€")

        if st.button("Καθαρισμός Όλων 🗑️"):
            st.session_state.my_bet = []
            st.rerun()

# Οι υπόλοιπες λειτουργίες παραμένουν ίδιες...
elif choice == "Live Σκορ":
    components.html('<iframe src="https://www.livescore.cz/widgets/scores.php?lang=el" width="100%" height="800" frameborder="0"></iframe>', height=850)
elif choice == "Value Bet":
    st.subheader("📊 Value Bet")
    od = st.number_input("Απόδοση", value=2.00)
    pr = st.number_input("Πιθανότητα %", value=50)
    if st.button("Υπολογισμός"):
        ev = (od * (pr/100)) - 1
        st.write(f"Value: {ev*100:.1f}%")
elif choice == "Arbitrage":
    st.subheader("💰 Arbitrage")
    o1 = st.number_input("Απόδοση 1", value=2.10)
    o2 = st.number_input("Απόδοση 2", value=2.10)
    if st.button("Έλεγχος"):
        arb = (1/o1) + (1/o2)
        st.write(f"Πλεονέκτημα: {((1/arb)-1)*100:.2f}%")
