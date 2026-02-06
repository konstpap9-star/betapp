import streamlit as st
from fpdf import FPDF
import io

st.set_page_config(page_title="Calibration Grid", layout="centered")

def create_calibration_grid():
    # Χρησιμοποιούμε μέγεθος Α4 για να δούμε πού "πατάει" ο εκτυπωτής
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=8)
    
    # Σχεδίαση Κάθετων Γραμμών (Άξονας X - Πλάτος)
    # Θα εκτυπώσει γραμμές κάθε 5mm
    for x in range(0, 211, 5):
        pdf.set_draw_color(200, 200, 200) # Γκρι γραμμή
        pdf.line(x, 0, x, 297)
        if x % 10 == 0:
            pdf.set_text_color(255, 0, 0) # Κόκκινο για τα 10mm
            pdf.text(x + 1, 10, str(x))

    # Σχεδίαση Οριζόντιων Γραμμών (Άξονας Y - Ύψος)
    # Θα εκτυπώσει γραμμές κάθε 5mm
    for y in range(0, 298, 5):
        pdf.set_draw_color(200, 200, 200)
        pdf.line(0, y, 210, y)
        if y % 10 == 0:
            pdf.set_text_color(0, 0, 255) # Μπλε για τα 10mm
            pdf.text(5, y - 1, str(y))

    return pdf.output(dest='S').encode('latin-1')

st.title("🎯 Πλέγμα Βαθμονόμησης")
st.write("Εκτύπωσε αυτό το πλέγμα πάνω στο δελτίο για να βρούμε τις συντεταγμένες.")

if st.button("🖨️ ΕΚΤΥΠΩΣΗ ΠΛΕΓΜΑΤΟΣ"):
    grid_pdf = create_calibration_grid()
    st.download_button(
        label="Λήψη PDF Πλέγματος",
        data=grid_pdf,
        file_name="calibration_grid.pdf",
        mime="application/pdf"
    )

st.warning("Σημαντικό: Κατά την εκτύπωση του PDF, βεβαιώσου ότι στις ρυθμίσεις του εκτυπωτή είναι επιλεγμένο το 'Actual Size' (Πραγματικό Μέγεθος) και ΟΧΙ το 'Fit to page'.")
