import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="Calibration Grid v2", layout="centered")

def create_calibration_grid():
    # Ορίζουμε το μέγεθος σελίδας ακριβώς όσο ένα δελτίο
    # Πλάτος 105mm, Ύψος 230mm
    pdf = FPDF(orientation='P', unit='mm', format=(105, 230))
    pdf.add_page()
    pdf.set_font("Arial", size=7)
    
    # Σχεδίαση Κάθετων Γραμμών (X) ανά 2mm για μέγιστη ακρίβεια
    for x in range(0, 106, 2):
        pdf.set_draw_color(220, 220, 220) # Πολύ ανοιχτό γκρι
        pdf.line(x, 0, x, 230)
        if x % 10 == 0:
            pdf.set_text_color(255, 0, 0) # Κόκκινο για τα εκατοστά
            pdf.text(x + 0.5, 5, str(x))

    # Σχεδίαση Οριζόντιων Γραμμών (Y) ανά 2mm
    for y in range(0, 231, 2):
        pdf.set_draw_color(220, 220, 220)
        pdf.line(0, y, 105, y)
        if y % 10 == 0:
            pdf.set_text_color(0, 0, 255) # Μπλε για τα εκατοστά
            pdf.text(1, y - 0.5, str(y))

    return pdf.output(dest='S').encode('latin-1')

st.title("🎯 Πλέγμα Ακριβείας (105x230)")
st.write("Αυτό το PDF έχει το μέγεθος του δελτίου για να το αναγνωρίσει ο εκτυπωτής.")

if st.button("🖨️ ΛΗΨΗ ΠΛΕΓΜΑΤΟΣ"):
    grid_pdf = create_calibration_grid()
    st.download_button(
        label="Κατέβασμα PDF",
        data=grid_pdf,
        file_name="grid_105x230.pdf",
        mime="application/pdf"
    )
