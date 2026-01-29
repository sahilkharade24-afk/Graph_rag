import pdfplumber

def load_pdf(file_source):
    """
    Loads a PDF file and returns its text content.
    Works with both file paths and file-like objects (e.g., Streamlit UploadedFile).
    """
    with pdfplumber.open(file_source) as pdf:
        text = ""
        for page in pdf.pages:
            # Check if page.extract_text() returns None
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text
