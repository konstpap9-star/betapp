import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="BigBet Tool", layout="wide")

# --- CSS ΓΙΑ ΕΜΦΑΝΙΣΗ ---
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

# --- 1. ΤΟ ΔΕΛΤΙΟ ΜΟΥ ---
if choice == "Το Δελτίο μου":
    st.subheader("📝 Δημιουργία Ψηφιακού Δελτίου")
    
    if 'my_bet' not in st.session_state:
        st.session_state.my_bet = []

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        code = st.text_input("Κωδικός", placeholder="π.χ. 101")
    with col2:
        # Ενημερωμένη λίστα με όλες τις βασικές επιλογές και O/U έως 3.5
        market_options = [
            "1", "X", "2", 
            "G/G", "N/G",
            "Over 0.5", "Under 0.5",
            "Over 1.5", "Under 1.5",
            "Over 2.5", "Under 2.5",
            "Over 3.5", "Under 3.5",
            "1X", "X2", "12"
        ]
        market = st.selectbox("Επιλογή", market_options)
    with col3:
        odds = st.number_input("Απόδοση", min_value=1.01, value=1.80, step=0.01, format="%.2f")

    if st.button("Προσθήκη στο Δελτίο ➕"):
        if code:
            st.session_state.my_bet.append({"Κωδικός": code, "Σημείο": market, "Απόδοση": odds})
            st.rerun()
        else:
            st.warning("Παρακαλώ εισάγετε τον κωδικό του αγώνα.")

    # Εμφάνιση Δελτίου
    if st.session_state.my_bet:
        st.write("### Οι επιλογές σου:")
        total_odds = 1.0
        
        # Εμφάνιση των αγώνων σε πίνακα για καλύτερη ανάγνωση
        for i, item in enumerate(st.session_state.my_bet):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.info(f"📍 {item['Κωδικός']} | {item['Σημείο']} | Απόδοση: {item['Απόδοση']}")
            with col_b:
                if st.button("❌", key=f"del_{i}"):
                    st.session_state.my_bet.pop(i)
                    st.rerun()
            total_odds *= item['Απόδοση']
        
        st.success(f"**Συνολική Απόδοση: {total_odds:.2f}**")
        
        col_stake, col_win = st.columns(2)
        with col_stake:
            stake = st.number_input("Ποντάρισμα (€)", min_value=0.0, value=10.0)
        with col_win:
            st.metric("Πιθανό Κέρδος", f"{stake * total_odds:.2f}€")

        if st.button("Καθαρισμός Δελτίου 🗑️"):
            st.session_state.my_bet = []
            st.rerun()

# --- ΟΙ ΥΠΟΛΟΙΠΕΣ ΛΕΙΤΟΥΡΓΙΕΣ (Value Bet, Arbitrage, Live Σκορ) ---
elif choice == "Live Σκορ":
    components.html('<iframe src="https://www.livescore.cz/widgets/scores.php?lang=el" width="100%" height="800" frameborder="0"></iframe>', height=850)

elif choice == "Value Bet":
    st.subheader("📊 Υπολογιστής Value Bet")
    od = st.number_input("Απόδοση", value=2.00, format="%.2f")
    pr = st.number_input("Πιθανότητα %", value=50)
    if st.button("Υπολογισμός"):
        ev = (od * (pr/100)) - 1
        if ev > 0: st.success(f"✅ Value! {ev*100:.1f}%")
        else: st.error(f"❌ Όχι Value. {ev*100:.1f}%")

elif choice == "Arbitrage":
    st.subheader("💰 Arbitrage Calculator")
    o1 = st.number_input("Απόδοση 1", value=2.10, format="%.2f")
    o2 = st.number_input("Απόδοση 2", value=2.10, format="%.2f")
    if st.button("Έλεγχος"):
        arb = (1/o1) + (1/o2)
        if arb < 1: st.success(f"🔥 Κέρδος: {((1/arb)-1)*100:.2f}%")
        else: st.warning("Δεν υπάρχει Arbitrage.")
