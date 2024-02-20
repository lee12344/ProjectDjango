"""
from flask import Flask, jsonify, request, render_template
import cv2
import easyocr
import numpy as np
import os
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Function to preprocess the license plate image
def preprocess_license_plate(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to convert to binary image
    _, binary_image = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

    # Apply morphological operations for noise removal and feature enhancement
    kernel = np.ones((5, 13), np.uint8)
    morph = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel, iterations=3)

    return morph

# Function to extract license plate text using OCR
def extract_license_plate_text(plate_img):
    # Convert the plate image to RGB format
    plate_img_rgb = cv2.cvtColor(plate_img, cv2.COLOR_BGR2RGB)

    # Initialize the OCR reader for Korean language
    reader = easyocr.Reader(['ko'])

    # Use OCR to extract text from the plate image
    results = reader.readtext(plate_img_rgb)

    # Check if OCR results are available
    if results:
        plate_text = results[0][1]
        return plate_text
    else:
        return "Error: Failed to extract license plate text."

# Route to render upload form
@app.route('/')
def upload_form():
    return render_template('apphtml.html')

# Route to extract license plate text
@app.route('/extract_license_plate_text', methods=['POST'])
def extract_license_plate_text_route():
    try:
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Check if the file is allowed
        if file and allowed_file(file.filename):
            # Read the image file
            image_stream = file.read()
            nparr = np.frombuffer(image_stream, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Preprocess the license plate image
            plate_img = preprocess_license_plate(image)

            # Extract license plate text
            plate_text = extract_license_plate_text(plate_img)

            # Return extracted license plate text as JSON response
            response = {'plate_text': plate_text}
            return jsonify(response)
        else:
            return jsonify({'error': 'File type not allowed'}), 400
    except Exception as e:
        # Handle exceptions and return error message
        return jsonify({'error': str(e)}), 500

# Function to check if the file extension is allowed
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
"""