from docx import Document

def extract_text_from_docx(filepath):
    try:
        doc = Document(filepath)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error extracting DOCX: {str(e)}"
