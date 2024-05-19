import pytesseract

# Specify the full path to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_and_display_text(image_path):
    try:
        extracted_text = pytesseract.image_to_string(image_path)
        print("Extracted Text:")
        print(extracted_text)
    except pytesseract.TesseractNotFoundError as e:
        print("Tesseract not found. Make sure the path is correctly specified.")
        print("Error details:", e)

if __name__ == "__main__":
    # Replace 'image.jpg' with the path to your image file
    image_file_path = 'download22.jpg'
    extract_and_display_text(image_file_path)
