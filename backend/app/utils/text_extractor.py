"""
Text extraction utility for resume files
Supports PDF, DOCX, and TXT formats
"""

import os
from typing import Optional
from werkzeug.datastructures import FileStorage

def extract_text_from_file(file: FileStorage) -> Optional[str]:
    """
    Extract text from uploaded file
    
    Args:
        file: Uploaded file object
        
    Returns:
        Extracted text or None if failed
    """
    filename = file.filename.lower()
    
    try:
        if filename.endswith('.txt'):
            return file.read().decode('utf-8', errors='ignore')
        
        elif filename.endswith('.pdf'):
            return extract_text_from_pdf(file)
        
        elif filename.endswith(('.docx', '.doc')):
            return extract_text_from_docx(file)
        
        else:
            return None
            
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        return None

def extract_text_from_pdf(file: FileStorage) -> str:
    """Extract text from PDF file"""
    try:
        import PyPDF2
        import tempfile

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_path = temp_file.name
            file.save(temp_path)

        text = ""
        with open(temp_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"

        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)

        return text.strip()

    except ImportError:
        # Fallback if PyPDF2 not available
        print("PyPDF2 not installed, using basic extraction")
        return file.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"PDF extraction error: {str(e)}")
        return ""

def extract_text_from_docx(file: FileStorage) -> str:
    """Extract text from DOCX file"""
    try:
        import docx
        import tempfile

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
            temp_path = temp_file.name
            file.save(temp_path)

        doc = docx.Document(temp_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)

        return text.strip()

    except ImportError:
        # Fallback if python-docx not available
        print("python-docx not installed, using basic extraction")
        return file.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"DOCX extraction error: {str(e)}")
        return ""
