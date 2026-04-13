from PyPDF2 import PdfReader

def extract_text_from_pdf(filepath):
    try:
        reader = PdfReader(filepath)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"
