import streamlit as st
import pandas as pd
import random
from itertools import combinations

st.set_page_config(page_title="BigBet Tool", layout="wide")

# --- CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp {background-color: #f0f2f6;}
    .stRadio > div { flex-direction: row; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏆 BigBet Tool")
choice = st.radio("Διάλεξε Εργαλείο:", ["Ανάπτυξη Στηλών", "Live Σκορ"], horizontal=True)

if choice == "Ανάπτυξη Στηλών":
    if 'my_bet' not in st.session_state: st.session_state.my_bet = []
    
    # 1. ΕΙΣΑΓΩΓΗ
    st.subheader("📝 Εισαγωγή Αγώνων")
    raw_input = st.text_input("Κωδικοί (π.χ. 101102103):")
    if st.button("Προσθήκη ➕"):
        if raw_input:
            new = [raw_input[i:i+3] for i in range(0, len(raw_input), 3)]
            for c in new:
                if len(c) == 3: st.session_state.my_bet.append({"Κωδικός": c, "Σημείο": "1"})
            st.rerun()

    # 2. ΕΠΕΞΕΡΓΑΣΙΑ ΑΓΩΝΩΝ
    if st.session_state.my_bet:
        for i, item in enumerate(st.session_state.my_bet):
            c1, c2, c3 = st.columns([1, 2, 0.5])
            with c1: st.session_state.my_bet[i]['Κωδικός'] = st.text_input(f"c_{i}", value=item['Κωδικός'], label_visibility="collapsed")
            with c2: st.session_state.my_bet[i]['Σημείο'] = st.selectbox(f"m_{i}", ["1","X","2","G/G","N/G","Over 2.5","Under 2.5","1X","X2"], index=0, label_visibility="collapsed")
            with c3:
                if st.button("❌", key=f"del_{i}"):
                    st.session_state.my_bet.pop(i)
                    st.rerun()

        # 3. ΑΝΑΠΤΥΞΗ ΣΤΗΛΩΝ
        st.markdown("---")
        n = len(st.session_state.my_bet)
        k_sys = st.number_input("Ζητούμενα (π.χ. 3άδες):", min_value=1, max_value=n if n>0 else 1, value=min(n, 3) if n>0 else 1)
        
        if st.button("Ανάπτυξη Συνδυασμών ⚙️"):
            combos = list(combinations(st.session_state.my_bet, k_sys))
            data = []
            for idx, c in enumerate(combos):
                content = ", ".join([f"{item['Κωδικός']}({item['Σημείο']})" for item in c])
                data.append({"Επιλογή": True, "Στήλη": idx + 1, "Περιεχόμενο": content})
            st.session_state.all_columns = pd.DataFrame(data)

        # 4. ΦΙΛΤΡΑΡΙΣΜΑ & ΠΙΝΑΚΑΣ
        if 'all_columns' in st.session_state:
            st.subheader("📊 Διαχείριση Στηλών")
            
            # Τυχαία Αφαίρεση
            col_rand1, col_rand2 = st.columns([1, 1])
            with col_rand1:
                num_to_keep = st.number_input("Πόσες τυχαίες στήλες να κρατήσω;", min_value=1, max_value=len(st.session_state.all_columns), value=len(st.session_state.all_columns))
            with col_rand2:
                if st.button("Τυχαία Επιλογή 🎲"):
                    # Μηδενίζουμε όλες τις επιλογές
                    st.session_state.all_columns['Επιλογή'] = False
                    # Επιλέγουμε τυχαία indexes
                    keep_idx = random.sample(list(st.session_state.all_columns.index), num_to_keep)
                    st.session_state.all_columns.loc[keep_idx, 'Επιλογή'] = True

            # Πίνακας για χειροκίνητη επιλογή
            edited_df = st.data_editor(
                st.session_state.all_columns,
                column_config={"Επιλογή": st.column_config.CheckboxColumn(required=True)},
                disabled=["Στήλη", "Περιεχόμενο"],
                hide_index=True,
                use_container_width=True
            )
            st.session_state.all_columns = edited_df

            # Τελικό Αποτέλεσμα
            selected_count = len(edited_df[edited_df['Επιλογή'] == True])
            st.success(f"Ενεργές Στήλες: {selected_count} / {len(edited_df)}")
            st.info(f"Συνολικό Κόστος (0.25€/στήλη): {selected_count * 0.25:.2f}€")

        if st.button("Καθαρισμός Όλων 🗑️"):
            if 'all_columns' in st.session_state: del st.session_state.all_columns
            st.session_state.my_bet = []
            st.rerun()

elif choice == "Live Σκορ":
    st.components.v1.html('<iframe src="https://www.livescore.cz/widgets/scores.php?lang=el" width="100%" height="800" frameborder="0"></iframe>', height=850)
