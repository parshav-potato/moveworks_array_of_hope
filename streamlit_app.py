import requests
from bs4 import BeautifulSoup
import streamlit as st
from io import BytesIO
import re
from PyPDF2 import PdfWriter
from reportlab.pdfgen import canvas


def extract_text_from_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string.strip()
    text = soup.get_text(separator=' ')
    text = "\n".join(line for line in text.splitlines() if line.strip())
    return text, title
def main():
    st.title("Website Text Extractor")
    url = st.text_input("Enter the URL of the website:")
    if st.button("Extract Text"):
        if url:
            try:
                extracted_text, webpage_title = extract_text_from_website(url)
                st.success("Text extraction successful!")
                st.text_area("Extracted Text:", value=extracted_text, height=400)
                pdf_bytes = BytesIO()
                pdf_writer = PdfWriter()
                c = canvas.Canvas(pdf_bytes)
                c.setFont("Helvetica", 12)
                c.drawString(50, 800, extracted_text)
                c.save()
                pdf_bytes.seek(0)
                file_name = re.sub(r'[\\/:"*?<>|]+', '_', webpage_title) + ".pdf"
                st.download_button("Download", data=pdf_bytes, file_name=file_name)
            except Exception as e:
                st.error("An error occurred during text extraction.")
                st.error(str(e))
        else:
            st.warning("Please enter a URL.")
