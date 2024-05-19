from flask import Flask, render_template, request, jsonify
from PIL import Image
import pytesseract
import base64
from io import BytesIO

app = Flask(__name__)

# Specify the full path to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Function to extract text from a cropped image
def extract_text_from_cropped_image(image_data):
    try:
        # Decode base64 image data
        image_bytes = base64.b64decode(image_data.split(',')[1])

        # Open image from bytes
        image = Image.open(BytesIO(image_bytes))

        # Extract text using Tesseract
        extracted_text = pytesseract.image_to_string(image)

        return extracted_text
    except pytesseract.TesseractNotFoundError as e:
        return f"Tesseract not found. Make sure the path is correctly specified. Error details: {e}"


# Homepage with file upload form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "imageData" not in request.json:
            return "No image data"

        image_data = request.json["imageData"]
        extracted_text = extract_text_from_cropped_image(image_data)

        return extracted_text

    return render_template("index.html")


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
