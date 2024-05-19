import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Initialize an empty string to store extracted text
    extracted_text = ""

    # Iterate through PDF pages and extract text
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        text = page.get_text()

        # Add text to the extracted_text string
        extracted_text += text

    # Close the PDF document
    pdf_document.close()

    return extracted_text


if __name__ == "__main__":
    # Replace 'document.pdf' with the path to your PDF file
    pdf_file_path = r'C:\Users\ok\Documents\Ps.pdf.'

    extracted_text = extract_text_from_pdf(pdf_file_path)

    print("Extracted Text:")
    print(extracted_text)
