import os
import streamlit as st
from fpdf import FPDF

# Save the debate as a PDF
def save_debate_as_pdf(debate_id, topic, pro_args, con_args):

        # Create the 'pdf' folder if it doesn't exist
        os.makedirs("pdf", exist_ok=True)

        # Define where the PDF file will be saved
        file_name = f"pdf/{debate_id}.pdf"
        pdf = FPDF()
        pdf.add_page()
        # Add the custom font for Unicode support
        pdf.add_font("DejaVu", "", "static/DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", size=12)

        pdf.cell(200, 10, txt=f"Debate Topic: {topic}", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Debate ID: {debate_id}", ln=True, align="C")
        pdf.cell(200, 10, txt="Pro Arguments:", ln=True, align="L")
        pdf.multi_cell(200, 10, txt=pro_args)
        pdf.cell(200, 10, txt="Con Arguments:", ln=True, align="L")
        pdf.multi_cell(200, 10, txt=con_args)

        pdf.output(file_name)

# Add download button for the PDF
def download_pdf(debate_id):
        pdf_path = f"pdf/{debate_id}.pdf"
        try:
                with open(pdf_path, "rb") as pdf_file:
                        pdf_data = pdf_file.read()
                st.download_button(
                        label="Download PDF",
                        data=pdf_data,
                        file_name=f"{debate_id}.pdf",
                        mime="application/pdf"
                )
        except Exception as e:
                st.write("No PDF available for download.")