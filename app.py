import streamlit as st
import streamlit.components.v1 as components

# Ρυθμίσεις εμφάνισης
st.set_page_config(page_title="BigBet Tool", layout="wide")

# --- CSS ΓΙΑ ΚΑΘΑΡΗ ΕΜΦΑΝΙΣΗ ΧΩΡΙΣ ΜΕΝΟΥ STREAMLIT ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #f0f2f6;}
    /* Στυλ για το μενού στο κέντρο */
    .stRadio > div {
        flex-direction: row;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ΚΕΝΤΡΙΚΟ ΜΕΝΟΥ ΠΑΝΩ-ΠΑΝΩ ---
st.title("🏆 BigBet Tool")
choice = st.radio("Διάλεξε Εργαλείο:", 
                 ["Live Σκορ", "Value Bet", "Arbitrage", "Κάλυψη (DNB)"],
                 horizontal=True)

st.markdown("---") # Μια γραμμή για διαχωρισμό

# --- 1. ΖΩΝΤΑΝΑ ΣΚΟΡ ---
if choice == "Live Σκορ":
    st.subheader("⚽ Ζωντανά Αποτελέσματα")
    components.html(
        """
        <iframe src="https://www.livescore.cz/widgets/scores.php?lang=el" 
                width="100%" height="800" frameborder="0"></iframe>
        """,
        height=850,
        scrolling=True
    )

# --- 2. VALUE BET ---
elif choice == "Value Bet":
    st.subheader("📊 Υπολογιστής Value Bet")
    od = st.number_input("Απόδοση", min_value=1.01, value=2.00)
    pr = st.number_input("Πιθανότητα που δίνεις %", min_value=1, max_value=100, value=50)
    if st.button("Υπολογισμός"):
        ev = (od * (pr/100)) - 1
        if ev > 0: st.success(f"✅ VALUE! +{ev*100:.1f}%")
        else: st.error(f"❌ ΟΧΙ VALUE. {ev*100:.1f}%")

# --- 3. ARBITRAGE ---
elif choice == "Arbitrage":
    st.subheader("💰 Arbitrage Calculator")
    o1 = st.number_input("Απόδοση 1", value=2.10)
    o2 = st.number_input("Απόδοση 2", value=2.10)
    bet = st.number_input("Ποσό (€)", value=100)
    if st.button("Έλεγχος"):
        arb = (1/o1) + (1/o2)
        if arb < 1:
            s1 = (bet/o1)/arb
            s2 = (bet/o2)/arb
            st.success(f"🔥 ΚΕΡΔΟΣ: {((1/arb)-1)*100:.2f}%")
            st.write(f"Πόνταρε **{s1:.2f}€** και **{s2:.2f}€**")
        else: st.warning("Δεν υπάρχει κέρδος.")

# --- 4. ΚΑΛΥΨΗ (DNB) ---
elif choice == "Κάλυψη (DNB)":
    st.subheader("🛡️ Κάλυψη στην Ισοπαλία")
    win_od = st.number_input("Απόδοση Νίκης", value=2.50)
    draw_od = st.number_input("Απόδοση Ισοπαλίας", value=3.20)
    total = st.number_input("Συνολικό Ποντάρισμα (€)", value=20)
    if st.button("Υπολογισμός"):
        d_stake = total / draw_od
        w_stake = total - d_stake
        st.info(f"Πόνταρε {d_stake:.2f}€ στο Χ και {w_stake:.2f}€ στη Νίκη.")
