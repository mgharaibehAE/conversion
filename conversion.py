import streamlit as st
import PyPDF2
from fpdf import FPDF
import io

# Configure page
st.set_page_config(page_title="PDF Upload & Export", page_icon="📄")

st.header("Upload and Convert PDF")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    reader = PyPDF2.PdfReader(uploaded_file)
    file_text = ""
    for page in reader.pages:
        file_text += page.extract_text() + "\n"

    st.subheader("Extracted Text")
    st.text_area("PDF Text", file_text, height=250)

    export_option = st.selectbox("Export format", ["PDF", "TXT"])

    if st.button("Export File"):
        if export_option == "PDF":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            lines = file_text.split('\n')
            for line in lines:
                pdf.multi_cell(0, 10, line)

            pdf_buffer = io.BytesIO()
            pdf.output(pdf_buffer)
            pdf_buffer.seek(0)

            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name="converted_file.pdf",
                mime="application/pdf"
            )

        elif export_option == "TXT":
            st.download_button(
                label="Download TXT",
                data=file_text,
                file_name="converted_file.txt",
                mime="text/plain"
            )
