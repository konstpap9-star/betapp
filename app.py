import streamlit as st
import math

st.set_page_config(page_title="BigBet Tool", layout="wide")

# --- CSS ΣΤΥΛ ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp {background-color: #f0f2f6;}
    .stRadio > div { flex-direction: row; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- ΚΕΝΤΡΙΚΟ ΜΕΝΟΥ ---
st.title("🏆 BigBet Tool")
choice = st.radio("Διάλεξε Εργαλείο:", ["Ανάπτυξη Στηλών", "Live Σκορ"], horizontal=True)

st.markdown("---")

if choice == "Ανάπτυξη Στηλών":
    if 'my_bet' not in st.session_state:
        st.session_state.my_bet = []

    # Λίστα σημείων
    market_options = [
        "1", "X", "2", "G/G", "N/G",
        "Over 0.5", "Under 0.5", "Over 1.5", "Under 1.5",
        "Over 2.5", "Under 2.5", "Over 3.5", "Under 3.5",
        "1X", "X2", "12"
    ]

    st.subheader("📝 Εισαγωγή Αγώνων")
    st.write("Γράψε τους κωδικούς συνεχόμενα (π.χ. 101102103):")
    raw_input = st.text_input("Εισαγωγή κωδικών:", key="bulk_input")
    
    if st.button("Προσθήκη Αγώνων ➕"):
        if raw_input:
            new_codes = [raw_input[i:i+3] for i in range(0, len(raw_input), 3)]
            for c in new_codes:
                if len(c) == 3:
                    st.session_state.my_bet.append({"Κωδικός": c, "Σημείο": "1"})
            st.rerun()

    # ΕΠΕΞΕΡΓΑΣΙΑ ΑΓΩΝΩΝ (Χωρίς Αποδόσεις)
    if st.session_state.my_bet:
        st.markdown("---")
        st.write("### Το Δελτίο σου")
        
        for i, item in enumerate(st.session_state.my_bet):
            col_code, col_market, col_del = st.columns([1, 2, 0.5])
            with col_code:
                st.session_state.my_bet[i]['Κωδικός'] = st.text_input(f"c_{i}", value=item['Κωδικός'], label_visibility="collapsed")
            with col_market:
                st.session_state.my_bet[i]['Σημείο'] = st.selectbox(f"m_{i}", market_options, index=market_options.index(item['Σημείο']), label_visibility="collapsed")
            with col_del:
                if st.button("❌", key=f"del_{i}"):
                    st.session_state.my_bet.pop(i)
                    st.rerun()

        # ΥΠΟΛΟΓΙΣΜΟΣ ΣΤΗΛΩΝ
        st.markdown("---")
        st.subheader("🔢 Ανάπτυξη Συστήματος")
        n = len(st.session_state.codes if 'codes' in st.session_state else st.session_state.my_bet)
        
        if n > 0:
            sys_choice = st.multiselect(f"Επίλεξε Ζητούμενα από τους {n} αγώνες:", range(1, n + 1))
            
            if sys_choice:
                total_columns = 0
                for k in sys_choice:
                    cols = math.comb(n, k)
                    total_columns += cols
                    st.write(f"🔹 **{k}άδες:** {cols} στήλες")
                
                st.success(f"### Συνολικές Στήλες: {total_columns}")
                
                cost_per_col = st.number_input("Κόστος ανά στήλη (€)", value=0.25, step=0.05)
                st.warning(f"**Συνολικό Κόστος: {total_columns * cost_per_col:.2f}€**")

        if st.button("Καθαρισμός Όλων 🗑️"):
            st.session_state.my_bet = []
            st.rerun()

elif choice == "Live Σκορ":
    st.components.v1.html('<iframe src="https://www.livescore.cz/widgets/scores.php?lang=el" width="100%" height="800" frameborder="0"></iframe>', height=850)
