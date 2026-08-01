import pdfplumber


# ---------------------------------------------------------
# Extract Text from PDF
# ---------------------------------------------------------

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts all text from a PDF file.

    Args:
        file_path: Path to the uploaded PDF.

    Returns:
        Extracted text as a single string.
    """

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text