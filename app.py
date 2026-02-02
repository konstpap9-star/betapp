
import streamlit as st

# Ρύθμιση σελίδας
st.set_page_config(page_title="BigBet Tool", layout="centered")

# --- ΠΛΑΓΙΟ ΜΕΝΟΥ ---
st.sidebar.title("🛠️ Μενού Εργαλείων")
choice = st.sidebar.radio("Επιλέξτε Εργαλείο:", 
                         ["Υπολογιστής Value Bet", "Arbitrage (Σίγουρο Κέρδος)"])

# --- 1. ΥΠΟΛΟΓΙΣΤΗΣ VALUE BET ---
if choice == "Υπολογιστής Value Bet":
    st.title("📊 Υπολογιστής Value Bet")
    st.write("Δες αν η απόδοση του μπουκ είναι μεγαλύτερη από την πραγματική πιθανότητα.")
    
    col1, col2 = st.columns(2)
    with col1:
        od = st.number_input("Απόδοση Εταιρείας", min_value=1.01, value=2.00, step=0.10)
    with col2:
        pr = st.number_input("Η Πιθανότητα που δίνεις %", min_value=1, max_value=100, value=50)
    
    fair = 100 / pr
    ev = (od * (pr / 100)) - 1
    
    st.subheader(f"Δίκαιη Απόδοση: {fair:.2f}")
    if ev > 0:
        st.success(f"✅ ΥΠΑΡΧΕΙ VALUE! Πλεονέκτημα: +{ev*100:.2f}%")
    else:
        st.error(f"❌ ΧΩΡΙΣ VALUE. Μειονέκτημα: {ev*100:.2f}%")

# --- 2. ARBITRAGE CALCULATOR ---
elif choice == "Arbitrage (Σίγουρο Κέρδος)":
    st.title("💰 Arbitrage Calculator")
    st.write("Υπολόγισε αν υπάρχει σίγουρο κέρδος από δύο διαφορετικές εταιρείες.")
    
    c1, c2 = st.columns(2)
    with c1:
        od1 = st.number_input("Απόδοση για Σημείο 1 (π.χ. Άσσος)", min_value=1.01, value=2.10)
    with c2:
        od2 = st.number_input("Απόδοση για Σημείο 2 (π.χ. Διπλό)", min_value=1.01, value=2.10)
    
    total_bet = st.number_input("Συνολικό Ποντάρισμα (€)", min_value=10, value=100)
    
    arbitrage_pct = (1/od1) + (1/od2)
    
    if arbitrage_pct < 1:
        st.success(f"🔥 ARBITRAGE! Σίγουρο κέρδος: {((1/arbitrage_pct)-1)*100:.2f}%")
        stake1 = (total_bet / od1) / arbitrage_pct
        stake2 = (total_bet / od2) / arbitrage_pct
        st.write(f"Πόνταρε **{stake1:.2f}€** στην πρώτη απόδοση")
        st.write(f"Πόνταρε **{stake2:.2f}€** στη δεύτερη απόδοση")
    else:
        st.warning(f"Δεν υπάρχει Arbitrage. Συνολική γκανιότα: {arbitrage_pct*100:.2f}%")

