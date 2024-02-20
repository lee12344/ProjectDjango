"""
from flask import Flask, jsonify, request
import cv2
import easyocr
import numpy as np
import os

app = Flask(__name__)

# Function to preprocess the license plate image
def preprocess_license_plate(car_no):
    image_path = f"images/car/{car_no:02d}.jpg"

    # Check if the image file exists
    if not os.path.exists(image_path):
        return None, "Error: Image file not found."

    # Read the image in BGR color
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to convert to binary image
    _, binary_image = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

    # Apply morphological operations for noise removal and feature enhancement
    kernel = np.ones((5, 13), np.uint8)
    morph = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel, iterations=3)

    return image, morph

# Function to extract license plate text using OCR
def extract_license_plate_text(plate_img):
    # Check if the plate image is None
    if plate_img is None:
        return "Error: Failed to preprocess the license plate image."

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

# Route to extract license plate text
@app.route('/extract_license_plate_text', methods=['POST'])
def extract_license_plate_text_route():
    try:
        # Get car number from the POST request data
        data = request.get_json()
        car_no = int(data.get('car_no', 0))

        # Preprocess the license plate image
        plate_img, _ = preprocess_license_plate(car_no)

        # Extract license plate text
        plate_text = extract_license_plate_text(plate_img)

        # Return extracted license plate text as JSON response
        response = {'plate_text': plate_text}
        return jsonify(response)
    except Exception as e:
        # Handle exceptions and return error message
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
"""