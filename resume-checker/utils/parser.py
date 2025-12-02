from pdfminer.high_level import extract_text
import re
import io

def extract_text_from_pdf(file_stream):
    """
    Extracts text from a PDF file stream using pdfminer.six.
    
    Args:
        file_stream (BytesIO): The PDF file stream.
        
    Returns:
        str: The extracted and cleaned text.
    """
    try:
        # Extract text from the PDF stream
        text = extract_text(file_stream)
        
        # Clean up the text
        # Remove special characters but keep punctuation relevant for sentence structure if needed, 
        # but for ATS, mostly alphanumeric and basic punctuation is fine.
        # Replacing multiple newlines/tabs with a single space or newline.
        
        # Remove non-printable characters (optional, but good for safety)
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        
        # Replace multiple spaces/newlines with a single space to make it a continuous stream of text
        # or keep paragraphs. Let's keep it simple: normalize whitespace.
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"
