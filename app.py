

import streamlit as st
import os
from io import BytesIO
import fitz  # PyMuPDF
from PIL import Image

st.set_page_config(page_title="DATA SWEEPER", layout="wide")
st.title("🚀 DATA SWEEPER!")

st.write("Upload your PDF or JPG files and convert them easily!")

# File Upload
uploaded_file = st.file_uploader("Upload a PDF or JPG file", type=["pdf", "jpg", "jpeg", "png"])

# Function to convert PDF to images using PyMuPDF
def pdf_to_images(pdf_bytes):
    doc = fitz.open("pdf", pdf_bytes)  # Open PDF from bytes
    images = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Load a page
        pix = page.get_pixmap()  # Convert page to image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    
    return images

if uploaded_file:
    file_ext = os.path.splitext(uploaded_file.name)[-1].lower()

    # PDF to JPG Conversion
    if file_ext == ".pdf":
        st.write("📄 PDF file uploaded!")
        images = pdf_to_images(uploaded_file.read())  # Convert PDF pages to images

        # Display preview of first page
        st.image(images[0], caption="Preview of converted JPG", use_column_width=True)

        img_buffer = BytesIO()
        images[0].save(img_buffer, format="JPEG")
        img_buffer.seek(0)

        # Debugging Print
        st.write(f"🛠️ Debug: File size → {img_buffer.getbuffer().nbytes} bytes")

        # Download Button for JPG
        st.download_button(
            label="Download as JPG",
            data=img_buffer,
            file_name="converted.jpg",
            mime="image/jpeg"
        )

        # Success Message
        st.success("🎉 File converted successfully!")

    # JPG/PNG to PDF Conversion
    elif file_ext in [".jpg", ".jpeg", ".png"]:
        st.image(uploaded_file, caption="🖼️ Uploaded Image", use_column_width=True)

        # Unique key for radio button
        conversion_type = st.radio("Select conversion type:", ["PDF", "JPG"], key=f"conversion_{uploaded_file.name}")

        if st.button(f"Convert {uploaded_file.name}"):
            buffer = BytesIO()
            img = Image.open(uploaded_file)

            if conversion_type == "PDF":
                img.convert("RGB").save(buffer, format="PDF")
                file_name = "converted.pdf"
                mime_type = "application/pdf"
            else:
                img.convert("RGB").save(buffer, format="JPEG")
                file_name = "converted.jpg"
                mime_type = "image/jpeg"

            buffer.seek(0)  # Reset buffer before download

            st.write(f"🛠️ Debug: Final file size → {buffer.getbuffer().nbytes} bytes")

            st.download_button(
                label=f"Download as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

            # Success Message
            st.success("🎉 File converted successfully!")
