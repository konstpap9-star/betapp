import streamlit as st
from fpdf import FPDF
import io

st.title("🎯 Καλιμπράρισμα Εκτυπωτή (Portrait)")

st.write("""
Βάλε το δελτίο στον εκτυπωτή όπως στη φωτογραφία σου. 
Θα εκτυπώσουμε τον κωδικό **001** και το σημείο **1** για δοκιμή.
""")

def create_test_pdf():
    # Δημιουργία PDF σε Portrait (Όρθιο)
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Ρυθμίσεις Συντεταγμένων (Δοκιμαστικές)
    # y = το ύψος από την πάνω άκρη του δελτίου
    # x = η απόσταση από την αριστερή άκρη (όπως το βλέπει ο εκτυπωτής)
    
    start_y = 24.0  # Η πρώτη γραμμή του δελτίου
    x_digits = 20.0 # Οι κουκίδες του κωδικού
    x_point_1 = 83.0 # Η κουκίδα για το σημείο "1"
    radius = 1.8

    pdf.set_fill_color(0, 0, 0)
    
    # 1. Εκτύπωση 3 κουκίδων για τον κωδικό (0, 0, 1)
    for i in range(3):
        pdf.ellipse(x_digits + (i * 4.0), start_y - radius, radius*2, radius*2, style='F')
    
    # 2. Εκτύπωση 1 κουκίδας για το σημείο "1"
    pdf.ellipse(x_point_1, start_y - radius, radius*2, radius*2, style='F')
    
    return pdf.output(dest='S').encode('latin-1')

if st.button("🖨️ ΔΗΜΙΟΥΡΓΙΑ PDF ΔΟΚΙΜΗΣ"):
    pdf_data = create_test_pdf()
    st.download_button(
        label="Λήψη PDF Δοκιμής",
        data=pdf_data,
        file_name="test_alignment.pdf",
        mime="application/pdf"
    )

st.info("Μόλις εκτυπώσεις, πες μου αν οι κουκίδες πήγαν πιο δεξιά, πιο αριστερά, πιο πάνω ή πιο κάτω από τα κουτάκια.")
