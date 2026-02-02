import streamlit as st
import streamlit.components.v1 as components

# Ρυθμίσεις εμφάνισης
st.set_page_config(page_title="BigBet Tool", layout="wide")

# --- CSS ΓΙΑ ΚΑΛΥΤΕΡΗ ΕΜΦΑΝΙΣΗ ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #f0f2f6;}
    </style>
    """, unsafe_allow_html=True)

# --- ΠΛΑΓΙΟ ΜΕΝΟΥ ---
st.sidebar.title("🛠️ Εργαλεία")
choice = st.sidebar.radio("Επιλέξτε λειτουργία:", 
                         ["Ζωντανά Σκορ", "Value Bet", "Arbitrage", "Κάλυψη (DNB)"])

# --- 1. ΖΩΝΤΑΝΑ ΣΚΟΡ ---
if choice == "Ζωντανά Σκορ":
    st.title("⚽ Ζωντανά Αποτελέσματα")
    st.write("Δες την εξέλιξη των αγώνων σε πραγματικό χρόνο.")
    
    # Ενσωμάτωση εξωτερικού Live Score widget (δωρεάν και σταθερό)
    components.html(
        """
        <div id="fs-wm"></div>
        <script type="text/javascript" src="https://widget.enetscore.com/FWB4A1D88E23689456"></script>
        <iframe src="https://www.livescore.cz/widgets/scores.php?lang=el" 
                width="100%" height="800" frameborder="0"></iframe>
        """,
        height=800,
        scrolling=True
    )

# --- 2. VALUE BET ---
elif choice == "Value Bet":
    st.title("📊 Value Bet")
    od = st.number_input("Απόδοση", min_value=1.01, value=2.00)
    pr = st.number_input("Πιθανότητα %", min_value=1, max_value=100, value=50)
    if st.button("Υπολογισμός"):
        ev = (od * (pr/100)) - 1
        if ev > 0: st.success(f"✅ VALUE! +{ev*100:.1f}%")
        else: st.error(f"❌ ΟΧΙ VALUE. {ev*100:.1f}%")

# --- 3. ARBITRAGE ---
elif choice == "Arbitrage":
    st.title("💰 Arbitrage")
    o1 = st.number_input("Απόδοση 1", value=2.10)
    o2 = st.number_input("Απόδοση 2", value=2.10)
    if st.button("Έλεγχος"):
        arb = (1/o1) + (1/o2)
        if arb < 1: st.success(f"🔥 ΣΙΓΟΥΡΟ ΚΕΡΔΟΣ! {((1/arb)-1)*100:.2f}%")
        else: st.warning("Δεν υπάρχει Arbitrage.")

# --- 4. ΚΑΛΥΨΗ (DNB) ---
elif choice == "Κάλυψη (DNB)":
    st.title("🛡️ Κάλυψη (DNB)")
    win_od = st.number_input("Απόδοση Νίκης", value=2.50)
    draw_od = st.number_input("Απόδοση Ισοπαλίας", value=3.20)
    total = st.number_input("Ποσό (€)", value=20)
    if st.button("Υπολογισμός"):
        d_stake = total / draw_od
        w_stake = total - d_stake
        st.info(f"Πόνταρε {d_stake:.2f}€ στο Χ και {w_stake:.2f}€ στη Νίκη.")

